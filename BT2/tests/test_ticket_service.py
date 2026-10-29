"""Unit test lớp nghiệp vụ tạo phiếu bảo hành (UC01) - ticket_service.

Ba nhóm bắt buộc của Bài tập 2:
  1. Luồng đúng (happy path)  : TestHappyPath
  2. Giá trị biên (boundary)   : TestBoundary   (FR2: mô tả lỗi tối thiểu 10 ký tự)
  3. Dữ liệu sai (invalid)     : TestInvalidInput

Test chạy trên repository giả trong bộ nhớ (xem conftest.py), không dùng MySQL.
"""
from datetime import date, datetime

import pytest
from services import ticket_service
from services.ticket_service import (MIN_DESC_LENGTH, ValidationError,
                                     admin_update_ticket, close_ticket,
                                     create_ticket, update_ticket_description)

EMPLOYEE_ID = 1  # nhân viên tiếp nhận thực hiện thao tác


# ============================================================================
# 1. LUỒNG ĐÚNG
# ============================================================================
class TestHappyPath:
    def test_create_ticket_with_valid_data_stores_correct_ticket(self, repo, make_data, now):
        """Dữ liệu hợp lệ -> tạo đúng phiếu, trạng thái đầu 'MOI', các trường quan trọng lưu chính xác."""
        data = make_data(phone="+84 843 310 647")

        result = create_ticket(repo, data, EMPLOYEE_ID, now=now)

        # --- kết quả trả về ---
        assert result["ticket_code"] == "BH-0001"
        assert result["ticket_status"] == "MOI"
        # --- phiếu được lưu ---
        assert len(repo.tickets) == 1
        t = repo.tickets[result["ticket_id"]]
        assert t["ticket_code"] == "BH-0001"
        assert t["ticket_status"] == "MOI"
        assert t["issue_category"] == "MAN_HINH"
        assert t["priority"] == "CAO"
        assert t["issue_desc"] == "Man hinh bi soc doc, khong cam ung duoc"
        assert t["received_by_employee_id"] == EMPLOYEE_ID
        assert t["received_at"] == now
        assert t["due_date"] == datetime(2026, 10, 27, 9, 0, 0)  # CAO = 24h: Thứ Hai -> Thứ Ba
        # --- khách hàng mới có SĐT đã chuẩn hóa ---
        assert list(repo.customers.values()) == [{"full_name": "Vu The Long", "phone": "0843310647"}]
        assert t["customer_id"] in repo.customers
        # --- thiết bị mới gắn với khách đó ---
        assert list(repo.devices.values()) == [
            {
                "customer_id": t["customer_id"],
                "serial_no": "IMEI350000000000001",
                "model_name": "Mekong Phone X1",
                "purchase_date": date(2026, 3, 15),
                "warranty_months": 12,
            }
        ]
        assert t["device_id"] in repo.devices
        # --- QT-06: có đúng 1 log khởi tạo, và dữ liệu đã được commit ---
        assert repo.status_logs == [(result["ticket_id"], None, "MOI", EMPLOYEE_ID)]
        assert repo.commits == 1
        assert repo.rollbacks == 0

    def test_existing_customer_and_device_are_reused(self, repo, make_data, now):
        """QT-01/QT-03: khách và thiết bị đã có thì dùng lại, không tạo bản ghi trùng."""
        cid = repo.seed_customer("Vu The Long", "0843310647")
        did = repo.seed_device(cid, "IMEI350000000000001")

        result = create_ticket(repo, make_data(full_name="", model_name=""), EMPLOYEE_ID, now=now)

        t = repo.tickets[result["ticket_id"]]
        assert (t["customer_id"], t["device_id"]) == (cid, did)
        assert len(repo.customers) == 1 and len(repo.devices) == 1

    def test_ticket_codes_are_sequential_and_unique(self, repo, make_data, now):
        """Mỗi phiếu mới nhận một mã BH-xxxx khác nhau."""
        first = create_ticket(repo, make_data(), EMPLOYEE_ID, now=now)
        second = create_ticket(repo, make_data(issue_desc="Pin tut nhanh, may nong khi sac"), EMPLOYEE_ID, now=now)
        assert (first["ticket_code"], second["ticket_code"]) == ("BH-0001", "BH-0002")

    @pytest.mark.parametrize(
        "priority, received, expected_due",
        [
            ("CAO", datetime(2026, 10, 26, 9, 0), datetime(2026, 10, 27, 9, 0)),
            ("THAP", datetime(2026, 10, 26, 9, 0), datetime(2026, 10, 31, 9, 0)),
            ("TRUNG_BINH", datetime(2026, 10, 30, 9, 0), datetime(2026, 11, 3, 9, 0)),
        ],
    )
    def test_due_date_follows_priority_and_skips_sunday(self, repo, make_data, priority, received, expected_due):
        """QT-04: hạn cam kết tự sinh theo mức ưu tiên, không tính Chủ Nhật."""
        result = create_ticket(repo, make_data(priority=priority), EMPLOYEE_ID, now=received)
        assert result["due_date"] == expected_due
        assert repo.tickets[result["ticket_id"]]["due_date"] == expected_due


# ============================================================================
# 2. GIÁ TRỊ BIÊN - FR2: mô tả lỗi tối thiểu 10 ký tự
# ============================================================================
class TestBoundary:
    def test_min_length_constant_matches_srs_fr2(self):
        """Hằng số nghiệp vụ phải đúng 10 như SRS FR2 quy định."""
        assert MIN_DESC_LENGTH == 10

    def test_description_with_exactly_10_characters_is_accepted(self, repo, make_data, now):
        """Biên dưới: đúng 10 ký tự phải được chấp nhận và lưu nguyên văn."""
        desc = "1234567890"
        assert len(desc) == 10

        result = create_ticket(repo, make_data(issue_desc=desc), EMPLOYEE_ID, now=now)

        assert repo.tickets[result["ticket_id"]]["issue_desc"] == desc
        assert repo.commits == 1

    def test_description_with_9_characters_is_rejected(self, repo, make_data, now, assert_nothing_created):
        """Ngay dưới biên: 9 ký tự phải bị từ chối, không tạo phiếu."""
        with pytest.raises(ValidationError) as exc:
            create_ticket(repo, make_data(issue_desc="123456789"), EMPLOYEE_ID, now=now)

        assert "ít nhất 10 ký tự" in exc.value.message
        assert exc.value.fields == ["issue_desc"]
        assert_nothing_created(repo)

    def test_description_with_11_characters_is_accepted(self, repo, make_data, now):
        """Ngay trên biên: 11 ký tự được chấp nhận."""
        result = create_ticket(repo, make_data(issue_desc="12345678901"), EMPLOYEE_ID, now=now)
        assert repo.tickets[result["ticket_id"]]["issue_desc"] == "12345678901"

    def test_surrounding_spaces_do_not_count_towards_length(self, repo, make_data, now, assert_nothing_created):
        """Khoảng trắng đầu/cuối bị cắt trước khi đếm: 9 ký tự + khoảng trắng vẫn bị từ chối."""
        with pytest.raises(ValidationError):
            create_ticket(repo, make_data(issue_desc="   123456789   "), EMPLOYEE_ID, now=now)
        assert_nothing_created(repo)

    def test_10_characters_with_surrounding_spaces_is_accepted_and_trimmed(self, repo, make_data, now):
        """10 ký tự thật sự (kèm khoảng trắng thừa) hợp lệ, và được lưu sau khi cắt khoảng trắng."""
        result = create_ticket(repo, make_data(issue_desc="  1234567890  "), EMPLOYEE_ID, now=now)
        assert repo.tickets[result["ticket_id"]]["issue_desc"] == "1234567890"


# ============================================================================
# 3. DỮ LIỆU SAI
# ============================================================================
class TestInvalidInput:
    @pytest.mark.parametrize("desc", ["", "   ", "ngan", "123456789"])
    def test_short_or_empty_description_is_rejected(self, repo, make_data, now, assert_nothing_created, desc):
        """Mô tả lỗi rỗng hoặc ngắn hơn 10 ký tự: từ chối, báo lỗi rõ ràng, không tạo phiếu."""
        with pytest.raises(ValidationError) as exc:
            create_ticket(repo, make_data(issue_desc=desc), EMPLOYEE_ID, now=now)

        assert "issue_desc" in exc.value.fields
        assert "Mô tả lỗi" in exc.value.message
        assert_nothing_created(repo)

    @pytest.mark.parametrize(
        "override, field, label",
        [
            ({"phone": ""}, "phone", "Số điện thoại"),
            ({"phone": "12345"}, "phone", "Số điện thoại"),
            ({"phone": "abcdefghij"}, "phone", "Số điện thoại"),
            ({"serial_no": ""}, "serial_no", "serial/IMEI"),
            ({"serial_no": "   "}, "serial_no", "serial/IMEI"),
        ],
    )
    def test_missing_required_field_is_rejected_with_clear_message(
        self, repo, make_data, now, assert_nothing_created, override, field, label
    ):
        """US1-AC3: thiếu trường bắt buộc -> từ chối, thông báo nêu đúng trường còn thiếu."""
        with pytest.raises(ValidationError) as exc:
            create_ticket(repo, make_data(**override), EMPLOYEE_ID, now=now)

        assert exc.value.fields == [field]
        assert label in exc.value.message
        assert_nothing_created(repo)

    def test_message_lists_every_missing_field(self, repo, now, assert_nothing_created):
        """Thiếu nhiều trường cùng lúc: thông báo nêu đủ tất cả."""
        with pytest.raises(ValidationError) as exc:
            create_ticket(repo, {}, EMPLOYEE_ID, now=now)

        assert exc.value.fields == ["phone", "serial_no", "issue_desc"]
        for label in ("Số điện thoại", "serial/IMEI", "Mô tả lỗi"):
            assert label in exc.value.message
        assert_nothing_created(repo)

    @pytest.mark.parametrize(
        "override",
        [
            {"priority": "KHAN_CAP"},
            {"priority": ""},
            {"issue_category": "KHONG_CO"},
        ],
    )
    def test_invalid_category_or_priority_is_rejected(self, repo, make_data, now, assert_nothing_created, override):
        with pytest.raises(ValidationError) as exc:
            create_ticket(repo, make_data(**override), EMPLOYEE_ID, now=now)
        assert "không hợp lệ" in exc.value.message
        assert_nothing_created(repo)

    def test_new_customer_without_name_is_rejected(self, repo, make_data, now, assert_nothing_created):
        """US1-AC2: khách mới bắt buộc có họ tên."""
        with pytest.raises(ValidationError) as exc:
            create_ticket(repo, make_data(full_name=""), EMPLOYEE_ID, now=now)
        assert exc.value.fields == ["full_name"]
        assert_nothing_created(repo)

    def test_serial_owned_by_another_customer_is_rejected_and_rolled_back(self, repo, make_data, now):
        """QT-03: serial đã thuộc khách khác -> từ chối; khách mới vừa thêm giữa chừng cũng bị hoàn tác."""
        owner = repo.seed_customer("Nguyen Van An", "0912345678")
        repo.seed_device(owner, "IMEI350000000000001")

        with pytest.raises(ValidationError) as exc:
            create_ticket(repo, make_data(phone="0843310647"), EMPLOYEE_ID, now=now)

        assert "thuộc về khách hàng khác" in exc.value.message
        assert repo.tickets == {} and repo.status_logs == []
        assert list(repo.customers) == [owner], "khách mới (0843310647) phải bị rollback"
        assert repo.rollbacks == 1 and repo.commits == 0

    def test_unexpected_storage_error_rolls_back_everything(self, repo, make_data, now):
        """NFR3: lỗi lưu giữa chừng -> hoàn tác toàn bộ, không còn phiếu/khách/thiết bị dở dang."""
        class BrokenLog(type(repo)):
            def add_status_log(self, *args):
                raise RuntimeError("mất kết nối khi ghi log")

        broken = BrokenLog()
        with pytest.raises(RuntimeError, match="mất kết nối"):
            create_ticket(broken, make_data(), EMPLOYEE_ID, now=now)

        assert broken.tickets == {} and broken.customers == {} and broken.devices == {}
        assert broken.rollbacks == 1 and broken.commits == 0

    def test_normalize_phone_rejects_garbage_and_accepts_known_formats(self):
        """QT-02: chuẩn hóa về 10 số bắt đầu bằng 0."""
        assert ticket_service.normalize_phone("+84 843.310.647") == "0843310647"
        assert ticket_service.normalize_phone("84843310647") == "0843310647"
        assert ticket_service.normalize_phone("0843310647") == "0843310647"
        assert ticket_service.normalize_phone("843310647") is None
        assert ticket_service.normalize_phone(None) is None



# ============================================================================
# 4. CHỈNH SỬA MÔ TẢ VÀ CẬP NHẬT/ĐÓNG PHIẾU
# ============================================================================
class TestTicketModificationsAndClosing:
    def test_update_ticket_description_success(self, repo, make_data, now):
        """Nhân viên tiếp nhận có thể sửa mô tả cho phiếu còn mở."""
        t_info = create_ticket(repo, make_data(), EMPLOYEE_ID, now=now)
        tid = t_info["ticket_id"]

        new_desc = "Thay đổi mô tả lỗi: máy bị vỡ màn hình kèm lỗi sạc"
        code = update_ticket_description(repo, tid, new_desc, EMPLOYEE_ID)

        assert code == t_info["ticket_code"]
        assert repo.tickets[tid]["issue_desc"] == new_desc

    def test_update_ticket_description_fails_if_too_short(self, repo, make_data, now):
        """Mô tả sửa đổi phải đạt tối thiểu 10 ký tự."""
        t_info = create_ticket(repo, make_data(), EMPLOYEE_ID, now=now)
        tid = t_info["ticket_id"]

        with pytest.raises(ValidationError) as exc:
            update_ticket_description(repo, tid, "Quá ngắn", EMPLOYEE_ID)
        assert f"ít nhất {MIN_DESC_LENGTH} ký tự" in exc.value.message

    def test_update_ticket_description_fails_if_closed(self, repo, make_data, now):
        """Không cho phép sửa mô tả khi phiếu đã ở trạng thái Đã đóng."""
        t_info = create_ticket(repo, make_data(), EMPLOYEE_ID, now=now)
        tid = t_info["ticket_id"]
        repo.tickets[tid]["ticket_status"] = "DA_DONG"

        with pytest.raises(ValidationError) as exc:
            update_ticket_description(repo, tid, "Mô tả mới dài hơn 10 ký tự", EMPLOYEE_ID)
        assert "Phiếu đã đóng" in exc.value.message

    def test_admin_update_ticket_priority_recalculates_due_date(self, repo, make_data, now):
        """Quản trị viên đổi mức ưu tiên -> hệ thống tự tính lại hạn cam kết SLA."""
        t_info = create_ticket(repo, make_data(priority="CAO"), EMPLOYEE_ID, now=now)
        tid = t_info["ticket_id"]

        # Đổi từ CAO (24h) sang THAP (120h)
        update_data = {
            "issue_category": "PIN",
            "priority": "THAP",
            "ticket_status": "DANG_XU_LY",
            "issue_desc": "Pin chai nhanh tụt pin cần thay thế",
            "technician_id": 2,
        }
        admin_update_ticket(repo, tid, update_data, EMPLOYEE_ID)

        t = repo.tickets[tid]
        assert t["issue_category"] == "PIN"
        assert t["priority"] == "THAP"
        assert t["ticket_status"] == "DANG_XU_LY"
        assert t["technician_id"] == 2
        # THAP = 120h (Thứ Hai 26/10 -> Thứ Bảy 31/10 09:00:00)
        assert t["due_date"] == datetime(2026, 10, 31, 9, 0, 0)
        # Có ghi nhận log chuyển từ MOI sang DANG_XU_LY
        assert (tid, "MOI", "DANG_XU_LY", EMPLOYEE_ID) in repo.status_logs

    def test_close_ticket_only_allowed_when_completed(self, repo, make_data, now):
        """Chỉ cho phép đóng phiếu khi trạng thái là HOAN_TAT."""
        t_info = create_ticket(repo, make_data(), EMPLOYEE_ID, now=now)
        tid = t_info["ticket_id"]

        # Đang là MOI -> đóng sẽ bị từ chối
        with pytest.raises(ValidationError) as exc:
            close_ticket(repo, tid, EMPLOYEE_ID)
        assert "Chỉ đóng được phiếu ở trạng thái Hoàn tất" in exc.value.message

        # Cập nhật sang HOAN_TAT -> đóng thành công
        repo.tickets[tid]["ticket_status"] = "HOAN_TAT"
        code = close_ticket(repo, tid, EMPLOYEE_ID)
        assert code == t_info["ticket_code"]
        assert repo.tickets[tid]["ticket_status"] == "DA_DONG"
        assert repo.tickets[tid]["closed_at"] is not None
        assert (tid, "HOAN_TAT", "DA_DONG", EMPLOYEE_ID) in repo.status_logs
