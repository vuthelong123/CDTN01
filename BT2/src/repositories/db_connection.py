"""Quản lý kết nối cơ sở dữ liệu MySQL thông qua biến ngữ cảnh Flask `g`."""
import os

import mysql.connector
from dotenv import load_dotenv
from flask import g

# Đọc cấu hình từ file .env ở thư mục gốc BT2
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))


def connect():
    """Tạo kết nối mới đến MySQL Server."""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "warranty_db"),
        charset="utf8mb4",
        autocommit=False,
    )


def get_db():
    """Lấy kết nối hiện tại trong request context của Flask."""
    if "db" not in g:
        g.db = connect()
    return g.db


def close_db(_exc=None):
    """Đóng kết nối khi kết thúc request."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def query(sql, args=(), one=False):
    """Thực thi câu truy vấn SELECT và trả về dict."""
    cur = get_db().cursor(dictionary=True)
    cur.execute(sql, args)
    rows = cur.fetchall()
    cur.close()
    if one:
        return rows[0] if rows else None
    return rows


def execute(sql, args=()):
    """Thực thi INSERT / UPDATE / DELETE và trả về lastrowid."""
    cur = get_db().cursor()
    cur.execute(sql, args)
    last_id = cur.lastrowid
    cur.close()
    return last_id
