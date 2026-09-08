# -*- coding: utf-8 -*-
"""
Read-only SQL execution tool with application-level guards.

双层防护：
  1) 账号级：使用 ecology_ro（仅 SELECT 权限），连接串来自
     app.core.config.READONLY_DATABASE_URL
  2) 应用级（本模块强制）：
     - 仅允许单条 SELECT / WITH / SHOW / DESC / EXPLAIN
     - 黑名单关键字（INTO OUTFILE / SLEEP( 等）直接拒绝
     - 自动追加 LIMIT（已有则取更小值），上限 SQL_MAX_ROWS
     - MySQL 侧超时 max_execution_time（秒级）
"""

import re
import time

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import READONLY_DATABASE_URL, SQL_MAX_ROWS, SQL_TIMEOUT_SECONDS

_ALLOWED_PREFIX = ("select", "with", "show", "desc", "describe", "explain")
_BLOCK_KEYWORDS = re.compile(
    r"\b(insert|update|delete|drop|alter|create|truncate|replace|grant|revoke|"
    r"rename|call|load\s+data|into\s+outfile|dumpfile|sleep\s*\(|benchmark\s*\(|"
    r"information_schema\.processlist)\b",
    flags=re.IGNORECASE | re.S,
)
_LIMIT_RE = re.compile(r"\blimit\s+(\d+)", flags=re.IGNORECASE)
# 注释（可被用来隐藏关键字/绕过检测），LLM 生成的 SQL 不应含注释
_COMMENT_RE = re.compile(r"(--|\#|/\*|\*/)")


class SQLGuardError(RuntimeError):
    pass


class SQLExecutionResult:
    def __init__(self, ok: bool, columns=None, rows=None, error: str = "",
                 elapsed: float = 0.0, truncated: bool = False):
        self.ok = ok
        self.columns = columns or []
        self.rows = rows or []
        self.error = error
        self.elapsed = elapsed
        self.truncated = truncated  # 是否因行数上限被截断

    def __repr__(self):
        if not self.ok:
            return "<SQLResult error=%r>" % self.error
        return "<SQLResult %d rows x %d cols>" % (len(self.rows), len(self.columns))


def guard_sql(raw_sql: str) -> str:
    """校验并规整 SQL；返回可直接执行的单条语句；非法则抛 SQLGuardError。"""
    if not raw_sql or not raw_sql.strip():
        raise SQLGuardError("SQL 为空")
    sql = raw_sql.strip()
    # 去尾部分号/空白
    sql = sql.rstrip("; \t\r\n")
    if ";" in sql:
        raise SQLGuardError("仅允许单条语句（不能包含分号/多语句）")
    first_word = sql.split(None, 1)[0].lower() if sql.split() else ""
    if first_word not in _ALLOWED_PREFIX:
        raise SQLGuardError("仅允许 SELECT/WITH/SHOW/DESC/EXPLAIN，收到: %r" % first_word)
    if _BLOCK_KEYWORDS.search(sql):
        raise SQLGuardError("SQL 包含被禁止的关键字/操作")
    if _COMMENT_RE.search(sql):
        raise SQLGuardError("SQL 不允许包含注释（-- / # / /* */）")
    # 自动 LIMIT
    m = _LIMIT_RE.search(sql)
    if m:
        user_limit = int(m.group(1))
        if user_limit > SQL_MAX_ROWS:
            sql = _LIMIT_RE.sub("LIMIT %d" % SQL_MAX_ROWS, sql, count=1)
    elif first_word != "show":  # SELECT/WITH/DESC/EXPLAIN 无 LIMIT 时追加
        sql = "%s LIMIT %d" % (sql, SQL_MAX_ROWS)
    return sql


class ReadonlyDBTool:
    def __init__(self):
        self.engine = create_engine(
            READONLY_DATABASE_URL,
            pool_pre_ping=True,
            pool_recycle=3600,
            echo=False,
        )

    def execute(self, raw_sql: str) -> SQLExecutionResult:
        start = time.time()
        try:
            sql = guard_sql(raw_sql)
        except SQLGuardError as e:
            return SQLExecutionResult(ok=False, error="护栏拒绝: %s" % e)
        try:
            # 会话级超时（MySQL 8 对 SELECT 生效），单位毫秒
            with self.engine.connect() as conn:
                conn.execute(
                    text("SET SESSION MAX_EXECUTION_TIME = %d"
                         % (SQL_TIMEOUT_SECONDS * 1000))
                )
                result = conn.execute(text(sql))
                columns = list(result.keys())
                fetched = result.fetchall()
            elapsed = time.time() - start
            truncated = len(fetched) > SQL_MAX_ROWS
            rows = [list(r) for r in fetched[:SQL_MAX_ROWS]]
            return SQLExecutionResult(
                ok=True, columns=columns, rows=rows,
                elapsed=round(elapsed, 3), truncated=truncated,
            )
        except SQLAlchemyError as e:
            elapsed = time.time() - start
            msg = str(e)
            # 提炼 MySQL 报错信息（pymysql 包裹在 cause 里）
            cause = getattr(e, "orig", None)
            if cause is not None:
                msg = str(cause)
            return SQLExecutionResult(ok=False, error=msg, elapsed=round(elapsed, 3))


if __name__ == "__main__":  # 自检护栏
    tool = ReadonlyDBTool()
    cases = [
        ("SELECT station_code, count(*) c FROM hydro_data GROUP BY station_code",
         "ok"),
        ("SELECT station_name FROM hydro_station WHERE station_code='HS001'",
         "ok"),
        ("DELETE FROM hydro_station", "deny"),
        ("SELECT * FROM hydro_station; DROP TABLE hydro_station", "deny"),
        ("SELECT SLEEP(5)", "deny"),
        ("SELECT * FROM hydro_station LIMIT 99999", "ok-truncated"),
    ]
    for sql, expect in cases:
        r = tool.execute(sql)
        print("%-70s -> ok=%s err=%s" % (sql[:68], r.ok, r.error[:60]))
    r = tool.execute("SELECT * FROM hydro_station")
    print("sample ok:", r.columns, len(r.rows), "truncated:", r.truncated)
