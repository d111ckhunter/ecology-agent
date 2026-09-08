# -*- coding: utf-8 -*-
"""
Mock 数据生成器（demo：01水环境 + 02水生生态）

从 docs/schema_manifest.json 读取表结构，按"维度表 → 事实表"顺序生成并直接
写入 MySQL ecology_demo。特性：
  * 外键一致：事实表引用已插入的维度表主键；站名/河段名/鱼名从父行抄写
  * 语义真实：按列中文含义/类型套用合理取值区间与中文词池
  * 可复现：--seed 固定随机源
  * 可重置：--reset 先清空全部表再灌
  * 埋点样本：超标值 / 缺测(None) / 季节-趋势序列，便于日后验证 text-to-SQL

用法（fastapi conda 环境，项目根目录执行）:
    python scripts/mock_data.py                 # 生成并写入（seed=42）
    python scripts/mock_data.py --reset         # 先清空 23 张表再灌
    python scripts/mock_data.py --seed 7        # 换一个随机种子
    python scripts/mock_data.py --dry-run       # 只打印计划不写库
"""

import argparse
import datetime as dt
import json
import math
import os
import random
import sys

from sqlalchemy import create_engine, text

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from app.core.config import SQLALCHEMY_DATABASE_URL  # noqa: E402

MANIFEST = os.path.join(PROJECT_ROOT, "docs", "schema_manifest.json")

# ---------------------------------------------------------------------------
# 每张表生成规格
#   kind   : dim（维度表，count 行）/ fact（事实表）
#   count  : dim 行数
#   months : fact 的时间长度（每个主父表行生成 months 条月度记录）
#   prefix : 主键编码前缀
#   parents: {本表外键列: 父表名}，第一个为主父表（按行×月展开），其余为次父表（随机引用）
#   trend  : 随时间线性抬升的数值列名
#   spike  : 按"中文含义关键词"随机放大为超标值的列
# ---------------------------------------------------------------------------
SPECS = {
    # ---------------- 维度表 ----------------
    "hydro_station": dict(kind="dim", count=6, prefix="HS"),
    "auto_surface_water_station": dict(kind="dim", count=6, prefix="AS"),
    "manual_surface_water_station": dict(kind="dim", count=5, prefix="MS"),
    "sediment_station": dict(kind="dim", count=5, prefix="SD"),
    "auto_water_temp_station": dict(kind="dim", count=5, prefix="WT"),
    "auto_groundwater_level_station": dict(kind="dim", count=5, prefix="GL"),
    "manual_groundwater_quality_station": dict(kind="dim", count=5, prefix="GW"),
    "aqua_reach_info": dict(kind="dim", count=6, prefix="HD"),
    "fish_species": dict(kind="dim", count=14, prefix="F"),
    "survey_point_info": dict(kind="dim", count=6, prefix="SP"),
    "fish_grounds": dict(kind="dim", count=8, prefix="FG"),
    # ---------------- 事实表 ----------------
    "hydro_data": dict(
        kind="fact", months=24, prefix="MH",
        parents={"station_code": "hydro_station"},
        trend=("water_level",)),
    "auto_surface_water_data": dict(
        kind="fact", months=24, prefix="MA",
        parents={"station_code": "auto_surface_water_station"},
        trend=("tn", "nh3n"), spike=("高锰酸盐", "氨氮", "总氮")),
    "manual_surface_water_data": dict(
        kind="fact", months=18, prefix="MM",
        parents={"station_code": "manual_surface_water_station"},
        spike=("高锰酸盐", "氨氮", "总磷", "pH")),
    "sediment_data": dict(
        kind="fact", months=12, prefix="MD",
        parents={"station_code": "sediment_station"}),
    "auto_water_temp_data": dict(
        kind="fact", months=24, prefix="MT",
        parents={"station_code": "auto_water_temp_station"}),
    "auto_groundwater_level_data": dict(
        kind="fact", months=24, prefix="MG",
        parents={"station_code": "auto_groundwater_level_station"},
        trend=("water_level",)),
    "manual_groundwater_quality_data": dict(
        kind="fact", months=12, prefix="MW",
        parents={"station_code": "manual_groundwater_quality_station"},
        spike=("氨氮", "总硬度", "溶解性总固体")),
    "habitat_monitor_data": dict(kind="fact", months=12, prefix="HB"),
    "reach_biodiversity_data": dict(
        kind="fact", months=12, prefix="RB",
        parents={"heduan_code": "aqua_reach_info"}),
    "reach_bio_survey_data": dict(
        kind="fact", months=12, prefix="BS",
        parents={"heduan_code": "aqua_reach_info"}),
    "fish_catch_data": dict(
        kind="fact", months=12, prefix="FC",
        parents={"heduan_code": "aqua_reach_info", "fish_code": "fish_species"}),
    "fish_diversity_data": dict(
        kind="fact", months=1, prefix="FD",
        parents={"fish_code": "fish_species"}),
}

# 插入顺序：父表先于子表
ORDER = [
    # 维度
    "hydro_station", "auto_surface_water_station", "manual_surface_water_station",
    "sediment_station", "auto_water_temp_station", "auto_groundwater_level_station",
    "manual_groundwater_quality_station",
    "aqua_reach_info", "fish_species", "survey_point_info", "fish_grounds",
    # 事实
    "hydro_data", "auto_surface_water_data", "manual_surface_water_data",
    "sediment_data", "auto_water_temp_data", "auto_groundwater_level_data",
    "manual_groundwater_quality_data", "habitat_monitor_data",
    "reach_biodiversity_data", "reach_bio_survey_data", "fish_catch_data",
    "fish_diversity_data",
]

# ---------------------------------------------------------------------------
# 词池
# ---------------------------------------------------------------------------
RIVERS = ["长江", "黄河", "珠江", "松花江", "淮河", "钱塘江", "闽江", "澜沧江", "汉江", "岷江"]
REACHES = ["上游段", "中游段", "下游段", "入库段", "出库段", "坝上段", "坝下段", "城区段", "河口段", "支流段"]
LOCATIONS = ["某市城郊河段", "库区中泓", "工业园下游500m", "农业灌区排水口", "水库大坝上游", "河口右岸"]
BRIEFS = [
    "多年监测显示生态状况总体稳定", "受季节性水位波动影响明显", "水生植被覆盖良好，鱼类资源较丰富",
    "底质以砂砾为主，透明度较高", "受上游来水影响，汛期含沙量偏高", "生境完整性较好，人为干扰较小",
]
FISH_CN = ["草鱼", "鲢", "鳙", "鲤", "鲫", "青鱼", "鲶", "黄颡鱼", "鳜", "翘嘴鲌",
           "马口鱼", "赤眼鳟", "餐条", "麦穗鱼", "棒花鱼", "银鲴", "乌鳢", "鳊", "鲌", "黄鳝"]
FISH_LATIN = [
    "Ctenopharyngodon idella", "Hypophthalmichthys molitrix", "Aristichthys nobilis",
    "Cyprinus carpio", "Carassius auratus", "Mylopharyngodon piceus", "Silurus asotus",
    "Pelteobagrus fulvidraco", "Siniperca chuatsi", "Culter alburnus", "Hemiculter leucisculus",
    "Pseudorasbora parva", "Abbottina rivularis", "Xenocypris argentea", "Channa argus",
    "Parabramis pekinensis", "Opsariichthys bidens", "Squaliobarbus curriculus",
]
TAXON_MAP = {
    "proty": "动物界", "kindom": "脊索动物门", "class": "辐鳍鱼纲",
    "bio_order": ["鲤形目", "鲇形目", "鲈形目", "合鳃鱼目"],
    "family": ["鲤科", "鲿科", "鳢科", "鳜科", "鲌科"],
    "genus": ["草鱼属", "鲢属", "鳙属", "鲤属", "鲫属", "鲶属", "黄颡鱼属", "鳜属"],
}

# 中文含义关键词 -> (low, high)；量级按监测惯例，仅作 demo
NUMERIC_RANGES = {
    "ph值": (6.0, 9.0), "水温": (6.0, 28.0), "溶解氧": (3.0, 12.0), "浊度": (0.5, 60.0),
    "电导率": (80.0, 1200.0), "高锰酸盐指数": (0.5, 12.0), "化学需氧量": (4.0, 40.0),
    "五日生化需氧量": (0.5, 10.0), "氨氮": (0.02, 2.0), "总氮": (0.1, 4.0), "总磷": (0.005, 0.6),
    "石油类": (0.005, 0.5), "挥发酚": (0.0001, 0.01), "汞": (0.00001, 0.001),
    "铅": (0.0005, 0.05), "镉": (0.00005, 0.005), "铜": (0.001, 0.1), "锌": (0.005, 1.0),
    "氟化物": (0.05, 1.5), "砷": (0.0001, 0.05), "硒": (0.0001, 0.01),
    "氰化物": (0.001, 0.2), "硫化物": (0.002, 0.5), "阴离子表面活性剂": (0.01, 0.3),
    "粪大肠菌群": (20.0, 10000.0), "细菌总数": (50.0, 50000.0), "悬浮物": (2.0, 200.0),
    "流量": (10.0, 2500.0), "雨量": (0.0, 60.0), "水位": (0.0, 150.0), "埋深": (1.0, 50.0),
    "采样深度": (0.5, 40.0), "硫酸盐": (5.0, 250.0), "氯化物": (5.0, 300.0),
    "硝酸盐": (0.1, 10.0), "亚硝酸盐": (0.001, 1.0), "铁": (0.005, 2.0), "锰": (0.005, 1.5),
    "总硬度": (50.0, 500.0), "溶解性总固体": (100.0, 2000.0), "色度": (1.0, 25.0),
    "六价铬": (0.001, 0.1), "总铬": (0.001, 0.1), "铝": (0.01, 0.5), "钠": (5.0, 200.0),
    "镁": (1.0, 60.0), "钾": (0.5, 30.0), "钙": (5.0, 150.0), "钼": (0.0001, 0.01),
    "钴": (0.0001, 0.05), "铍": (0.00001, 0.002), "锑": (0.0001, 0.01), "钡": (0.01, 1.0),
    "钒": (0.001, 0.1), "铊": (0.00001, 0.0005), "钛": (0.001, 0.1), "镍": (0.001, 0.05),
    "碘化物": (0.001, 0.5), "总α放射性": (0.01, 0.5), "总β放射性": (0.05, 1.0),
    "盐度": (0.0, 2.5), "流速": (0.05, 3.0), "透明度": (0.2, 5.0),
    "面积": (0.05, 800.0), "长度": (0.5, 300.0), "宽度": (5.0, 2500.0), "深度": (0.3, 120.0),
    "海拔": (0.0, 3000.0), "经度": (97.0, 123.0), "纬度": (21.0, 47.0),
    "体长": (5.0, 120.0), "体重": (0.005, 20.0), "密度": (50.0, 200000.0),
    "生物量": (0.01, 500.0), "多样性指数": (0.1, 4.0), "比例": (0.001, 0.5),
}


def load_manifest():
    with open(MANIFEST, encoding="utf-8") as f:
        return json.load(f)


def table_cols(manifest, table):
    for e in manifest:
        if e["table"] == table:
            return e["columns"]
    raise KeyError(table)


class MockGen:
    def __init__(self, seed: int, dry: bool, reset: bool):
        self.rng = random.Random(seed)
        self.dry = dry
        self.reset = reset
        self.manifest = load_manifest()
        self.engine = None if dry else create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
        self.code_seq = {}
        self.parent_rows = {}  # 父表名 -> 行 dict（含主键与名字列）

    # ---------------- helpers ----------------
    def new_code(self, prefix: str) -> str:
        self.code_seq[prefix] = self.code_seq.get(prefix, 0) + 1
        return "%s%03d" % (prefix, self.code_seq[prefix])

    def pick(self, seq):
        return seq[self.rng.randrange(len(seq))]

    def make_time(self, year: int, month: int) -> dt.datetime:
        return dt.datetime(year, month, self.rng.randint(1, 28),
                           self.rng.randint(8, 18), self.rng.randint(0, 59))

    def range_for(self, chinese: str):
        for key, (lo, hi) in NUMERIC_RANGES.items():
            if key in chinese:
                return lo, hi
        return 0.001, 100.0

    # ---------------- value builders ----------------
    def text_value(self, col: dict) -> str:
        c = col.get("chinese", "")
        n = col["column"]
        if n == "fish_name":
            return self.pick(FISH_CN)
        if n in ("proty", "kindom", "class"):
            return TAXON_MAP[n]
        if n in ("bio_order", "family", "genus"):
            return self.pick(TAXON_MAP[n])
        if n == "species":
            return self.pick(FISH_CN)
        if n.endswith("_name") or n in ("station_name", "heduan_name", "sp_name", "eco_name", "field_name"):
            return "%s%s" % (self.pick(RIVERS), self.pick(REACHES))
        if n in ("river", "monitor_river") or "河流" in c:
            return self.pick(RIVERS)
        if n == "type" or "类型" in c or "属性" in c:
            return self.pick(["干流", "支流", "人工河道", "湖泊", "水库", "库湾"])
        if n == "tag_srs" or "坐标系" in c:
            return "CGCS2000"
        if "拉丁" in c:
            return self.pick(FISH_LATIN)
        if "位置" in c or n in ("location", "ecogklocation"):
            return self.pick(LOCATIONS)
        if "底质" in c:
            return self.pick(["砂质", "泥质", "砾石", "淤泥", "石质", "砂砾混合"])
        if "营养" in c:
            return self.pick(["贫营养", "中营养", "富营养", "中富营养"])
        if "保护" in c:
            return self.pick(["国家一级", "国家二级", "未列入"])
        if "濒危" in c:
            return self.pick(["极危", "濒危", "易危", "近危", "无危"])
        if "特有" in c:
            return self.pick(["长江特有", "地方特有", "非特有"])
        if "评价" in c:
            return self.pick(["连通性好", "连通性一般", "存在阻隔"])
        if "特征" in c or "形态" in c:
            return self.pick(["岸坡以自然土质为主", "河床砂砾石质", "人工护岸比例较高", "水生植物沿边带分布"])
        if "情况" in c:
            return self.pick(["无重大阻隔", "建有鱼道但过鱼效率一般", "自然河道无水利工程"])
        if "多样性" in c:
            return self.pick(["高", "中", "低"])
        return self.pick(BRIEFS)

    def numeric_value(self, col: dict, time_idx=None, trend=()) -> float | int:
        c = col.get("chinese", "")
        n = col["column"]
        sql = col["sql_type"]
        lo, hi = self.range_for(c)
        if sql == "Integer" or "物种数" in c or "尾数" in c or n.endswith("_num"):
            return self.rng.randint(int(lo), max(int(hi), int(lo) + 1))
        v = self.rng.uniform(lo, hi)
        # 季节波动（水温类）
        if time_idx is not None and ("水温" in c or n in ("wt", "wtemp", "wq")):
            mid = (lo + hi) / 2
            v = mid + (hi - lo) / 2 * math.sin(2 * math.pi * time_idx / 12.0 - math.pi / 2)
        # 趋势列随时间轻微抬升
        if time_idx is not None and n in trend:
            v += (hi - lo) * 0.04 * time_idx
        v = max(lo, min(hi * 1.5, v))
        return round(v, 4)

    def value_for(self, col: dict, time_idx=None, trend=()):
        sql = col["sql_type"]
        if sql == "DateTime":
            return self.make_time(self.rng.randint(2022, 2024), self.rng.randint(1, 12))
        if sql == "Text" or sql.startswith("String"):
            return self.text_value(col)
        return self.numeric_value(col, time_idx=time_idx, trend=trend)

    # ---------------- row assembly ----------------
    def assemble_row(self, table: str, spec: dict, time_idx=None,
                     parent_rows: dict | None = None) -> dict:
        """parent_rows: {本表外键列: 父行dict}，用于外键赋值 + 名字抄写。"""
        row = {}
        cols = table_cols(self.manifest, table)
        fk_ok = parent_rows or {}
        # 1) 主键
        for col in cols:
            if col.get("is_pk"):
                row[col["column"]] = self.new_code(spec.get("prefix", "X"))
        # 2) 外键 = 父行同名列
        for n, prow in fk_ok.items():
            row[n] = prow[n]
        # 3) 抄写父行中同名的"描述性列"（station_name / heduan_name / fish_name ...）
        for col in cols:
            n = col["column"]
            if n in row:
                continue
            for prow in fk_ok.values():
                if n in prow and prow[n] is not None:
                    row[n] = prow[n]
                    break
        # 4) 剩余列按规则生成
        for col in cols:
            n = col["column"]
            if n in row or n == "monitor_time":
                continue
            row[n] = self.value_for(col, time_idx=time_idx, trend=spec.get("trend", ()))
        return row

    # ---------------- main ----------------
    def run(self):
        total = 0
        if not self.dry:
            with self.engine.begin() as conn:
                if self.reset:
                    for t in reversed(ORDER):
                        conn.execute(text(f"DELETE FROM `{t}`"))
                    print("[reset] 已清空全部表")
            print("[info] 写入 MySQL 库 ecology_demo")
        for t in ORDER:
            spec = SPECS[t]
            cols = table_cols(self.manifest, t)
            pk_col = next(c["column"] for c in cols if c.get("is_pk"))
            rows = []
            if spec["kind"] == "dim":
                for _ in range(spec["count"]):
                    rows.append(self.assemble_row(t, spec))
            else:
                parents = spec.get("parents", {})
                months = spec.get("months", 12)
                if not parents:
                    for mi in range(months):
                        r = self.assemble_row(t, spec, time_idx=mi)
                        r["monitor_time"] = self.make_time(2023 + mi // 12, mi % 12 + 1)
                        rows.append(r)
                else:
                    # 主父表：逐行 × 逐月；次父表：每条记录随机引用
                    pnames = list(parents.values())
                    main_p = pnames[0]
                    for prow in self.parent_rows[main_p]:
                        for mi in range(months):
                            fk_map = {}
                            for fk, p in parents.items():
                                if p == main_p:
                                    fk_map[fk] = prow
                                else:
                                    fk_map[fk] = self.rng.choice(self.parent_rows[p])
                            r = self.assemble_row(t, spec, time_idx=mi, parent_rows=fk_map)
                            r["monitor_time"] = self.make_time(2023 + mi // 12, mi % 12 + 1)
                            rows.append(r)
            # 埋点
            self.inject_spikes(t, spec, rows)
            self.inject_missing(t, spec, rows)
            if rows:
                self._insert(t, rows)
                total += len(rows)
                if spec["kind"] == "dim":
                    self.parent_rows[t] = rows
            print("[%s] %-34s %5d rows" % ("dry-run" if self.dry else "ok", t, len(rows)))
        print("TOTAL mock rows:", total)

    # ---------------- 埋点 ----------------
    def inject_spikes(self, table: str, spec: dict, rows: list):
        if spec["kind"] != "fact" or not spec.get("spike") or not rows:
            return
        cols = table_cols(self.manifest, table)
        numerics = [c for c in cols if c["sql_type"].startswith("DECIMAL") and not c.get("is_pk")]
        if not numerics:
            return
        n = max(2, len(rows) // 12)
        for _ in range(n):
            r = self.rng.choice(rows)
            target = next((c for c in numerics
                           if any(k in c["chinese"] for k in spec["spike"])), None)
            target = target or self.rng.choice(numerics)
            if isinstance(r.get(target["column"]), (int, float)):
                r[target["column"]] = round(r[target["column"]] * self.rng.uniform(3.0, 6.0), 4)

    def inject_missing(self, table: str, spec: dict, rows: list):
        if spec["kind"] != "fact" or not rows:
            return
        cols = table_cols(self.manifest, table)
        numerics = [c["column"] for c in cols
                    if c["sql_type"].startswith("DECIMAL") and not c.get("is_pk")]
        if not numerics:
            return
        for r in rows:
            if self.rng.random() < 0.02:
                r[self.rng.choice(numerics)] = None

    # ---------------- persist ----------------
    def _insert(self, table: str, rows: list):
        if self.dry:
            return
        cols = table_cols(self.manifest, table)
        names = [c["column"] for c in cols]
        col_sql = ", ".join("`%s`" % n for n in names)
        val_sql = ", ".join(":" + n for n in names)
        with self.engine.begin() as conn:
            for r in rows:
                conn.execute(
                    text("INSERT INTO `%s` (%s) VALUES (%s)" % (table, col_sql, val_sql)),
                    {n: r.get(n) for n in names},
                )


def main():
    ap = argparse.ArgumentParser(description="ecology-agent mock 数据生成（01水环境+02水生生态）")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--reset", action="store_true")
    args = ap.parse_args()
    MockGen(seed=args.seed, dry=args.dry_run, reset=args.reset).run()


if __name__ == "__main__":
    main()
