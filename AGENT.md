# Email Triage Agent — AGENT.md

> **Dành cho AI coding agents (Codex, Claude, Gemini, v.v.).**
> Đọc file này trước khi thực hiện bất kỳ thay đổi nào trong repo.

---

## 1. Project Overview

**Email Triage Agent** là một AI agent phân loại, sắp xếp và quản lý hộp thư đến tự động.

| Thuộc tính | Chi tiết |
|---|---|
| **Mục tiêu** | Đọc, phân tích, dán nhãn và tự động phản hồi email cơ bản qua Gmail API |
| **Độ khó** | Beginner |
| **Framework** | LangChain + LangGraph |
| **LLM** | Google Gemini (via `langchain-google-genai`) |
| **Search tool** | Tavily |
| **Python** | ≥ 3.13 |
| **Package manager** | `uv` |

---

## 2. Cấu trúc thư mục

```
email-triage-agent/
├── agents/          # Định nghĩa các agent node (LangGraph)
├── chains/          # LangChain chains tái sử dụng
├── config/          # Cấu hình ứng dụng (model, prompts, v.v.)
├── core/            # Business logic cốt lõi, không phụ thuộc framework
├── data/            # Dữ liệu mẫu, fixtures
├── db/              # Persistence layer (nếu có)
├── docs/            # Tài liệu kỹ thuật
├── logs/            # Log files (KHÔNG commit)
├── schemas/         # Pydantic schemas / data models
├── tests/           # Unit & integration tests
├── tools/           # Custom LangChain tools (Gmail, v.v.)
├── main.py          # Entry point
├── pyproject.toml   # Project metadata & dependencies
└── .env             # Secrets (KHÔNG commit)
```

---

## 3. Setup nhanh

```bash
# 1. Cài dependencies
uv sync

# 2. Tạo file .env từ mẫu
cp .env.example .env
# Điền GOOGLE_API_KEY, TAVILY_API_KEY, Gmail credentials...

# 3. Chạy agent
uv run python main.py
```

---

## 4. Stack & Dependencies

| Package | Vai trò |
|---|---|
| `langchain-core` | Abstraction layer (Runnable, Messages) |
| `langchain-google-genai` | Gemini LLM integration |
| `langgraph` | Orchestration graph (state machine) |
| `pydantic` | Data validation & schemas |
| `python-dotenv` | Load biến môi trường từ `.env` |
| `tavily-python` | Web search tool |

---

## 5. ✅ DO — Những điều PHẢI làm

### 5.1 Về code chung

- **Dùng `uv`** để quản lý dependencies: `uv add <package>`, `uv sync`, `uv run`.
- **Dùng type hints** cho mọi function signature. Python 3.13+, ưu tiên `X | Y` thay `Union[X, Y]`.
- **Dùng Pydantic v2** để định nghĩa tất cả data model và schema. Không dùng `dict` thuần khi có thể dùng model.
- **Dùng `python-dotenv`** để load secrets. Tất cả API key phải đọc từ `os.getenv(...)`.
- **Viết docstring** cho mọi class và function public theo format Google style.
- **Đặt test** trong `tests/` với naming `test_<module>.py`. Dùng `pytest`.

### 5.2 Về LangChain / LangGraph

- **Dùng LCEL (LangChain Expression Language)** — cú pháp `chain = prompt | llm | parser` — thay vì legacy `LLMChain`.
- **Định nghĩa State rõ ràng** bằng `TypedDict` hoặc Pydantic model cho mọi LangGraph graph.
- **Đặt tất cả custom tool** vào `tools/`, dùng decorator `@tool` của LangChain.
- **Dùng `langchain-google-genai`** để khởi tạo Gemini, ví dụ: `ChatGoogleGenerativeAI(model="gemini-2.0-flash")`.
- **Xử lý tool error** trong graph: luôn có edge hoặc conditional để bắt lỗi từ tool node.

### 5.3 Về cấu trúc module

- Code logic thuần (không phụ thuộc LangChain) đặt vào `core/`.
- Mỗi agent / subgraph là một file riêng trong `agents/`.
- Chains tái sử dụng đặt vào `chains/`.

---

## 6. ❌ DON'T — Những điều KHÔNG được làm

### 6.1 Về bảo mật

- **KHÔNG hardcode** API key, OAuth credentials, hay bất kỳ secret nào trong code.
- **KHÔNG commit** file `.env`, `credentials.json`, hay `token.json` (Gmail OAuth).
- **KHÔNG log** nội dung email hay thông tin cá nhân của người dùng ở level INFO/DEBUG.

### 6.2 Về code

- **KHÔNG dùng** `LLMChain`, `ConversationChain` hay các class legacy của LangChain v0.1.
- **KHÔNG import** trực tiếp từ `langchain` (gói gốc) nếu có thể import từ `langchain_core` hoặc integration package cụ thể.
- **KHÔNG dùng** `Any` type hint trừ khi thực sự không thể tránh — phải có comment giải thích.
- **KHÔNG để** hàm quá 50 dòng. Nếu vượt quá, tách thành hàm nhỏ hơn.
- **KHÔNG dùng** `print()` để debug. Dùng `logging` module với logger được đặt tên theo module.

### 6.3 Về LangGraph

- **KHÔNG tạo** vòng lặp vô hạn trong graph mà không có điều kiện dừng rõ ràng (`recursion_limit`).
- **KHÔNG mutate** State dict trực tiếp — luôn trả về dict mới từ node function.
- **KHÔNG đặt** business logic phức tạp trực tiếp trong node — delegate xuống `core/`.

### 6.4 Về file & commit

- **KHÔNG commit** vào `logs/`, `data/raw/`, hay bất kỳ file sinh ra lúc runtime.
- **KHÔNG xóa** hay sửa `skills-lock.json` thủ công.
- **KHÔNG sửa** `uv.lock` thủ công — để `uv` tự quản lý.

---

## 7. Conventions & Naming

| Đối tượng | Convention | Ví dụ |
|---|---|---|
| File / module | `snake_case` | `email_classifier.py` |
| Class | `PascalCase` | `EmailTriageAgent` |
| Function / variable | `snake_case` | `classify_email()` |
| Hằng số | `UPPER_SNAKE_CASE` | `MAX_RETRY_COUNT = 3` |
| LangGraph node | `snake_case` + suffix `_node` | `classify_node` |
| Pydantic model | `PascalCase` + suffix `State`/`Input`/`Output` | `TriageState`, `EmailInput` |
| Tool | `snake_case`, động từ + danh từ | `get_emails`, `send_reply` |

---

## 8. Biến môi trường

Tạo file `.env` từ `.env.example`. Các biến bắt buộc:

```env
GOOGLE_API_KEY=          # Gemini API key
TAVILY_API_KEY=          # Tavily search API key
```

Biến tuỳ chọn (Gmail OAuth):

```env
GMAIL_CREDENTIALS_PATH=  # Đường dẫn tới credentials.json
GMAIL_TOKEN_PATH=        # Đường dẫn tới token.json
```

---

## 9. Ghi chú cho AI Agent

- **Ưu tiên đọc `docs/`** trước khi thay đổi logic phức tạp.
- Khi thêm dependency mới: chạy `uv add <package>` — **không tự sửa** `pyproject.toml` thủ công.
- Khi tạo tool mới: đặt vào `tools/`, export trong `tools/__init__.py`, viết unit test kèm theo.
- Khi tạo graph node mới: định nghĩa signature `(state: TriageState) -> dict` hoặc tương đương.
- Mọi thay đổi breaking phải có comment `# BREAKING CHANGE:` rõ ràng.
