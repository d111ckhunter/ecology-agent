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
│   └── schemas/                # Pydantic v2 请求/响应模型（自动生成）
├── tools/
│   └── build_schema.py         # 代码生成器：解析 xlsx 模板 → 重新生成 model/schema/docs
├── scripts/
│   ├── init_db.py              # 初始化脚本：建库 + 建表
│   └── mock_data.py            # Mock 数据生成：向 ecology_demo 灌入示例数据
└── docs/
    ├── schema_manifest.json    # 全库表结构定义（机器可读，唯一事实源）
    └── schema_report.md        # 表结构文档（人类/LLM 可读）
```

各部分职责：

| 路径 | 用途 | 何时使用 |
|---|---|---|
| `app/models/`、`app/schemas/` | 应用的 ORM 与校验模型，应用运行直接依赖 | 日常运行，勿手改 |
| `tools/build_schema.py` | 由 Excel 模板（前三行：英文列码/中文含义/填写说明）生成 model、schema、docs | 仅当模板变动或扩展新领域时 |
| `scripts/init_db.py` | 在 MySQL 建库（`ecology_demo`）并创建全部表 | 新机器初始化、库表变更后 |
| `scripts/mock_data.py` | 向全部表灌入语义合理的 mock 数据 | 开发/测试需要样例数据时 |
| `docs/` | 表结构清单与字段字典 | 查阅结构、供导入器/LLM 使用 |

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

### 3. 生成 Mock 数据（开发/测试用）

```bash
# 清空全部表后灌入 mock 数据（seed=42，可复现）：
python scripts/mock_data.py --reset

# 换种子 / 只预览不写库：
python scripts/mock_data.py --seed 7
python scripts/mock_data.py --dry-run
```

- 读取 `docs/schema_manifest.json` 驱动生成，维度表先于事实表插入，外键引用父表已生成的主键；
- 共 23 张表约千行：每张测站/物种等维度表 5~14 行，数据表按月展开（如 6 站 × 24 月）；
- 已埋入验证样本：**超标值**（3~6 倍放大）、**缺测**（约 2% 数值列置 NULL）、**季节波动**（水温正弦）与**趋势**（水位/氮磷缓升）；
- 生成前请先执行 `python scripts/init_db.py` 确保表存在；数据仅用于开发测试，无真实数据。

### 4. 启动 API

```bash
python -m uvicorn app.main:app --reload --port 8000
```

启动后访问 `http://127.0.0.1:8000/docs` 查看接口文档，`/health` 可检查服务状态。
