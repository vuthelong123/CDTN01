MỤC 1 – BẢN SRS RÚT GỌN
1.1. Giới thiệu và phạm vi
Bối cảnh: Luồng L2 của Smart CRM – Mekong Mobile tập trung vào việc tiếp nhận và xử lý yêu cầu bảo hành. Hệ thống hỗ trợ ghi nhận, phân loại, phân công, theo dõi trạng thái và đóng phiếu bảo hành.
Phạm vi: Nhân viên tiếp nhận tạo, phân loại yêu cầu bảo hành, quản trị viên gán kỹ thuật viên xử lý, sau đó kỹ thuật viên cập nhật trạng thái cho đến khi yêu cầu được hoàn thành, đóng yêu cầu.
Điều không làm: lịch hẹn kỹ thuật viên; kho linh kiện; thanh toán; bán hàng/cơ hội bán hàng; các luồng khác ngoài L2.
Bảng thuật ngữ:
Thuật ngữ
Định nghĩa
Tên kỹ thuật gợi ý
Khách hàng
Cá nhân đã mua ít nhất một sản phẩm hoặc sử dụng dịch vụ của Mekong Mobile.
customer
Thiết bị
Một máy cụ thể mà khách hàng sở hữu, xác định bằng số serial hoặc IMEI.
device
Phiếu bảo hành
Một yêu cầu bảo hành hoặc sửa chữa được ghi nhận, có mã duy nhất và vòng đời trạng thái.
ticket
Trạng thái phiếu
Vị trí hiện tại của phiếu trong vòng đời: Mới → Đã phân công → Đang xử lý → Chờ linh kiện → Hoàn tất → Đã đóng.
ticket_status
Hạn cam kết (SLA)
Thời điểm chậm nhất phải hoàn tất phiếu, tính từ lúc tiếp nhận theo mức ưu tiên.
due_date
Nhóm sự cố
Phân loại nguyên nhân bảo hành: màn hình, pin, sạc, phần mềm, nước vào, khác.
issue_category
Mức ưu tiên
Mức khẩn của phiếu: Cao, Trung bình, Thấp. Quyết định hạn cam kết.
priority
Kỹ thuật viên
Nhân viên thực hiện sửa chữa, có danh sách tay nghề và địa bàn làm việc.
technician



1.2. Các bên liên quan và vai trò
Actor
Được làm
Không được làm
Nhân viên tiếp nhận
Tạo, phân loại phiếu bảo hành.
Không phân công kỹ thuật viên, không đóng phiếu.
Quản trị viên
Tra cứu, phân công, đóng phiếu.
Không cập nhật xử lý thay kỹ thuật viên trong phạm vi này.
Kỹ thuật viên
Xem phiếu được phân công, cập nhật trạng thái.
Không tự phân công lại phiếu.

1.3. User Story và MoSCoW
Mã
User Story
MoSCoW
Tiêu chí chấp nhận
US1
Là nhân viên tiếp nhận, tôi muốn tạo phiếu bảo hành chỉ bằng số điện thoại khách để không phải nhập lại thông tin khách đã có trong hệ thống.
MUST
AC1. GIVEN số điện thoại 0843310647 đã có trong hệ thống, WHEN nhân viên nhập số này vào ô tìm khách, THEN hệ thống tự điền tên, địa chỉ và lịch sử mua hàng của khách đó.

AC2. GIVEN số điện thoại chưa có trong hệ thống, WHEN nhân viên nhập số này, THEN hệ thống mở form tạo khách hàng mới với số điện thoại đã điền sẵn.

AC3. GIVEN nhân viên chưa nhập mô tả lỗi, WHEN bấm Lưu phiếu, THEN hệ thống từ chối lưu và hiển thị thông báo nêu rõ trường còn thiếu.
US2
Là nhân viên tiếp nhận, tôi muốn phân loại phiếu bảo hành để xác định loại yêu cầu và mức độ xử lý phù hợp.
SHOULD
AC1. GIVEN phiếu đã được tạo, WHEN nhân viên chọn nhóm sự cố và mức ưu tiên, THEN hệ thống lưu hai giá trị vào phiếu.

AC2. GIVEN mức ưu tiên được nhập, WHEN giá trị không thuộc Cao, Trung bình hoặc Thấp, THEN hệ thống từ chối lưu giá trị không hợp lệ.
US3
Là quản trị viên, tôi muốn tra cứu phiếu bảo hành để theo dõi các phiếu đang được xử lý.
SHOULD
AC1. GIVEN quản trị viên có quyền tra cứu, WHEN nhập mã phiếu hợp lệ, THEN hệ thống hiển thị đúng phiếu bảo hành.

AC2. GIVEN quản trị viên lọc theo trạng thái, WHEN thực hiện tra cứu, THEN hệ thống chỉ hiển thị các phiếu phù hợp với trạng thái đã chọn.
US4
Là quản trị viên, tôi muốn gán kỹ thuật viên cho phiếu bảo hành để phân công người chịu trách nhiệm xử lý.
MUST
AC1. GIVEN phiếu chưa được phân công, WHEN quản trị viên chọn một kỹ thuật viên và xác nhận, THEN phiếu được gán cho kỹ thuật viên đó.

AC2. GIVEN phiếu đã có kỹ thuật viên, WHEN quản trị viên cố gán thêm kỹ thuật viên thứ hai, THEN hệ thống từ chối thao tác và giữ nguyên người đang được phân công.

AC3. GIVEN kỹ thuật viên không tồn tại hoặc không ở trạng thái hoạt động, WHEN quản trị viên xác nhận phân công, THEN hệ thống từ chối và không thay đổi phiếu.
US5
Là kỹ thuật viên, tôi muốn xem phiếu bảo hành được phân công để nắm được nội dung và thực hiện xử lý.
SHOULD
AC1. GIVEN kỹ thuật viên đã đăng nhập, WHEN mở danh sách phiếu được phân công, THEN hệ thống chỉ hiển thị các phiếu thuộc kỹ thuật viên đó.

AC2. GIVEN kỹ thuật viên mở một phiếu, WHEN xem chi tiết, THEN hệ thống hiển thị thông tin phiếu, nhóm sự cố, mức ưu tiên, trạng thái và hạn cam kết.
US6
Là kỹ thuật viên, tôi muốn cập nhật trạng thái phiếu bảo hành để theo dõi tiến độ xử lý.
MUST
AC1. GIVEN phiếu đã được phân công cho kỹ thuật viên, WHEN kỹ thuật viên chọn trạng thái chuyển tiếp hợp lệ, THEN hệ thống cập nhật trạng thái và ghi một bản ghi vào ticket_status_log.

AC2. GIVEN phiếu chưa được phân công cho kỹ thuật viên, WHEN kỹ thuật viên cố cập nhật trạng thái, THEN hệ thống từ chối thao tác và không tạo log mới.

AC3. GIVEN trạng thái mới làm phiếu quay lại trạng thái trước đó, WHEN kỹ thuật viên xác nhận, THEN hệ thống từ chối chuyển trạng thái.
US7
Là quản trị viên, tôi muốn đóng phiếu bảo hành để xác nhận quy trình xử lý đã hoàn tất.
SHOULD
AC1. GIVEN phiếu đã ở trạng thái Hoàn tất, WHEN quản trị viên xác nhận đóng, THEN hệ thống chuyển phiếu sang Đã đóng và ghi nhận thời điểm đóng.

AC2. GIVEN phiếu chưa ở trạng thái Hoàn tất, WHEN quản trị viên yêu cầu đóng, THEN hệ thống từ chối đóng phiếu.

1.4. Yêu cầu chức năng
Mã
Yêu cầu chức năng
US
UC
FR1
Cho phép nhân viên tiếp nhận tạo phiếu với khách hàng, thiết bị và mô tả lỗi bắt buộc.
US1
UC01
FR2
Kiểm tra mô tả lỗi có độ dài tối thiểu 10 ký tự trước khi lưu.
US1
UC01
FR3
Cho phép nhân viên phân loại nhóm sự cố và mức ưu tiên.
US2
UC02
FR4
Cho phép quản trị viên tra cứu phiếu theo mã phiếu và trạng thái.
US3
UC03
FR5
Cho phép quản trị viên gán không quá một kỹ thuật viên cho mỗi phiếu.
US4
UC04
FR6
Cho phép kỹ thuật viên xem các phiếu được phân công cho mình.
US5
UC05
FR7
Cho phép kỹ thuật viên cập nhật trạng thái hợp lệ và lưu lịch sử thay đổi.
US6
UC06
FR8
Chỉ cho phép quản trị viên đóng phiếu khi phiếu đã hoàn tất xử lý.
US7
UC07



1.5. Yêu cầu phi chức năng
Mã
Yêu cầu phi chức năng
Ngưỡng
NFR1
Danh sách phiếu hiển thị dưới 2 giây với 100 bản ghi.
≤ 2 giây / 100 phiếu
NFR2
Nhân viên tiếp nhận mới tạo được một phiếu đúng trong dưới 3 phút mà không cần hỏi đồng nghiệp.
< 3 phút / phiếu
NFR3
Trong 10 lần mô phỏng mất kết nối lúc lưu, số phiếu đã xác nhận lưu nhưng bị mất bằng 0.
0/10 lần mất dữ liệu
NFR4
Hệ thống khởi động trên Windows, macOS và Linux bằng đúng hai lệnh Docker Compose.
3 OS / 2 lệnh

1.6. Ràng buộc và quy tắc nghiệp vụ
Mã
Quy tắc nghiệp vụ
Luồng liên quan
QT-01
Số điện thoại khách hàng là duy nhất trong hệ thống. Khi nhập số đã tồn tại, hệ thống phải hiển thị hồ sơ có sẵn thay vì tạo hồ sơ mới.
L2
QT-02
Số điện thoại được chuẩn hóa về dạng 10 chữ số bắt đầu bằng 0 trước khi lưu. Các dạng +84…, 84…, có dấu cách hoặc dấu chấm phải quy về dạng chuẩn.
L2
QT-03
Thiết bị được xác định duy nhất bằng số serial hoặc IMEI. Một thiết bị chỉ thuộc về một khách hàng tại một thời điểm.
L2
QT-04
Hạn cam kết được sinh tự động từ thời điểm tiếp nhận theo mức ưu tiên: CAO = 24 giờ, TRUNG_BINH = 72 giờ, THAP = 120 giờ; chỉ tính ngày làm việc từ thứ Hai đến thứ Bảy.
L2
QT-05
Thiết bị còn bảo hành nếu (ngày tiếp nhận − ngày mua) ≤ số tháng bảo hành của sản phẩm. Nếu không có ngày mua, phiếu phải được đánh dấu “chưa xác minh bảo hành” và cần quản lý phê duyệt.
L2
QT-06
Phiếu chỉ được chuyển trạng thái theo đúng vòng đời: Mới → Đã phân công → Đang xử lý → Chờ linh kiện → Hoàn tất → Đã đóng. Không được quay lại trạng thái trước; mọi lần chuyển trạng thái phải ghi vào ticket_status_log.
L2
QT-13
Không được xóa vật lý phiếu bảo hành. Chỉ đánh dấu ngừng sử dụng (soft delete) và giữ nguyên lịch sử.
Tất cả
QT-14
Nhân viên chỉ xem được dữ liệu của trung tâm hoặc cửa hàng mình làm việc; quản lý xem được toàn bộ đơn vị mình phụ trách; Ban giám đốc xem được toàn công ty.
Tất cả
QT-15
Số điện thoại khách hàng hiển thị dạng che, ví dụ 090****567, với mọi vai trò trừ Quản lý và Ban giám đốc.
Tất cả













1.7. Bảng truy vết yêu cầu


FR
US
Use Case
MoSCoW
FR1
US1
UC01
MUST
FR2
US1
UC01
MUST
FR3
US2
UC02
SHOULD
FR4
US3
UC03
SHOULD
FR5
US4
UC04
MUST
FR6
US5
UC05
SHOULD
FR7
US6
UC06
MUST
FR8
US7
UC07
SHOULD

