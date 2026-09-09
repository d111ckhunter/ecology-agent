# -*- coding: utf-8 -*-
"""
Schema context builder for text-to-SQL.

Reads docs/schema_manifest.json (single source of truth emitted by
tools/build_schema.py) and renders a compact "table dictionary" that is fed
to the LLM inside the system prompt, plus human table-relation notes.

Everything here works off the manifest file - never queries the database.
"""

import json
import os
from functools import lru_cache

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_MANIFEST = os.path.join(_PROJECT_ROOT, "docs", "schema_manifest.json")

# manifest column keys we care about
_KEEP = ("original", "column", "chinese", "sql_type", "is_pk")


@lru_cache(maxsize=1)
def load_manifest() -> list[dict]:
    with open(_MANIFEST, encoding="utf-8") as f:
        return json.load(f)


def _short_type(sql_type: str) -> str:
    """manifest 里的 DECIMAL(x,y)/String(n)/Text/DateTime/Integer 缩写."""
    if sql_type.startswith("DECIMAL"):
        return "num"
    if sql_type == "Integer":
        return "int"
    if sql_type == "DateTime":
        return "datetime"
    if sql_type == "Text":
        return "text"
    # String(n)
    return "str"


def build_schema_text() -> str:
    """
    Render 全部 23 张表为可投喂 LLM 的字典文本。

    格式（每表）：
    [表名] 中文表名 (来源模板: xx.xlsx, 主键: xxx)
    - 外键: station_code -> hydro_station.station_code
    - 列: 列名 [类型] 中文含义
    """
    manifest = load_manifest()
    lines = []
    for entry in manifest:
        tbl = entry["table"]
        chinese = entry["table_chinese"]
        pk = entry["pk"]
        lines.append("### 表 %s （%s） 主键: %s" % (tbl, chinese, pk))
        # relations
        rels = []
        for col in entry["columns"]:
            if col.get("fk"):
                rels.append("%s -> %s" % (col["column"], col["fk"]))
        if rels:
            lines.append("   外键: " + " ; ".join(rels))
        for col in entry["columns"]:
            name = col["column"]
            typ = _short_type(col["sql_type"])
            cmean = col.get("chinese", "") or col.get("original", "")
            cmean = cmean.replace("（主键）", "").replace("（FK", "（FK")  # 无操作，防御
            tag = " PK" if col.get("is_pk") else ""
            lines.append("   - %s [%s]%s %s" % (name, typ, tag, cmean))
        lines.append("")
    return "\n".join(lines)


def build_relation_notes() -> str:
    """仅提取表间关联说明（用于回答“哪些表怎么连”）."""
    manifest = load_manifest()
    lines = ["表间关联（外键关系）:"]
    for entry in manifest:
        for col in entry["columns"]:
            if col.get("fk"):
                lines.append("  %s.%s → %s" % (entry["table"], col["column"], col["fk"]))
    return "\n".join(lines)


def compact_tables(max_tables: int | None = None) -> list[dict]:
    """结构化的精简表清单，供程序侧使用（如展示支持哪些表）。"""
    manifest = load_manifest()
    if max_tables:
        manifest = manifest[:max_tables]
    out = []
    for entry in manifest:
        out.append({
            "table": entry["table"],
            "chinese": entry["table_chinese"],
            "pk": entry["pk"],
            "n_columns": len(entry["columns"]),
        })
    return out


if __name__ == "__main__":  # 快速自检
    txt = build_schema_text()
    print("schema text length:", len(txt), "chars")
    print(txt[:1200])
