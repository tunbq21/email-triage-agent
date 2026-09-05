# Cấu trúc thư mục (Project Structure)

Dự án **Email Triage Agent** được thiết kế theo tiêu chuẩn của một hệ thống AI Agent Production-ready. Việc phân chia thư mục rõ ràng giúp tách biệt các mối quan tâm (Separation of Concerns), dễ dàng mở rộng và bảo trì.

Dưới đây là giải thích chi tiết vai trò của từng thư mục:

## 1. `schemas/` (Data Models)
**Vai trò:** Định nghĩa hình dáng của dữ liệu (Data Structures) truyền vào và đi ra khỏi các thành phần của hệ thống.
- Chứa các class **Pydantic** để xác thực dữ liệu (ví dụ: `EmailInput`, `ClassificationResult`).
- Giúp LLM trả về kết quả theo chuẩn Structured Output thay vì text lộn xộn.
- Khai báo kiểu dữ liệu `State` (bộ nhớ trung tâm) cho đồ thị LangGraph.

## 2. `chains/` (LLM Interactions)
**Vai trò:** Nơi chứa các logic tương tác trực tiếp với mô hình ngôn ngữ (LLM).
- Chứa các Prompt Templates (lệnh hướng dẫn AI).
- Kết hợp Prompt và LLM thành các chuỗi xử lý (LangChain LCEL).
- Ví dụ: `classifier.py` nhận email, đưa vào prompt, gọi Gemini, và trả về object kết quả.

## 3. `agents/` (Graph Nodes & Orchestration)
**Vai trò:** Định nghĩa các bước xử lý (Nodes) và luồng đi (Routing) trong đồ thị LangGraph.
- Mỗi file trong này thường tương ứng với một hành động hoặc một Agent nhỏ (Ví dụ: `classifier_node`, `reply_node`, `label_node`).
- Nhận `State` hiện tại, xử lý (thường là gọi sang `chains/` hoặc `tools/`), và trả về kết quả để cập nhật `State` mới.

## 4. `tools/` (Agentic Tools)
**Vai trò:** Chứa các công cụ (Function Calling) mà AI Agent có thể sử dụng để tương tác với thế giới bên ngoài.
- Tích hợp API bên thứ ba (như Gmail API để đọc/gửi email, Tavily để tìm kiếm web).
- Các hàm ở đây thường được bọc bởi `@tool` decorator của LangChain.

## 5. `core/` (Business Logic & Utils)
**Vai trò:** Chứa các logic cốt lõi của ứng dụng nhưng không trực tiếp phụ thuộc vào framework AI.
- Chứa dữ liệu giả lập (`mock_data.py`).
- Các hàm helper, config loader, logging, hoặc evaluation metrics.

## 6. `tests/` (Testing)
**Vai trò:** Đảm bảo hệ thống hoạt động ổn định và chính xác.
- Chứa các bài test tự động chạy bằng `pytest`.
- **Unit Test:** Kiểm tra từng hàm nhỏ.
- **Evaluation Test:** Kiểm tra chất lượng (Ground Truth) của LLM output.

## 7. Các thư mục khác
- **`docs/`**: Chứa tài liệu thiết kế hệ thống, hướng dẫn sử dụng (như file bạn đang đọc).
- **`config/`**: (Nếu có) Chứa các file YAML/JSON cấu hình (system prompts, thresholds...).
- **`logs/`**: Nơi hệ thống tự động ghi lại lịch sử hoạt động (bị ignore trên Git).
- **`db/`**: Chứa SQLite checkpointer để LangGraph ghi nhớ State qua nhiều lần chạy (Persistent Memory).
