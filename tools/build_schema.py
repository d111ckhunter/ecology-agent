# -*- coding: utf-8 -*-
"""
Schema generator for the ecology-agent demo (水环境 + 水生生态).

Reads the canonical 3-row headers (english_code / chinese_meaning / description)
from every template xlsx under 01水环境 & 02水生生态, applies naming/type rules,
and emits:
  - docs/schema_manifest.json      (single source of truth, UTF-8)
  - docs/schema_report.md          (human/LLM readable audit)
  - app/models/water_env.py        (SQLAlchemy models, 水环境)
  - app/models/aqua_eco.py         (SQLAlchemy models, 水生生态)
  - app/schemas/water_env.py       (Pydantic v2 schemas, 水环境)
  - app/schemas/aqua_eco.py        (Pydantic v2 schemas, 水生生态)

Run with the BASE anaconda python (has openpyxl):  python tools/build_schema.py
"""
import os
import re
import json
import unicodedata

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# 1. Domain & table configuration
#    key: relative xlsx path (POSIX) -> (physical table name)
# ---------------------------------------------------------------------------
TABLES = [
    # ---------------- 01 水环境 ----------------
    ("01水环境/01水文情势/水文测站/水文情势测站信息表.xlsx", "hydro_station"),
    ("01水环境/01水文情势/水文测站/水文情势监测数据表.xlsx", "hydro_data"),
    ("01水环境/02地表水质/01在线监测/自动地表水水质测站信息表.xlsx", "auto_surface_water_station"),
    ("01水环境/02地表水质/01在线监测/自动地表水水质监测数据表.xlsx", "auto_surface_water_data"),
    ("01水环境/02地表水质/02人工监测/人工地表水水质测站信息表.xlsx", "manual_surface_water_station"),
    ("01水环境/02地表水质/02人工监测/人工地表水水质监测数据表.xlsx", "manual_surface_water_data"),
    ("01水环境/02地表水质/03底泥监测/沉积物测站信息表.xlsx", "sediment_station"),
    ("01水环境/02地表水质/03底泥监测/沉积物监测数据表.xlsx", "sediment_data"),
    ("01水环境/03水温监测/01水温监测站/自动水温测站信息表.xlsx", "auto_water_temp_station"),
    ("01水环境/03水温监测/01水温监测站/自动水温监测数据表.xlsx", "auto_water_temp_data"),
    ("01水环境/04地下水/01地下水水位监测站/自动地下水水位测站信息表.xlsx", "auto_groundwater_level_station"),
    ("01水环境/04地下水/01地下水水位监测站/自动地下水水位监测数据表.xlsx", "auto_groundwater_level_data"),
    ("01水环境/04地下水/02地下水水质/人工地下水水质测站信息表.xlsx", "manual_groundwater_quality_station"),
    ("01水环境/04地下水/02地下水水质/人工地下水水质监测数据表.xlsx", "manual_groundwater_quality_data"),
    # ---------------- 02 水生生态 ----------------
    ("02水生生态/01水生生境/01水生生境/生境监测数据表.xlsx", "habitat_monitor_data"),
    ("02水生生态/02水生生物/河段生物多样性数据表.xlsx", "reach_biodiversity_data"),
    ("02水生生态/02水生生物/河段生物调查数据表.xlsx", "reach_bio_survey_data"),
    ("02水生生态/03鱼类资源/01种类组成/鱼类物种表.xlsx", "fish_species"),
    ("02水生生态/03鱼类资源/02渔获物/渔获物数据表.xlsx", "fish_catch_data"),
    ("02水生生态/03鱼类资源/02渔获物/鱼类多样性信息表.xlsx", "fish_diversity_data"),
    ("02水生生态/03鱼类资源/03重要生境/鱼类三场.xlsx", "fish_grounds"),
    ("02水生生态/04补充/水生生态监测河段信息表.xlsx", "aqua_reach_info"),
    ("02水生生态/04补充/调查点位信息表.xlsx", "survey_point_info"),
]

# foreign keys: source file -> {column_original: (target_table, target_column)}
FKS = {
    "01水环境/01水文情势/水文测站/水文情势监测数据表.xlsx": {"station_code": ("hydro_station", "station_code")},
    "01水环境/02地表水质/01在线监测/自动地表水水质监测数据表.xlsx": {"station_code": ("auto_surface_water_station", "station_code")},
    "01水环境/02地表水质/02人工监测/人工地表水水质监测数据表.xlsx": {"station_code": ("manual_surface_water_station", "station_code")},
    "01水环境/02地表水质/03底泥监测/沉积物监测数据表.xlsx": {"station_code": ("sediment_station", "station_code")},
    "01水环境/03水温监测/01水温监测站/自动水温监测数据表.xlsx": {"station_code": ("auto_water_temp_station", "station_code")},
    "01水环境/04地下水/01地下水水位监测站/自动地下水水位监测数据表.xlsx": {"station_code": ("auto_groundwater_level_station", "station_code")},
    "01水环境/04地下水/02地下水水质/人工地下水水质监测数据表.xlsx": {"station_code": ("manual_groundwater_quality_station", "station_code")},
    "02水生生态/02水生生物/河段生物多样性数据表.xlsx": {"heduan_code": ("aqua_reach_info", "heduan_code")},
    "02水生生态/02水生生物/河段生物调查数据表.xlsx": {"heduan_code": ("aqua_reach_info", "heduan_code")},
    "02水生生态/03鱼类资源/02渔获物/渔获物数据表.xlsx": {
        "heduan_code": ("aqua_reach_info", "heduan_code"),
        "fish_code": ("fish_species", "fish_code"),
    },
    "02水生生态/03鱼类资源/02渔获物/鱼类多样性信息表.xlsx": {"fish_code": ("fish_species", "fish_code")},
}

# primary key column (original code) per file
PKS = {
    "01水环境/01水文情势/水文测站/水文情势测站信息表.xlsx": "station_code",
    "01水环境/02地表水质/01在线监测/自动地表水水质测站信息表.xlsx": "station_code",
    "01水环境/02地表水质/02人工监测/人工地表水水质测站信息表.xlsx": "station_code",
    "01水环境/02地表水质/03底泥监测/沉积物测站信息表.xlsx": "station_code",
    "01水环境/03水温监测/01水温监测站/自动水温测站信息表.xlsx": "station_code",
    "01水环境/04地下水/01地下水水位监测站/自动地下水水位测站信息表.xlsx": "station_code",
    "01水环境/04地下水/02地下水水质/人工地下水水质测站信息表.xlsx": "station_code",
    "02水生生态/03鱼类资源/01种类组成/鱼类物种表.xlsx": "fish_code",
    "02水生生态/03鱼类资源/03重要生境/鱼类三场.xlsx": "field_code",
    "02水生生态/04补充/水生生态监测河段信息表.xlsx": "heduan_code",
    "02水生生态/04补充/调查点位信息表.xlsx": "sp_code",
    # remaining (fact tables) use monitor_code
}

GREEK = {
    "α": "alpha", "β": "beta", "γ": "gamma", "δ": "delta", "ε": "epsilon",
    "Α": "alpha", "Β": "beta", "Γ": "gamma", "Δ": "delta",
}

# ---------------------------------------------------------------------------
# 2. naming helpers
# ---------------------------------------------------------------------------
def to_identifier(code):
    """sanitize an original header code into a valid snake_case identifier."""
    out = []
    for ch in code.strip():
        if ch.isascii() and (ch.isalnum() or ch == "_"):
            out.append(ch)
        elif ch in GREEK:
            out.append("_" + GREEK[ch])
        elif ch.isspace():
            out.append("_")
        else:
            name = unicodedata.name(ch, "")
            if "GREEK SMALL LETTER" in name or "GREEK CAPITAL LETTER" in name:
                out.append("_" + GREEK[ch.lower()])
            else:
                out.append("_")
    s = re.sub(r"_+", "_", "".join(out)).strip("_").lower()
    if not s:
        s = "col_unknown"
    if s[0].isdigit():
        s = "c_" + s
    return s

# python-keyword column names keep a python-safe attribute while the DB column
# keeps the original sanitized name.
#   鱼类物种表."class"(纲) -> klass ; 人工地表水水质监测数据表."as"(砷) -> ars
KEYWORDS = {"class": "klass", "as": "ars"}

def camel(name):
    return "".join(p.capitalize() for p in name.split("_"))

# ---------------------------------------------------------------------------
# 3. type rules
#    Returns one of ("String(64)","String(100)","String(128)","String(255)",
#                    "Text","DateTime","DECIMAL(x,y)","Integer")
# ---------------------------------------------------------------------------
# explicit string/text overrides (table file -> {original code: target type})
EXPLICIT = {
    "02水生生态/02水生生物/河段生物调查数据表.xlsx": {
        "mglatinm": "String(255)", "mgnm": "String(255)", "latinm": "String(255)", "chnm": "String(255)",
    },
    "02水生生态/03鱼类资源/01种类组成/鱼类物种表.xlsx": {
        "proty": "String(100)", "kindom": "String(100)", "class": "String(100)",
        "bio_order": "String(100)", "family": "String(100)", "genus": "String(100)",
        "species": "String(100)", "speciestpye": "String(100)", "protection_level": "String(100)",
        "endangered_status": "String(100)", "specificity": "String(100)",
        "appchara": "Text", "area": "Text", "internal": "Text",
        "food": "Text", "habits": "Text", "reproduction": "Text",
    },
    "02水生生态/03鱼类资源/02渔获物/渔获物数据表.xlsx": {
        "type": "String(100)", "length_range": "String(255)", "weight_range": "String(255)",
    },
    "02水生生态/03鱼类资源/02渔获物/鱼类多样性信息表.xlsx": {
        "div_description": "Text", "dif_description": "Text",
    },
    "02水生生态/03鱼类资源/03重要生境/鱼类三场.xlsx": {
        "type": "String(100)", "location": "String(255)", "species": "Text", "substrate": "Text",
    },
    "02水生生态/04补充/水生生态监测河段信息表.xlsx": {
        "type": "String(100)", "river": "String(255)",
    },
    "02水生生态/04补充/调查点位信息表.xlsx": {
        "type": "String(100)", "river": "String(255)",
    },
    "02水生生态/01水生生境/01水生生境/生境监测数据表.xlsx": {
        "ecogklocation": "String(255)", "ecogkbrief": "Text", "hedu_eco": "String(100)",
        "dzlxbrief": "String(255)", "dztzbrief": "Text", "wyyzk": "String(100)",
        "wzb": "Text", "rvltpj": "String(255)", "yatzh": "Text", "hctzh": "Text",
        "zrrkzg": "Text", "gytd": "Text", "pazbdyx": "String(255)", "abtdlylx": "String(255)",
    },
}

TEXT_WORDS = ["描述", "特征", "简介", "习性", "食性", "繁殖", "情况", "内容", "说明", "组成", "形态"]
STR_WORDS = ["名称", "位置", "河流", "河段", "类型", "属性", "状态", "级别", "等级", "地点", "地名", "拉丁", "评价"]

def infer_sql_type(table_file, code, meaning, desc):
    """primary decision: rules -> overrides -> patterns -> keywords -> DECIMAL default"""
    cl = code.strip().lower()
    if table_file in EXPLICIT and code in EXPLICIT[table_file]:
        return EXPLICIT[table_file][code]
    # time
    if cl in {"monitor_time", "tag_time_create", "tag_time_update"} or "time" in cl:
        return "DateTime"
    # coordinates / altitude
    if cl in {"longitude", "latitude", "tag_lon", "tag_lat", "start_longitude",
              "start_latitude", "end_longitude", "end_latitude"} or cl.endswith("_lon") or cl.endswith("_lat"):
        return "DECIMAL(10,6)"
    if cl in {"altitude", "tag_alt", "start_altitude", "end_altitude"} or "海拔" in meaning:
        return "DECIMAL(10,3)"
    # code / name / srs
    if cl.endswith("_code") or "_code" in cl:
        return "String(64)"
    if cl.endswith("_name") or "_name" in cl:
        return "String(255)"
    if "srs" in cl:
        return "String(128)"
    if cl == "type":
        return "String(100)"
    # counts: *_num
    if cl.endswith("_num") or cl.endswith("_count") or "尾数" in meaning or "物种数" in meaning:
        return "Integer"
    # ratio
    if "ratio" in cl or "比例" in meaning:
        return "DECIMAL(10,6)"
    # pH / water temperature / conductivity quick wins by chinese meaning
    if re.search(r"ph值?|pH值?", meaning):
        return "DECIMAL(5,2)"
    if "水温" in meaning:
        return "DECIMAL(6,2)"
    # descriptive text
    if any(w in meaning for w in TEXT_WORDS):
        return "Text"
    if any(w in meaning for w in STR_WORDS):
        return "String(255)"
    # everything else defaults to numeric measurement
    return "DECIMAL(14,4)"

# ---------------------------------------------------------------------------
# 4. parsing
# ---------------------------------------------------------------------------
from openpyxl import load_workbook

def parse_sheet(fullpath):
    """return (code_row, meaning_row, desc_row) as lists of strings for Sheet1."""
    wb = load_workbook(fullpath, read_only=True, data_only=True)
    try:
        ws = wb.worksheets[0]  # 模板固定第一张表为数据表
        rows = list(ws.iter_rows(values_only=True))
        if len(rows) < 3:
            raise ValueError("unexpected rows=%d" % len(rows))
        code_r, mean_r, desc_r = rows[0], rows[1], rows[2]
        code = [str(c).strip() if c is not None else "" for c in code_r]
        mean = [str(c).strip() if c is not None else "" for c in mean_r]
        desc = [str(c).strip() if c is not None else "" for c in desc_r]
        # extend to full length
        n = max(len(code), len(mean), len(desc))
        code += [""] * (n - len(code))
        mean += [""] * (n - len(mean))
        desc += [""] * (n - len(desc))
        return code, mean, desc
    finally:
        wb.close()

def build_manifest():
    manifest = []
    warnings = []
    for rel, tbl in TABLES:
        full = os.path.join(BASE, rel.replace("/", os.sep))
        chinese = os.path.splitext(os.path.basename(rel))[0]
        code, mean, desc = parse_sheet(full)
        pk_orig = PKS.get(rel) or "monitor_code"
        fks = FKS.get(rel, {})
        seen = {}
        cols = []
        for i, c in enumerate(code):
            if not c:
                continue
            meaning = mean[i]
            descr = desc[i]
            ident = to_identifier(c)
            attr = KEYWORDS.get(ident, ident)
            # de-dup (by db column name)
            base = ident
            k = 1
            while ident in seen:
                ident = "%s_%d" % (base, k)
                attr = "%s_%d" % (attr, k)
                k += 1
            seen[ident] = c
            if ident != c:
                warnings.append("[%s] column renamed %r -> %r (%s)" % (tbl, c, ident, meaning))
            sql_type = infer_sql_type(rel, c, meaning, descr)
            is_pk = (c == pk_orig)
            fk = None
            if c in fks:
                tgt_tbl, tgt_col = fks[c]
                fk = "%s.%s" % (tgt_tbl, to_identifier(tgt_col))
            cols.append({
                "original": c, "column": ident, "attr": attr, "chinese": meaning,
                "desc": descr, "sql_type": sql_type, "is_pk": is_pk, "fk": fk, "idx": i,
            })
        if pk_orig not in seen.values():
            warnings.append("[%s] PK %r not found in header!" % (tbl, pk_orig))
        manifest.append({
            "table": tbl, "table_chinese": chinese, "file": rel,
            "pk": pk_orig, "fks": {k: "%s.%s" % (v[0], v[1]) for k, v in fks.items()},
            "columns": cols,
        })
    return manifest, warnings

# ---------------------------------------------------------------------------
# 5. emit python code
# ---------------------------------------------------------------------------
def col_type_py(sql_type):
    if sql_type.startswith("String"):
        return "str"
    if sql_type == "Text":
        return "str"
    if sql_type == "DateTime":
        return "datetime"
    if sql_type == "Integer":
        return "int"
    return "Decimal"  # DECIMAL(x,y)

def emit_model(entry):
    cls = camel(entry["table"])
    lines = []
    lines.append('class %s(Base):' % cls)
    lines.append('    """%s (%s)"""' % (entry["table_chinese"], entry["table"]))
    lines.append('    __tablename__ = "%s"' % entry["table"])
    lines.append('    __table_args__ = {"comment": "%s"}' % entry["table_chinese"])
    lines.append("")
    for c in entry["columns"]:
        args = []
        t = c["sql_type"]
        attr = c.get("attr", c["column"])
        colname = c["column"]
        if c["is_pk"]:
            args.append("primary_key=True")
        args.append("nullable=" + ("False" if c["is_pk"] else "True"))
        if c["fk"]:
            args.insert(0, 'ForeignKey("%s")' % c["fk"])
        comment = c["chinese"] or c["original"]
        if c["is_pk"]:
            comment += "（主键）"
        if c["fk"]:
            comment += "（FK→%s）" % c["fk"]
        args.append('comment="%s"' % comment.replace('"', "\\\""))
        if attr != colname:
            lines.append('    %s = Column("%s", %s, %s)' % (attr, colname, t, ", ".join(args)))
        else:
            lines.append('    %s = Column(%s, %s)' % (colname, t, ", ".join(args)))
    lines.append("")
    return "\n".join(lines)

def emit_schema(entry, mode="out"):
    cls = camel(entry["table"])
    lines = []
    suffix = "" if mode == "out" else "Create"
    name = "%s%s" % (cls, suffix)
    lines.append('class %s(BaseModel):' % name)
    doc = "Read model for %s" if mode == "out" else "Create payload for %s"
    lines.append('    """%s"""' % (doc % entry["table_chinese"]))
    if mode == "out":
        lines.append('    model_config = ConfigDict(from_attributes=True)')
    lines.append("")
    for c in entry["columns"]:
        py = col_type_py(c["sql_type"])
        attr = c.get("attr", c["column"])
        ann = "Optional[%s]" % py
        req = c["is_pk"] and mode == "create"
        if req:
            lines.append('    %s: %s' % (attr, py))
        else:
            lines.append('    %s: %s = None' % (attr, ann))
    lines.append("")
    return "\n".join(lines)

# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    manifest, warnings = build_manifest()
    print("tables:", len(manifest))
    total = sum(len(e["columns"]) for e in manifest)
    print("total columns:", total)
    for w in warnings:
        print("WARN", w)

    docs_dir = os.path.join(BASE, "docs")
    os.makedirs(docs_dir, exist_ok=True)
    with open(os.path.join(docs_dir, "schema_manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)

    # split by domain
    def is_water(e):
        return e["table"] in {t for rel, t in TABLES if rel.startswith("01水环境")}

    water, aqua = [e for e in manifest if is_water(e)], [e for e in manifest if not is_water(e)]
    for pkg, group, outname in (("models", water, "water_env"), ("models", aqua, "aqua_eco"),
                                ("schemas", water, "water_env"), ("schemas", aqua, "aqua_eco")):
        d = os.path.join(BASE, "app", pkg)
        os.makedirs(d, exist_ok=True)

    def write_file(relp, content):
        p = os.path.join(BASE, relp)
        with open(p, "w", encoding="utf-8") as f:
            f.write(content)
        print("wrote", relp, len(content.splitlines()), "lines")

    # --- models ---
    for name, group in (("water_env", water), ("aqua_eco", aqua)):
        domain = "01水环境" if name == "water_env" else "02水生生态"
        header = (
            "# -*- coding: utf-8 -*-\n"
            '"""\n'
            "SQLAlchemy ORM models - %s. Auto-generated by tools/build_schema.py.\n"
            "Field types/comments derive from the source xlsx templates.\n"
            '"""\n'
            "from sqlalchemy import Column, DECIMAL, DateTime, ForeignKey, Integer, String, Text\n"
            "from app.models.base import Base\n\n"
        ) % domain
        body = "\n\n".join(emit_model(e) for e in group)
        write_file("app/models/%s.py" % name, header + body)

    # --- schemas ---
    for name, group in (("water_env", water), ("aqua_eco", aqua)):
        domain = "01水环境" if name == "water_env" else "02水生生态"
        header = (
            "# -*- coding: utf-8 -*-\n"
            '"""\n'
            "Pydantic v2 schemas - %s. Auto-generated by tools/build_schema.py.\n"
            '"""\n'
            "from datetime import datetime\n"
            "from decimal import Decimal\n"
            "from typing import Optional\n"
            "from pydantic import BaseModel, ConfigDict\n\n"
        ) % domain
        parts = []
        for e in group:
            parts.append(emit_schema(e, "create"))
            parts.append(emit_schema(e, "out"))
        write_file("app/schemas/%s.py" % name, header + "\n".join(parts))

    # --- report ---
    rep = ["# Schema Report（水环境 + 水生生态）", ""]
    for e in manifest:
        rep.append("## %s (`%s`)" % (e["table_chinese"], e["table"]))
        rep.append("来源: `%s` | 主键: `%s`" % (e["file"], e["pk"]))
        if e["fks"]:
            rep.append("外键: " + "; ".join("%s → %s" % kv for kv in e["fks"].items()))
        rep.append("")
        rep.append("| 列码 | 字段 | 中文 | 类型 | 主键 | 外键 | 说明 |")
        rep.append("|---|---|---|---|---|---|---|")
        for c in e["columns"]:
            rep.append("| %s | `%s` | %s | %s | %s | %s | %s |" % (
                c["original"], c["column"], c["chinese"], c["sql_type"],
                "Y" if c["is_pk"] else "", c["fk"] or "", c["desc"]))
        rep.append("")
    write_file("docs/schema_report.md", "\n".join(rep))

if __name__ == "__main__":
    main()
