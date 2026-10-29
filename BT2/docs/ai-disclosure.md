# BẢNG KHAI BÁO SỬ DỤNG CÔNG CỤ TRÍ TUỆ NHÂN TẠO (AI DISCLOSURE)

- **Học phần:** Chuyên đề tốt nghiệp 01 (CDTN01) - Track SE (Software Engineering)
- **Bài tập:** Bài tập 2 (BT2) - Hiện thực mã nguồn và Kiểm thử đơn vị
- **Sinh viên thực hiện:** Vũ Thế Long - MSSV: 2374802010286

---

## Bảng kê khai chi tiết

| Công cụ AI | Nội dung áp dụng | Phần áp dụng trong đồ án | Cách thức sinh viên kiểm chứng & làm chủ |
| :--- | :--- | :--- | :--- |
| **Antigravity / ChatGpt** | Gợi ý cấu trúc tách lớp phần mềm theo chuẩn Software Engineering (SE): phân chia trách nhiệm giữa `routes`, `services`, `repositories`, `validators`. | Mã nguồn thư mục `src/` | Sinh viên trực tiếp rà soát từng module, đảm bảo tính đóng gói: Service không bị dính mã nguồn Flask hay câu lệnh SQL thuần; Repository tuân thủ Dependency Inversion. |
| **Antigravity / ChatGpt** | Gợi ý bộ khung Unit Test sử dụng thư viện `pytest` và thiết kế mẫu kho dữ liệu giả lập (`FakeTicketRepository` in-memory snapshot/rollback). | Thư mục `tests/` (`conftest.py`, `test_ticket_service.py`) | Sinh viên tự kiểm tra đối chiếu từng test case với tài liệu SRS: đảm bảo đủ 3 nhóm bắt buộc (Happy Path, Boundary 10 ký tự theo FR2, Invalid Input). Tự chạy lệnh `pytest -v` trên Terminal và kiểm chứng 29/29 test pass. |
| **Antigravity / ChatGpt** | Hỗ trợ chuẩn hóa các hàm tiện ích nghiệp vụ: chuẩn hóa số điện thoại 10 số (QT-02), thuật toán tính hạn cam kết SLA bỏ qua ngày Chủ Nhật (QT-04). | `src/validators/`, `src/services/` | Sinh viên tự viết các ca kiểm thử biên (Boundary test) và kiểm thử ngày rơi vào cuối tuần để xác minh thuật toán tính toán chính xác 100%. |
| **Không sử dụng AI (Tự làm)** | - Thiết kế giao diện (HTML/CSS) theo phong cách Dark Mode kính mờ (Glassmorphism).<br>- Phân bổ Use Case và vai trò người dùng theo đề tài L2.<br>- Cài đặt và cấu hình cơ sở dữ liệu MySQL 8.0 trên môi trường Windows. | `src/templates/`, `src/static/`, `sql/` | Sinh viên tự thiết kế bố cục, kiểm tra giao diện trực tiếp trên trình duyệt web tại cổng `127.0.0.1:5000` và kiểm tra dữ liệu trong MySQL Workbench. |

---

## Cam kết của sinh viên
-Tôi cam kết việc sử dụng các công cụ AI trong quá trình thực hiện dự án đã được trình bày trung thực trong phụ lục này. Tôi chịu trách nhiệm về nội dung của bảng, đã kiểm chứng phần AI hỗ trợ.
-Họ và tên: Vũ Thế Long
-MSSV: 2374802010286
-Ngày: 28/10/2026

