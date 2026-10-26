# HỆ THỐNG QUẢN LÝ YÊU CẦU BẢO HÀNH

## 1. Thông tin đề tài

- **Tên đề tài:** Hệ thống quản lý yêu cầu bảo hành
- **Luồng:** L2 – Yêu cầu bảo hành (Service Desk)
- **Track:** SE – Software Engineering

## 2. Phạm vi

Hệ thống hỗ trợ tiếp nhận, phân loại, tra cứu, phân công kỹ thuật viên, theo dõi trạng thái và đóng phiếu bảo hành.

### Các vai trò chính

- Nhân viên tiếp nhận
- Quản trị viên
- Kỹ thuật viên

### Ngoài phạm vi

- Lịch hẹn kỹ thuật viên
- Quản lý kho linh kiện
- Thanh toán
- Bán hàng / cơ hội bán hàng
- Các luồng khác ngoài L2

## 3. Cấu trúc thư mục

```text
warranty-app/
├── app/
│   ├── app.py              # Routes Flask và điều phối giao diện
│   ├── ticket_service.py   # Lớp service nghiệp vụ (tách độc lập để unit test)
│   ├── repository.py       # Lớp tương tác MySQL
│   ├── db.py               # Kết nối CSDL MySQL
│   ├── init_auth.py        # Khởi tạo bảng xác thực và user mẫu
│   ├── requirements.txt    # Danh sách thư viện (Flask, MySQL, Pytest)
│   ├── static/             # CSS giao diện
│   └── templates/          # Jinja templates (3 vai trò + login)
├── tests/
│   ├── conftest.py         # Fake repository & fixtures trong bộ nhớ
│   └── test_ticket_service.py # Bộ unit test (Happy path, Boundary, Invalid input)
├── docs/
│   ├── srs.md
│   ├── test-results.txt    # Kết quả chạy test thực tế
│   ├── architecture.drawio
│   ├── usecase.drawio
│   └── erd.drawio
├── db/
│   ├── schema.sql
│   └── seed.sql
└── pytest.ini              # Cấu hình đường dẫn test và module
```

## 4. Hướng dẫn chạy Unit Test

Cài đặt thư viện:
```bash
pip install -r app/requirements.txt
```

Chạy toàn bộ unit test bằng 1 lệnh:
```bash
pytest -q
```
hoặc hiển thị chi tiết từng test:
```bash
pytest -v
```
Toàn bộ test chạy trên `FakeTicketRepository` (in-memory mock repository), hoàn toàn không phụ thuộc và không tác động đến cơ sở dữ liệu thật.

