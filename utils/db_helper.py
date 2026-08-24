"""
数据库校验辅助（P3 高级项）

说明：
    - 真实企业项目中，订单创建后往往需要在数据库层做二次校验
      （UI 显示成功 ≠ 数据真正落库）。
    - 本演示项目使用的是公开练习站点，无法直连其数据库，
      因此这里提供一个「标准实现 + 可跳过」的模块：
        * 从 config 读取 database 配置；
        * 若未配置（默认留空），相关用例通过 pytest.skip 自动跳过，
          保证整套用例在缺库环境下依然可运行；
        * 接入真实数据库后，取消配置即可启用数据库断言。

技术栈：PyMySQL（已列入 requirements.txt）
"""

import pymysql

from utils.config_reader import load_config


def get_db_config():
    """从环境配置中读取 database 段。"""
    cfg = load_config()
    return cfg.get("database", {}) or {}


def is_db_configured() -> bool:
    """数据库是否已配置（host / user / password 均非空才视为可用）。"""
    db = get_db_config()
    return bool(
        db.get("host")
        and db.get("user") is not None
        and db.get("password") is not None
        and db.get("database")
    )


def query_order(order_id):
    """
    按订单 id 查询订单记录。
    返回单行记录（dict）；未找到返回 None。
    """
    db = get_db_config()
    conn = pymysql.connect(
        host=db["host"],
        user=db["user"],
        password=str(db["password"]),
        database=db["database"],
        port=int(db.get("port", 3306)),
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=10,
    )
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM orders WHERE id = %s",
                (order_id,),
            )
            return cur.fetchone()
    finally:
        conn.close()


def order_exists(order_id) -> bool:
    """订单记录是否存在（数据库校验入口）。"""
    return query_order(order_id) is not None
