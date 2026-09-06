"""
Email Triage Agent — Entry Point

Chạy lệnh: uv run python main.py
"""
import os
from dotenv import load_dotenv
from graph.builder import build_graph
from tools.gmail_api import fetch_unread_emails


def main():
    load_dotenv()

    if not os.getenv("GOOGLE_API_KEY"):
        print("Lỗi: Không tìm thấy GOOGLE_API_KEY trong file .env")
        return

    print("Khoi tao Email Triage Agent...")
    app = build_graph()

    try:
        emails = fetch_unread_emails(max_results=3)
    except FileNotFoundError as e:
        print(f"\n Lỗi: {e}")
        return

    print(f"Tim thay {len(emails)} email chua doc.\n")

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
