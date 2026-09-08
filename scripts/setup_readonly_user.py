# -*- coding: utf-8 -*-
"""
创建 MySQL 只读账号 ecology_ro（仅 SELECT ecology_demo），并把凭据写入 .env。

用法: python scripts/setup_readonly_user.py
"""
import os
import secrets
import string
import sys

import pymysql

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(PROJECT_ROOT, ".env")

ADMIN = dict(host="127.0.0.1", port=3307, user="root", password="123456")
RO_USER = "ecology_ro"
RO_HOSTS = ["localhost", "127.0.0.1"]
DB_NAME = "ecology_demo"


def gen_password(n=20):
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(n))


def load_env(path):
    env = {}
    if os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            env[k.strip()] = v.strip()
    return env


def main():
    pw = gen_password()
    conn = pymysql.connect(**ADMIN)
    cur = conn.cursor()
    try:
        # 每次重建，保证密码与权限幂等
        for h in RO_HOSTS:
            cur.execute("DROP USER IF EXISTS %s@%s", (RO_USER, h))
            cur.execute("CREATE USER %s@%s IDENTIFIED BY %s", (RO_USER, h, pw))
            cur.execute("GRANT SELECT ON `%s`.* TO %s@%s" % (DB_NAME, RO_USER, h))
        conn.commit()
        print("[ok] 已创建只读账号 %s (仅 SELECT %s.*)" % (RO_USER, DB_NAME))
    finally:
        conn.close()

    # 写 .env（保留原内容，仅更新/追加 DB_RO_*）
    env = load_env(ENV_PATH)
    env["DB_RO_HOST"] = env.get("DB_RO_HOST", "127.0.0.1")
    env["DB_RO_PORT"] = env.get("DB_RO_PORT", "3307")
    env["DB_RO_USER"] = RO_USER
    env["DB_RO_PASSWORD"] = pw
    env["DB_RO_NAME"] = env.get("DB_RO_NAME", DB_NAME)
    lines = []
    for k, v in env.items():
        lines.append("%s=%s" % (k, v))
    with open(ENV_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("[ok] 已更新 .env（DB_RO_USER=%s）" % RO_USER)

    # 自测：只读连接可 SELECT；INSERT 应被拒绝
    try:
        ro = pymysql.connect(host=env["DB_RO_HOST"], port=int(env["DB_RO_PORT"]),
                             user=RO_USER, password=pw, database=DB_NAME)
        rc = ro.cursor()
        rc.execute("SELECT count(*) FROM hydro_station")
        print("[ok] 只读 SELECT 成功, hydro_station 行数 =", rc.fetchone()[0])
        try:
            rc.execute("INSERT INTO hydro_station (station_code) VALUES ('X-TEST')")
            ro.commit()
            print("[warn] INSERT 未被拒绝 —— 权限异常！")
        except pymysql.err.OperationalError as e:
            print("[ok] INSERT 已被拒绝:", e.args[0])
        ro.close()
    except Exception as e:
        print("[fail] 只读自测失败:", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
