"""Script khởi tạo cột tài khoản và mật khẩu cho bảng employee (chạy một lần)."""
import os
import sys

from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

sys.path.insert(0, os.path.dirname(__file__))
from repositories import connect

sys.stdout.reconfigure(encoding="utf-8")
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

DEFAULT_PASSWORD = "123456"
SEED_USERNAMES = {1: "nhanvientiepnhan", 2: "quantrivien", 3: "kythuatvien", 4: "kythuatvien2"}


def column_exists(cur, name):
    cur.execute(
        "SELECT COUNT(*) FROM information_schema.COLUMNS "
        "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'employee' AND COLUMN_NAME = %s",
        (name,),
    )
    return cur.fetchone()[0] > 0


def main():
    conn = connect()
    cur = conn.cursor()

    if not column_exists(cur, "username"):
        cur.execute("ALTER TABLE employee ADD COLUMN username VARCHAR(50) NULL UNIQUE")
        print("Đã thêm cột employee.username")
    if not column_exists(cur, "password_hash"):
        cur.execute("ALTER TABLE employee ADD COLUMN password_hash VARCHAR(255) NULL")
        print("Đã thêm cột employee.password_hash")

    cur.execute("SELECT employee_id FROM employee WHERE username IS NULL OR password_hash IS NULL")
    for (emp_id,) in cur.fetchall():
        username = SEED_USERNAMES.get(emp_id, f"nv{emp_id}")
        cur.execute(
            "UPDATE employee SET username = COALESCE(username, %s), password_hash = %s "
            "WHERE employee_id = %s",
            (username, generate_password_hash(DEFAULT_PASSWORD), emp_id),
        )
        print(f"Đã tạo tài khoản: {username}")

    for emp_id, username in SEED_USERNAMES.items():
        cur.execute("UPDATE employee SET username = %s WHERE employee_id = %s", (username, emp_id))

    conn.commit()
    conn.close()
    print("Khởi tạo tài khoản thành công.")


if __name__ == "__main__":
    main()
