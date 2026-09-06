# Tóm Tắt Ngữ Cảnh Dự Án (Project Context)

> **Lưu ý dành cho AI Agent ở phiên làm việc mới:**
> Hãy đọc kỹ file này trước khi thực hiện bất kỳ thay đổi nào để nắm bắt kiến trúc, tiến độ và quy chuẩn thiết kế của dự án.

## 1. Tổng Quan Dự Án
- **Tên dự án:** Email Triage Agent
- **Mục tiêu:** Một AI Agent tự động đọc hòm thư (Gmail), lọc nhiễu (spam, promotion) và đánh giá mức độ ưu tiên của email. Với các email cực kỳ quan trọng (P0), AI sẽ tự động điều tra và soạn sẵn bản nháp (Draft) phản hồi.
- **Tình trạng hiện tại:** Đã hoàn thành **Phase 3**. Hệ thống đã tích hợp thành công Web UI (FastAPI) và kết nối được với Gmail API thực tế qua OAuth 2.0.

## 2. Công Nghệ & Kiến Trúc
- **Ngôn ngữ:** Python 3.12+ (Quản lý package bằng `uv`).
- **AI Framework:** `LangGraph` (Quản lý luồng state machine) & `LangChain`.
- **Mô Hình:** Google Gemini (Hiện đang dùng `Gemini 3.1 Pro`).
- **Web Framework:** `FastAPI` + `Uvicorn`.
- **Frontend:** Vanilla HTML/CSS/JS thuần túy. KHÔNG DÙNG framework frontend nặng nề.

### Cấu trúc 4 Lớp Hiện Tại:
1. **Frontend & Web API (`main.py`, `static/`)**: FastAPI phục vụ file tĩnh và cung cấp API `/api/triage`.
2. **Orchestration (`graph/`)**: Chứa `builder.py`, `nodes.py`, `router.py` quản lý luồng StateGraph.
3. **Services (`services/`)**: Chứa logic gọi LLM (`classifier.py`, `auto_reply.py`).
4. **Tools (`tools/`)**: Chứa `gmail_api.py` xử lý xác thực OAuth và các thao tác Gmail.

## 3. Quy Chuẩn Thiết Kế Giao Diện (Frontend Design Strict Rules)
Giao diện tuân thủ tuyệt đối kỹ năng `frontend-design` đã được thống nhất:
- **Concept:** Trạm kiểm soát tín hiệu (Signal Control Station).
- **Aesthetic:** Dark mode, Glassmorphism, phong cách Premium, siêu tối giản.
- **Palette Màu (CSS Variables):** 
  - Nền: `Midnight Indigo` (`#0B0E14`).
  - Text: `Ice White` (`#F2F5F8`), `Muted Azure` (`#8A9BB4`).
  - Cảnh báo P0 (Khẩn cấp): `Neon Coral` (`#FF5A5F`).
  - Cảnh báo P2 (Chờ duyệt): `Warm Amber` (`#F5A623`).
  - Cảnh báo Archive (Rác): `Muted Slate` (`#4A5568`).
- **Typography:** `Outfit` cho Heading/Tags, `Inter` cho Body text.

## 4. Các Lệnh Cần Nhớ (Code Quality)
Mọi đoạn code Python mới viết ra phải vượt qua 4 lệnh kiểm tra sau:
1. `uv run ruff format .` (Định dạng code)
2. `uv run ruff check . --fix` (Bắt lỗi và tự sửa)
3. `uv run mypy .` (Kiểm tra kiểu Type Hinting)
4. `uv run pytest` (Đảm bảo Unit Tests luôn pass)

## 5. Tiến Độ Kế Tiếp (Roadmap / Phase 4)
- Viết kịch bản tự động gán nhãn (Labeling) và xóa mail/lưu trữ (Archive) thật sự trên Gmail (hiện tại mới chỉ phân loại trên Web UI chứ chưa thao tác ngược lại hòm thư gốc).
- Thêm giao diện để người dùng có thể bấm duyệt (Approve) và gửi (Send) các email ở trạng thái P2 (Pending Human Review).
- Bổ sung toàn diện bộ Unit Test, Integration Test và E2E Test cho các file trong thư mục `tests/`.
