# ecology-agent

生态环境监测数据查询 Agent（demo：**01 水环境** + **02 水生生态**）。
技术栈：MySQL 8 + Python（conda：`fastapi`）+ FastAPI + SQLAlchemy 2 + Pydantic v2 + Vue3（`web/`，待接入）。

## 目录结构

```
ecology-agent/
├── app/                        # FastAPI 后端包
│   ├── main.py                 # 应用入口（注册路由，/health）
│   ├── core/
│   │   ├── config.py           # 配置（.env 覆盖；主/只读连接、LLM、护栏参数）
│   │   └── database.py         # 主库 engine / Session / get_db
│   ├── models/                 # SQLAlchemy ORM（自动生成 + 会话表）
│   │   ├── water_env.py        #   01 水环境（14 表，自动生成）
│   │   ├── aqua_eco.py         #   02 水生生态（9 表，自动生成）
│   │   └── session.py          #   agent_sessions / agent_messages（多轮记忆）
│   ├── schemas/                # Pydantic v2（自动生成数据表 + api.py 请求模型）
│   ├── services/
│   │   ├── session_store.py    #   会话存储抽象（预留 Redis 实现）
│   │   ├── mysql_session_store.py  # MySQL 实现
│   │   └── agent_service.py    #   会话化 Agent：事件生成器 + 记忆注入
│   ├── api/sessions.py         # REST + SSE 路由
│   └── agent/                  # 问答 Agent 核心（CLI 仍可用）
│       ├── schema.py           #   读 schema_manifest → LLM 表字典
│       ├── llm.py              #   DeepSeek 封装（openai SDK / mock 模式）
│       ├── db_tool.py          #   只读 SQL 执行 + 安全护栏
│       ├── agent.py            #   编排：SQL演进式多轮记忆、纠错重试、成稿
│       └── cli.py              #   CLI 入口（开发期工具）
├── tools/build_schema.py       # xlsx 模板 → 重新生成 models/schemas/docs
├── scripts/
│   ├── init_db.py              # 建库 + 建表
│   ├── mock_data.py            # 向 23 张表灌 mock 数据（含超标/缺测埋点）
│   └── setup_readonly_user.py  # 创建只读账号 ecology_ro 并回填 .env
├── docs/
│   ├── schema_manifest.json    # 全库表结构（机器可读，唯一事实源）
│   ├── schema_report.md        # 表结构文档（人类/LLM 可读）
│   └── agent_design.md         # Agent 设计文档
└── web/                        # Vue3 前端（Vite+TS+Element Plus）
```

## 环境准备（首次）

```bash
# 后端
pip install -r requirements.txt
cp .env.example .env          # 填 DB_* 与 LLM_API_KEY
python scripts/init_db.py              # 建库建表（含会话表，共 25 张）
python scripts/mock_data.py --reset    # （可选）灌入 mock 数据
python scripts/setup_readonly_user.py  # 创建只读账号 ecology_ro 并回填 .env

# 前端
cd web && npm install && cd ..
```

## 启动服务

```bash
# 终端 1：后端（启动参数已内置，直接运行；无 LLM key 用 AGENT_MOCK=1 演示）
AGENT_MOCK=1 python -m app.main
# 可选：--host / --port / --no-reload（均有默认值：127.0.0.1:8000，开发默认热重载）
# 访问 http://127.0.0.1:8000/docs 查看接口；/health 探活

# 终端 2：前端
cd web && npm run dev        # http://localhost:5173（/api 已代理到 8000）
```

## HTTP API（v2，多轮对话）

### 会话
| 方法 | 路径 | 说明 |
|---|---|---|
| POST | `/api/sessions` | 创建会话，body `{"title": "可选"}` |
| GET | `/api/sessions` | 会话列表（最新在前），`?limit=&offset=` |
| GET | `/api/sessions/{id}` | 会话详情 |
| GET | `/api/sessions/{id}/messages` | 历史消息（含 sql / result_summary） |
| POST | `/api/sessions/{id}/chat` | 提问，**SSE 流式**返回，body `{"question": "..."}` |

### SSE 事件协议（`POST /api/sessions/{id}/chat` 响应）
```
event: status  data: {"type":"status","stage":"generating_sql|composing"}
event: sql     data: {"type":"sql","sql":"...","thinking":"..."}
event: table   data: {"type":"table","columns":[...],"rows":[...],"truncated":bool}
event: answer  data: {"type":"answer","text":"..."}
event: error   data: {"type":"error","message":"..."}
event: done    data: {"type":"done","session_id":"...","message_id":...,"ok":true}
```
前端用 `fetch + ReadableStream` 消费（`EventSource` 不支持 POST）。

### 多轮对话记忆
- **SQL 演进式**：每轮把最近 5 个"问题+成功SQL+结果摘要"注入提示词；追问基于最近成功 SQL 改写；
- user/assistant 消息（含 SQL 与结果摘要）持久化到 `agent_sessions / agent_messages`；
- 存储走 `SessionStore` 抽象，未来可平滑换 Redis 实现。

### 快速验证
```bash
# 无 LLM key 也可跑通链路（AGENT_MOCK 演示模式）
AGENT_MOCK=1 python -m app.main

# 建会话
curl -X POST localhost:8000/api/sessions -H 'Content-Type: application/json' -d '{"title":"demo"}'
# 提问（SSE）
curl -N -X POST localhost:8000/api/sessions/<id>/chat \
  -H 'Content-Type: application/json' -d '{"question":"2024年哪个测站氨氮最高？"}'
```

## 安全（Agent 查询只读双保险）
1. **账号级**：`ecology_ro` 仅 `SELECT ecology_demo.*`（`scripts/setup_readonly_user.py` 创建，已验证写被拒）；
2. **应用级**（`app/agent/db_tool.py`）：仅 SELECT/WITH/SHOW/DESC/EXPLAIN 前缀、禁分号多语句、禁注释与危险函数、自动 `LIMIT 200`、10s 超时。

## 常用脚本速览
| 命令 | 用途 |
|---|---|
| `python tools/build_schema.py` | 模板变动/扩领域后重新生成 model/schema/docs（含 openpyxl 环境） |
| `python scripts/init_db.py [--drop]` | 建库建表（`--drop` 重建并清数据） |
| `python scripts/mock_data.py [--reset] [--seed N] [--dry-run]` | 灌 mock 数据 |
| `python scripts/setup_readonly_user.py` | 建只读账号并回填 `.env` |
| `python -m app.agent.cli` | CLI 问答（开发期工具，正式用 HTTP API） |

## 备注
- 数据表结构与字段类型由 Excel 模板生成，勿手改 `app/models/*.py`（改模板后重跑 build_schema）；
- `.env` 不入库；`docs/schema_manifest.json` 是字段字典与未来 LLM schema 上下文的唯一事实源；
- Agent 设计细节见 `docs/agent_design.md`。
