# Email Triage Agent

Email Triage Agent là một hệ thống AI tự động phân loại, lọc nhiễu và xử lý hòm thư điện tử (Gmail). Hệ thống đóng vai trò như một "Trạm kiểm soát tín hiệu", tự động phân biệt thư rác, thư quảng cáo, và những thư công việc quan trọng cần ưu tiên (P0, P1). Đặc biệt, với các thư khẩn cấp, AI Agent có thể tự động soạn sẵn các bản nháp (Drafts) phản hồi thay cho người dùng.

## Công Nghệ Sử Dụng (Tech Stack)

Dự án được xây dựng dựa trên kiến trúc hiện đại, tập trung vào hiệu năng và khả năng mở rộng:

- **Ngôn ngữ:** Python 3.12+
- **Package Manager:** `uv` (Siêu tốc, thay thế pip/poetry)
- **AI Framework:** `LangGraph` & `LangChain` (Quản lý luồng Agentic AI)
- **Mô hình Ngôn ngữ (LLM):** `Google Gemini` (Gemini 3.1 Pro / Gemini Flash)
- **Backend Framework:** `FastAPI` + `Uvicorn`
- **Giao diện (Frontend):** Vanilla HTML/CSS/JS (Thiết kế Glassmorphism, tối giản)
- **Tích hợp API:** `Google Gmail API` (Xác thực OAuth 2.0)
- **Data Parsing:** `Pydantic` (Xác thực schema)

## Kiến Trúc Dự Án (Architecture)

Dự án áp dụng mô hình phân tách rõ ràng (Separation of Concerns), chia thành 4 lớp chính:

1. **Lớp Giao Diện (Frontend & Web API):**
   - `main.py`: Điểm neo (Entry point) của ứng dụng, chạy server FastAPI.
   - `static/`: Chứa mã nguồn giao diện đồ họa.
2. **Lớp Orchestration (Graph):**
   - `graph/builder.py` & `graph/nodes.py`: Điều phối luồng xử lý email bằng LangGraph (StateGraph), định tuyến các email vào đúng chu trình (auto-reply, human-review, archive).
3. **Lớp AI Logic (Services):**
   - `services/llm.py`: Cấu hình LLM chính.
   - `services/classifier.py`: Chứa System Prompt phức tạp để phân loại độ ưu tiên (P0-P3) và danh mục (Category).
   - `services/auto_reply.py`: Logic soạn thảo thư trả lời tự động dựa trên ngữ cảnh.
4. **Lớp Công Cụ (Tools):**
   - `tools/gmail_api.py`: Quản lý OAuth, lấy email chưa đọc và tạo Draft trên Gmail thực tế.

```text
email-triage-agent/
├── main.py              # Web server (FastAPI)
├── run_cli.py           # CLI fallback
├── static/              # Giao diện web (HTML/CSS/JS)
├── schemas/             # Pydantic models (Email, Classification)
├── services/            # AI Chains & LLM configuration
├── graph/               # LangGraph workflow (Nodes & Edges)
├── tools/               # External APIs (Gmail API)
├── docs/                # Tài liệu dự án
└── tests/               # Unit, Integration, E2E Testing
```

## Cách Khởi Chạy (How to run)

1. Cài đặt các thư viện thông qua `uv`:
   ```bash
   uv sync
   ```

2. Yêu cầu có file `credentials.json` (Google Cloud OAuth Client ID) đặt tại thư mục gốc.

3. Khởi động Web Server:
   ```bash
   uv run python main.py
   ```

4. Truy cập giao diện tại: `http://localhost:8000`
