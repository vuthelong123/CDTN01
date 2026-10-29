Down file ở github về và giải nén

HƯỚNG DẪN TÁI TẠO DỰ ÁN

Cách 1: Chạy tự động bằng 1 cú click (Khuyên dùng trên Windows)
Chỉ cần vào thư mục `BT2` và click đúp vào file:
run.bat
(Script sẽ tự động cài đặt thư viện, chạy 34/34 Unit Tests và khởi động Web Server ngay lập tức).

Cách 2: Chạy bằng 3 câu lệnh thủ công trong Terminal / PowerShell
1. Mở terminal tại thư mục `BT2`:
   cd BT2
2. Cài đặt thư viện cần thiết:
   pip install -r requirements.txt
3. Chạy kiểm thử tự động (34 Unit Tests):
   pytest -v
   (Toàn bộ 34 test case đều PASSED ).
4. Khởi chạy ứng dụng Web:
   python src/main.py
   Hệ thống sẽ tự động tạo cơ sở dữ liệu `warranty.db` và nạp sẵn tài khoản mẫu.
5. Mở trình duyệt truy cập:
   http://127.0.0.1:5000

Danh sách tài khoản đăng nhập thử nghiệm (Mật khẩu chung: `123456`)
- Nhân viên tiếp nhận: tài khoản `nhanvientiepnhan` mật khẩu `123456` Tạo phiếu mới (UC01), Phân loại sự cố (UC02), Tra cứu khách hàng theo SĐT (US1-AC1)
- Quản trị viên: tài khoản `quantrivien` mật khẩu `123456` Tra cứu/Lọc danh sách phiếu (UC03), Phân công Kỹ thuật viên (UC04), Đóng phiếu bảo hành (UC07)
- Kỹ thuật viên 1: tài khoản `kythuatvien` mật khẩu `123456` Xem phiếu được phân công (UC05), Cập nhật tiến độ theo quy trình tuyến tính (UC06)
- Kỹ thuật viên 2: tài khoản `kythuatvien2` mật khẩu `123456` Kiểm tra phân quyền cách ly giữa các kỹ thuật viên khác nhau

Kết quả kiểm thử tự động (29 Unit Tests)
Lệnh thực thi:
pytest -v
Kết quả: 34 passed 
