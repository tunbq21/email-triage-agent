# Bộ Lệnh Kiểm Tra Chất Lượng Code (Code Quality & Testing)

Để đảm bảo dự án đạt chuẩn Production-grade, đây là danh sách "Thất kiếm" (7 lệnh) dùng để kiểm tra dự án Python một cách toàn diện. Chúng ta sử dụng `uv` làm trình quản lý (Package Manager).

## Nhóm 1: Format & Lint (Làm đẹp và Dọn rác)

1. **Ruff Format (Chỉnh sửa format PEP-8)**
   ```bash
   uv run ruff format .
   ```
   *Tác dụng:* Tự động căn lề, thụt đầu dòng, thêm bớt dấu ngoặc, dấu phẩy... cho đúng chuẩn PEP-8 đẹp mắt.

2. **Ruff Check & Fix (Bắt lỗi logic, xóa biến thừa, tự sắp xếp import)**
   ```bash
   uv run ruff check . --fix
   ```
   *Tác dụng:* Quét toàn bộ code tìm các lỗi tiềm ẩn (biến chưa dùng, import thừa, code rác) và tự động sửa những lỗi cơ bản.

## Nhóm 2: Typing & Testing (Chống bug)

3. **Mypy (Kiểm tra Type Hinting)**
   ```bash
   uv run mypy .
   ```
   *Tác dụng:* Kiểm tra xem bạn có vô tình truyền nhầm biến kiểu `string` vào một hàm đang đợi kiểu `int` hay không.

4. **Pytest (Chạy Unit Test)**
   ```bash
   uv run pytest
   ```
   *Tác dụng:* Chạy toàn bộ các file test trong thư mục `tests/` để đảm bảo không có module nào bị hỏng hóc sau khi sửa code.

5. **Coverage (Đo phần trăm code đã được Test)**
   ```bash
   uv run coverage run -m pytest
   uv run coverage report -m
   ```
   *Tác dụng:* Chỉ ra chính xác dòng code nào trong dự án CHƯA được chạy qua unit test bao giờ.

## Nhóm 3: Security (Bảo mật - Bắt buộc cho App có API/Cloud)

6. **Bandit (Quét lỗ hổng bảo mật trong code)**
   ```bash
   uv run bandit -r . -c pyproject.toml
   ```
   *Tác dụng:* Tìm xem code có đang vô tình hardcode mật khẩu, hay có nguy cơ bị SQL Injection / dính mã độc không.

7. **Safety (Quét lỗ hổng trong thư viện)**
   ```bash
   uv run safety check
   ```
   *Tác dụng:* Quét file thư viện xem có gói nào đang bị hacker công bố lỗ hổng CVE hay không để update kịp thời.
