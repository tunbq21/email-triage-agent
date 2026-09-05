"""
Email Triage Agent — Entry Point

Chạy lệnh: uv run python main.py
"""
import os
from dotenv import load_dotenv
from graph.builder import build_graph
from data.mock_emails import get_mock_emails


def main():
    load_dotenv()

    if not os.getenv("GOOGLE_API_KEY"):
        print("Lỗi: Không tìm thấy GOOGLE_API_KEY trong file .env")
        return

    print("🚀 Khởi tạo Email Triage Agent...")
    app = build_graph()

    emails = get_mock_emails()
    print(f"📬 Tìm thấy {len(emails)} email cần xử lý.\n")

    for email in emails:
        result = app.invoke({"current_email": email})

        classification = result["classification"]
        print(f"  ├─ Category   : {classification.category.upper()}")
        print(f"  ├─ Priority   : {classification.priority}")
        print(f"  ├─ Confidence : {classification.confidence:.0%}")
        print(f"  ├─ Action     : {result.get('action_taken', '-')}")
        if result.get("draft_reply"):
            print(f"\n[DRAFT REPLY]\n{result['draft_reply']}\n")
        print("  " + "─" * 48)


if __name__ == "__main__":
    main()
