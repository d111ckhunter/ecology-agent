# ecology-agent（demo）

生态环境监测数据查询 Agent 后端（demo 阶段：**01 水环境** + **02 水生生态**）。
技术栈：MySQL 8 + Python（conda：`fastapi`）+ FastAPI + SQLAlchemy 2 + Pydantic v2。

## 目录结构

```
ecology-agent/
├── app/                        # FastAPI 后端包
│   ├── main.py                 # 应用入口（FastAPI 实例，/health）
│   ├── core/
│   │   ├── config.py           # 数据库连接配置（可用环境变量覆盖）
│   │   └── database.py         # SQLAlchemy engine / Session / get_db
│   ├── models/                 # SQLAlchemy ORM 模型（自动生成）
│   │   ├── water_env.py        #   01 水环境（14 表）
│   │   └── aqua_eco.py         #   02 水生生态（9 表）
│   ├── schemas/                # Pydantic v2 请求/响应模型（自动生成）
│   └── agent/                  # 问答 Agent（text-to-SQL）
│       ├── schema.py           #   读 schema_manifest → LLM 表字典
│       ├── llm.py              #   DeepSeek 封装（openai SDK / mock 模式）
│       ├── db_tool.py          #   只读 SQL 执行 + 安全护栏
│       ├── agent.py            #   编排：生成 SQL → 执行 → 纠错 → 成稿
│       └── cli.py              #   CLI 入口（交互 / --question）
├── tools/
│   └── build_schema.py         # 代码生成器：解析 xlsx 模板 → 重新生成 model/schema/docs
├── scripts/
│   ├── init_db.py              # 初始化脚本：建库 + 建表
│   ├── mock_data.py            # Mock 数据生成：向 ecology_demo 灌示例数据
│   └── setup_readonly_user.py  # 创建只读账号 ecology_ro 并回填 .env
└── docs/
    ├── schema_manifest.json    # 全库表结构定义（机器可读，唯一事实源）
    ├── schema_report.md        # 表结构文档（人类/LLM 可读）
    └── agent_design.md         # Agent 设计文档
```

各部分职责：

| 路径 | 用途 | 何时使用 |
|---|---|---|
| `app/models/`、`app/schemas/` | 应用的 ORM 与校验模型，应用运行直接依赖 | 日常运行，勿手改 |
| `tools/build_schema.py` | 由 Excel 模板（前三行：英文列码/中文含义/填写说明）生成 model、schema、docs | 仅当模板变动或扩展新领域时 |
| `scripts/init_db.py` | 在 MySQL 建库（`ecology_demo`）并创建全部表 | 新机器初始化、库表变更后 |
| `scripts/mock_data.py` | 向全部表灌入语义合理的 mock 数据（含超标/缺测埋点） | 开发/测试需要样例数据时 |
| `scripts/setup_readonly_user.py` | 创建只读账号 `ecology_ro`（仅 SELECT）并回填 `.env` | 新机器、Agent 查询前 |
| `app/agent/` | text-to-SQL 问答 Agent（CLI） | 有 `LLM_API_KEY` 后问答 |
| `docs/` | 表结构清单、字段字典与设计文档 | 查阅结构、供导入器/LLM 使用 |

## 环境准备（首次）

```bash
pip install -r requirements.txt
cp .env.example .env          # 按本机填写 DB_* 与 LLM_API_KEY
python scripts/init_db.py     # 建库建表
python scripts/mock_data.py --reset   # （可选）灌入 mock 数据
python scripts/setup_readonly_user.py # 创建只读账号并回填 .env
```

## 脚本使用方法

### 1. 初始化数据库（建库建表）

```bash
# 首次初始化 / 新增了表后补齐：
python scripts/init_db.py

# 重建全部表（先删后建，会清空数据，仅演示环境使用）：
python scripts/init_db.py --drop
```

- 默认连接 `127.0.0.1:3307`，root，密码 `123456`，库名 `ecology_demo`；
- 连接信息可用环境变量覆盖：`DB_HOST` / `DB_PORT` / `DB_USER` / `DB_PASSWORD` / `DB_NAME`；
- `create_all` 只新建缺失的表，**不会修改已有表**，也不会清空已有数据；
- 需要 Python 依赖：`sqlalchemy`、`pymysql`、`cryptography`（`pip install -r requirements.txt` 全装即可）。

### 2. 修改模板后重新生成模型

当 `01水环境`、`02水生生态` 下的 xlsx 模板有改动（增列、改字段），或想扩展到其他领域时：

```bash
# 需在含 openpyxl 的环境执行（base anaconda 已具备）
python tools/build_schema.py
```

- 运行会**覆盖生成** `app/models/`、`app/schemas/`、`docs/` 下的文件；
- 扩新领域时需先在 `tools/build_schema.py` 顶部的 `TABLES`（表登记）、`FKS`（外键）、`PKS`（主键）、`EXPLICIT`（字段类型覆盖）配置中登记，并同步 `app/models/__init__.py` 的导入；
- 生成后如需让新表落到数据库，再执行 `python scripts/init_db.py`。

### 3. Agent 问答（text-to-SQL）

在 `.env` 中填写 `LLM_API_KEY`（DeepSeek，OpenAI 兼容）后：

```bash
# 交互式问答
python -m app.agent.cli

# 单发一问
python -m app.agent.cli -q "2024年哪个测站氨氮最高？"

# 结构化输出（JSON）
python -m app.agent.cli -q "列出各河段鱼类物种数" --json

# 无 key 演示模式（不联网，验证链路）
AGENT_MOCK=1 python -m app.agent.cli
```

- 数据查询一律走只读账号 `ecology_ro`，应用层另有护栏（仅 SELECT/WITH、禁注释与危险函数、自动 `LIMIT 200`、10s 超时）；
- 首次生成 SQL 执行失败会自动把错误回喂 LLM 修正（最多 2 次）；
- 详见 `docs/agent_design.md`。

### 4. 启动 API

```bash
python -m uvicorn app.main:app --reload --port 8000
```

启动后访问 `http://127.0.0.1:8000/docs` 查看接口文档，`/health` 可检查服务状态。
