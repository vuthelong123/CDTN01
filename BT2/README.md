# HỆ THỐNG QUẢN LÝ YÊU CẦU BẢO HÀNH (BÀI TẬP 2 - TRACK SE)

- **Đề tài:** Hệ thống quản lý yêu cầu bảo hành
- **Luồng:** L2 – Yêu cầu bảo hành (Service Desk - Smart CRM Mekong Mobile)
- **Track:** SE – Software Engineering
- **Sinh viên:** Vũ Thế Long - MSSV: 2374802010286

---

## 1. Cấu trúc thư mục chuẩn Track SE

```text
BT2/
├── docs/                      # Tài liệu đồ án
│   ├── srs.md                 # Đặc tả yêu cầu phần mềm (kế thừa từ BT1)
│   ├── thay-doi-thiet-ke.md   # Ghi nhận các thay đổi thiết kế từ BT1 sang BT2
│   ├── ai-disclosure.md       # Bảng kê khai sử dụng công cụ AI
│   ├── architecture-thuc-te.md # Tài liệu mô tả kiến trúc đã hiện thực
│   └── architecture-thuc-te.drawio # Sơ đồ kiến trúc thực tế (Draw.io)
│
├── src/                       # Mã nguồn hệ thống (TÁCH LỚP CHUẨN SE)
│   ├── routes/                # 1. Lớp điều phối giao diện / HTTP routes (Blueprints)
│   │   ├── auth_routes.py     # Đăng nhập, đăng xuất, phân quyền vai trò
│   │   ├── reception_routes.py# Giao diện Nhân viên tiếp nhận (UC01, UC02)
│   │   ├── admin_routes.py    # Giao diện Quản trị viên (UC03, UC04, UC07)
│   │   └── tech_routes.py     # Giao diện Kỹ thuật viên (UC05, UC06)
│   │
│   ├── services/              # 2. Lớp nghiệp vụ cốt lõi (Business Domain Logic)
│   │   └── ticket_service.py  # Xử lý quy tắc nghiệp vụ L2, tính SLA, transaction
│   │
│   ├── validators/            # 3. Lớp kiểm tra tính hợp lệ dữ liệu
│   │   └── ticket_validator.py# Ràng buộc FR2 (>=10 ký tự), QT-02 (chuẩn hóa SĐT)
│   │
│   ├── repositories/          # 4. Lớp truy cập cơ sở dữ liệu (Data Access Layer)
│   │   ├── db_connection.py   # Quản lý kết nối MySQL qua ngữ cảnh Flask
│   │   └── ticket_repository.py # MySQLTicketRepository (triển khai SQL)
│   │
│   ├── static/                # Tài nguyên giao diện (CSS phong cách Dark Mode kính mờ)
│   │   └── style.css
│   ├── templates/             # Giao diện Jinja2 (HTML5 ngữ nghĩa, responsive)
│   │   ├── base.html
│   │   ├── _macros.html
│   │   ├── login.html
│   │   ├── reception.html
│   │   ├── admin.html
│   │   └── technician.html
│   ├── main.py                # Entrypoint khởi chạy ứng dụng Flask
│   └── init_auth.py           # Khởi tạo dữ liệu người dùng ban đầu
│
├── tests/                     # 5. Bộ kiểm thử tự động (Unit Tests)
│   ├── conftest.py            # Fixtures & FakeTicketRepository (chạy trên RAM)
│   └── test_ticket_service.py # 29 test cases: Happy path, Boundary, Invalid input
│
├── sql/                       # Kịch bản cơ sở dữ liệu
│   ├── schema.sql             # Cấu trúc bảng MySQL 8.0 (6 bảng)
│   └── seed.sql               # Dữ liệu khởi tạo mẫu
│
├── .env                       # Biến môi trường kết nối MySQL Server
├── pytest.ini                 # Cấu hình testpaths và pythonpath
└── requirements.txt           # Danh mục thư viện phụ thuộc
```

---

## 2. Hướng dẫn chạy Unit Test

1. Mở Terminal / PowerShell và chuyển vào thư mục `BT2`:
   ```bash
   cd c:\CDTN01\BT2
   ```

2. Cài đặt các thư viện cần thiết:
   ```bash
   pip install -r requirements.txt
   ```

3. Chạy toàn bộ 29 Unit Tests bằng 1 lệnh:
   ```bash
   pytest -v
   ```
   *(Toàn bộ test sử dụng `FakeTicketRepository` in-memory, hoàn toàn không phụ thuộc và không tác động đến database MySQL production).*

---

## 3. Hướng dẫn chạy ứng dụng Web

1. Đảm bảo MySQL Service đang hoạt động (Port 3306):
   ```powershell
   net start MYSQL80
   ```
2. Khởi chạy server Flask:
   ```bash
   python src/main.py
   ```
3. Truy cập trên trình duyệt: `http://127.0.0.1:5000`

### Danh sách tài khoản thử nghiệm (Mật khẩu: `123456`)
- **Nhân viên tiếp nhận:** `nhanvientiepnhan`
- **Quản trị viên:** `quantrivien`
- **Kỹ thuật viên:** `kythuatvien` (hoặc `kythuatvien2`)
