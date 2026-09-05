from schemas.state import TriageState
from services.classifier import classify_email
from services.auto_reply import generate_auto_reply


def classifier_node(state: TriageState) -> dict:
    """
    Node phân loại email.
    Nhận state, lấy current_email, gọi classifier service, và trả về dict để cập nhật state.
    """
    email = state["current_email"]
    print(f"\n--- Đang xử lý email: [{email.id}] {email.subject} ---")
    classification = classify_email(email)
    return {"classification": classification}


def archive_node(state: TriageState) -> dict:
    """
    Node xử lý thư rác, quảng cáo, hoặc thư không quan trọng.
    """
    email = state["current_email"]
    print(f"[{email.id}] 🗑️ Chuyển vào Archive/Thùng rác.")
    return {"action_taken": "archived"}


def human_review_node(state: TriageState) -> dict:
    """
    Node xử lý email thông thường.
    Chuyển email vào danh sách chờ con người xem xét và trả lời.
    """
    email = state["current_email"]
    print(f"[{email.id}] 👤 Đã đưa vào hàng chờ Human Review.")
    return {"action_taken": "pending_human_review"}


def auto_reply_node(state: TriageState) -> dict:
    """
    Node xử lý các email khẩn cấp/quan trọng (P0, P1).
    Tự động soạn thảo một email phản hồi (draft).
    """
    email = state["current_email"]
    classification = state["classification"]

    print(f"[{email.id}] 🤖 Đang soạn thư phản hồi khẩn cấp (Priority: {classification.priority})...")

    draft = generate_auto_reply({
        "sender": email.sender,
        "subject": email.subject,
        "body": email.body,
        "priority": classification.priority
    })

    return {
        "action_taken": "auto_replied",
        "draft_reply": draft
    }
