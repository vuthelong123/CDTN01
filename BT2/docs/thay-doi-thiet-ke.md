# BẢN GHI NHẬN THAY ĐỔI THIẾT KẾ (BT1 → BT2)

- **Học phần:** Chuyên đề tốt nghiệp 01 (CDTN01) - Track SE (Software Engineering)
- **Đề tài:** Hệ thống quản lý yêu cầu bảo hành (Luồng L2 - Service Desk)
- **Sinh viên thực hiện:** Vũ Thế Long - MSSV: 2374802010286

---

## 1. Lý do và Mục tiêu thay đổi
Trong Bài tập 1 (BT1), hệ thống đã xây dựng tài liệu đặc tả yêu cầu (SRS), mô hình cơ sở dữ liệu (ERD) và các bản vẽ thiết kế Use Case. Tuy nhiên, khi chuyển sang giai đoạn hiện thực mã nguồn và phát triển kiểm thử tự động ở Bài tập 2 (BT2), một số thiết kế ban đầu bộc lộ hạn chế cần được tái cấu trúc:
1. **Thiếu khả năng kiểm thử độc lập:** Logic nghiệp vụ ban đầu bị gắn chặt vào Framework giao diện (Flask routes) và truy vấn trực tiếp cơ sở dữ liệu MySQL, khiến việc viết Unit Test bắt buộc phải kết nối CSDL thật, dễ gây sai lệch dữ liệu và chạy chậm.
2. **Cơ chế xác thực chưa được mô hình hóa trong CSDL:** Bảng `employee` ở BT1 chỉ có thông tin định danh và vai trò, chưa có tài khoản và mật khẩu bảo mật.
3. **Quy tắc chuyển trạng thái cần làm chặt chẽ hơn:** Đảm bảo kỹ thuật viên tuân thủ nghiêm ngặt tiến trình xử lý sự cố từng bước một.

---

## 2. Bảng tổng hợp các thay đổi chính

| Thành phần | Thiết kế ở BT1 | Hiện thực thực tế ở BT2 | Lý do thay đổi & Lợi ích |
| :--- | :--- | :--- | :--- |
| **Kiến trúc mã nguồn** | Các route Flask vừa nhận request, vừa kiểm tra validation, vừa gọi SQL trực tiếp. | **Tách lớp 4 tầng chuẩn SE:**<br>- `routes/` (Presentation)<br>- `services/` (Business Logic)<br>- `validators/` (Validation)<br>- `repositories/` (Data Access) | Tách biệt trách nhiệm (SoC), mã nguồn module hóa, cho phép kiểm thử nghiệp vụ độc lập mà không cần khởi động server web. |
| **Kiểm thử tự động** | Chưa có kiểm thử tự động. | **Bộ Unit Test với Pytest:**<br>- Sử dụng `FakeTicketRepository` (in-memory)<br>- Bao phủ 3 nhóm: Happy path, Boundary (FR2), Invalid input. | Đảm bảo chất lượng mã nguồn, chạy 29/29 test pass chỉ trong ~0.05s mà không cần đụng đến database MySQL production. |
| **Bảng dữ liệu `employee`** | Chỉ gồm `employee_id`, `full_name`, `role`, `phone`, `is_active`. | **Bổ sung:**<br>- `username VARCHAR(50) UNIQUE`<br>- `password_hash VARCHAR(255)` | Hiện thực chức năng đăng nhập, phân quyền 3 vai trò theo SRS và bảo mật mật khẩu bằng thuật toán băm (Werkzeug hash). |
| **Luồng trạng thái KTV (QT-06)** | Cho phép chọn giữa các trạng thái kế tiếp trong danh sách. | **Khóa chặt tiến trình tuyến tính:**<br>`Đã phân công` → `Đang xử lý` → `Chờ linh kiện` → `Hoàn tất`. | Ngăn chặn kỹ thuật viên nhảy cóc trạng thái hoặc thao tác sai quy trình xử lý kỹ thuật. |
| **Giao diện hiển thị trạng thái** | Sử dụng badge trạng thái đơn lẻ. | **Thanh tiến trình (Stepper) 6 bước trực quan:**<br>`Mới` → `Đã phân công` → `Đang xử lý` → `Chờ linh kiện` → `Hoàn tất` → `Đã đóng`. | Giúp cả 3 vai trò (Tiếp nhận, Quản trị, Kỹ thuật) quan sát trực quan vị trí hiện tại của phiếu trong vòng đời SLA. |

---

## 3. Chi tiết kiến trúc tách lớp ở BT2 (Track SE)

```text
       [ Client / Trình duyệt ]
                  │  HTTP Request
                  ▼
     ┌────────────────────────┐
     │      src/routes/       │  Presentation Layer: Nhận request, quản lý session,
     │ (Flask Blueprints/View)│  trả về HTML / JSON.
     └───────────┬────────────┘
                 │
                 ▼
     ┌────────────────────────┐         ┌────────────────────────┐
     │     src/services/      │ ──────> │    src/validators/     │ Validation Layer:
     │    (Business Logic)    │         │ (Kiểm tra dữ liệu FR2, │ Chuẩn hóa SĐT (QT-02),
     └───────────┬────────────┘         │  QT-01, QT-02, SLA)    │ kiểm tra độ dài lỗi...
                 │
                 ▼ (Dependency Inversion)
     ┌────────────────────────┐
     │   src/repositories/    │  Data Access Layer:
     │ (Repository Interface) │  Đóng gói toàn bộ thao tác lưu trữ dữ liệu.
     └───────────┬────────────┘
                 │
        ┌────────┴──────────────────┐
        ▼                           ▼
┌─────────────────┐       ┌────────────────────────┐
│  MySQL Database │       │  FakeTicketRepository  │
│  (Môi trường    │       │  (Chạy trong RAM khi   │
│   thực thi app) │       │   chạy Unit Test)      │
└─────────────────┘       └────────────────────────┘
```

---

## 4. Tác động tới tài liệu và mã nguồn
- Bản vẽ kiến trúc thực tế được ghi nhận chi tiết tại [architecture-thuc-te.md](file:///c:/CDTN01/BT2/docs/architecture-thuc-te.md).
- Toàn bộ các yêu cầu chức năng (FR1 – FR8) và quy tắc nghiệp vụ (QT-01 – QT-06, QT-15) trong [srs.md](file:///c:/CDTN01/BT2/docs/srs.md) đều được đảm bảo vẹn toàn và phản ánh chính xác trong mã nguồn mới.
