# Agent 设计（v0.1，CLI 版）

生态监测数据问答 Agent —— 用户用自然语言提问，Agent 生成 SQL 查询只读库，
再把结果组织成自然语言回答。**首版交付 CLI**，接入点均为 FastAPI 友好设计，
后续可直接挂 API 层。

## 1. 目标与非目标

**目标**
- 支持"水环境 + 水生生态"23 张表的精确/聚合/跨表查询问题
  - 例：某站某指标历年趋势 / 某河段鱼类多样性 / 氨氮超标的站点 / 各河段物种数对比
- 数据永远只读（专用只读账号 + SQL 白名单双保险）
- 一次提问 → 自然语言回答（附 SQL 与执行摘要，方便复核）

**非目标（首版不做）**
- 不检索非结构化数据（08 目录），不做 RAG
- 不做写操作/多轮会话管理/流式输出（CLI 单轮问答即可）
- 不做严格 SQL 正确性评估框架（后续再加测试集）

## 2. 组件与职责

```
提问 ──► Agent(LLM 翻译官)
            ├ 1. 组装系统提示词 = schema 元数据 + 规则 + 示例
            ├ 2. chat → 产出 SQL (JSON 包裹，便于解析)
            ├ 3. 调用 DB Tool 执行
            ├ 4. 若 SQL 错误 → 把报错回喂 LLM 修正（≤2 次）
            └ 5. 把结果(行集/报错)再交 LLM → 自然语言回答
                      ▲
                      └ DB Tool：只读连接 + 护栏
```

| 模块 | 职责 | 关键设计 |
|---|---|---|
| `app/agent/schema.py` | 加载 schema 元数据 | 读 `docs/schema_manifest.json`，组装成给 LLM 的"表字典"（表名/中文/列/中文含义/类型/主外键），不读库 |
| `app/agent/llm.py` | DeepSeek 调用封装 | openai SDK，`base_url=https://api.deepseek.com/v1`，模型 `deepseek-v4-flash`，温度 0.1，key 从 `LLM_API_KEY` 读 |
| `app/agent/db_tool.py` | 只读 SQL 执行 | 用 `READONLY_DATABASE_URL`（ecology_ro）建独立 engine；护栏见 §4 |
| `app/agent/agent.py` | 编排循环 | 生成→执行→出错重试(≤2)→成稿；记录过程供 CLI 展示 |
| `app/agent/cli.py` | 命令行入口 | `python -m app.agent.cli`，交互式一问一答，`exit`/`quit` 退出；支持 `--question "…"` 单发模式 |

## 3. 提示词设计（text-to-SQL 成败核心）

**系统提示词 = 四段拼接：**

1. **身份与规则**（简短固定）
   - 你是生态监测数据库的 SQL 专家；只输出**只读 SELECT**；
   - 一律给列名加反引号（规避 `as`/`class` 等保留字列）；
   - 时间过滤用 `monitor_time`；数值不确定时给出上限约束；
   - 不确定表/列就说明"库中无对应字段"，禁止编造。

2. **Schema 字典**（来自 `schema_manifest.json`，量大按需精简）
   - 格式：`表名(中文) [注释]` → `列名 类型 · 中文含义`
   - 只带关键列可控制 token：默认全列，若超限则截断为"主键+外键+常用指标列"并注明省略；
   - 附带表间关联说明（station_code/heduan_code/fish_code 关系）。

3. **示例（few-shot，3~5 个与本 schema 强相关的问答→SQL）**
   - 例："长江某站2023年氨氮月均值" → 对应 SQL + 说明用了哪几张表；
   - few-shot 显著提升对列缩写的理解。

4. **输出协议**
   - 要求 LLM 输出 JSON：`{"sql": "...", "thinking": "..."}`
   - 便于程序可靠解析，避免夹带解释文字。

**二段提示词（结果→回答）**：把 `{原始问题, SQL, 行数, 前N行结果}` 交给 LLM，
要求：用中文回答、引用关键数值、结果为空时如实说明"未查询到"、不虚构。

## 4. 安全护栏（只读双保险）

**第一层 · 账号级**（已完成 ✅）
- `ecology_ro` 账号仅 `GRANT SELECT ON ecology_demo.*`，由
  `scripts/setup_readonly_user.py` 一键创建并回填 `.env`；已验证 INSERT 被拒(1142)。

**第二层 · 应用级（db_tool.py 内强制）**
- 仅允许单条语句：剥离首尾空白后必须以 `SELECT`/`WITH`/`SHOW`/`DESC`/`EXPLAIN` 开头；
- 含 `;` 多语句 / `INTO OUTFILE` / `SLEEP(` / 注释拼接等黑名单关键字 → 拒绝；
- 自动追加 `LIMIT {SQL_MAX_ROWS}`（默认 200），若原 SQL 已有 LIMIT 则取更小者；
- 执行包超时（10s）→ 超时即终止并提示；
- engine 只允许连接只读库，代码内不持有任何写凭据。

## 5. Agent 循环（agent.py 伪码）

```python
def answer(question: str) -> Answer:
    ctx = build_schema_context()              # §3.2
    for attempt in range(3):                  # 首次 + 2 次纠错
        sql = llm_generate_sql(ctx, question, error_hint=prev_error)
        if sql is None:
            return Answer(unsupported=...)    # LLM 明确表示库中无此数据
        result = execute_readonly(sql)        # db_tool，含护栏
        if result.ok:
            break
        prev_error = result.error             # 回喂 MySQL 报错
    return compose_answer(question, sql, result)
```

- 连续 3 次失败 → 返回"生成/执行失败 + 最近一次报错"，不硬编。
- `Answer` 记录：question / sql / rows / error / retries / answer_text。

## 6. CLI 使用方式（交付后）

```bash
# 交互式
python -m app.agent.cli
> 长江水系某测站2023年氨氮最高值出现在几月？

# 单发
python -m app.agent.cli --question "列出2024年鱼类多样性指数最高的3个河段"
```

依赖：fastapi 环境已具备 `openai==2.41.0`；只需在 `.env` 填 `LLM_API_KEY`。

## 7. 落地顺序（下一步代码实现）

1. `app/agent/schema.py` —— 读 manifest 出字典 + 关联说明
2. `app/agent/llm.py` —— DeepSeek chat 封装（JSON 输出解析）
3. `app/agent/db_tool.py` —— 只读执行 + 护栏（重点单测）
4. `app/agent/agent.py` —— 编排循环
5. `app/agent/cli.py` —— CLI 入口
6. 冒烟：无 key 时走"mock LLM"或打印待填提示；有 key 后跑 3~5 个典型问题

## 8. 验收样例（mock 数据里已埋好对应信号）

| 问题 | 预期行为 |
|---|---|
| 2023年水温最高的月份是？ | 趋势/季节信号 → 应答 7~8 月 |
| 哪个站点氨氮存在超标记录？ | spike 埋点（3~6 倍）→ 命中该站 |
| 各河段鱼类物种数对比 | join fish_catch_data ↔ aqua_reach_info |
| 某指标有缺测的数据点 | NULL 埋点 → 如实说明存在缺测 |
