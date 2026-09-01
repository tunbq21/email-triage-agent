from schemas.state import TriageState
from chains.classifier import classify_email_chain

def classifier_node(state: TriageState) -> dict:
    """
    Node phân loại email.
    Nhận state, lấy current_email, gọi classifier chain, và trả về dict để cập nhật state.
    """
    email = state["current_email"]
    print(f"\n--- Đang xử lý email: [{email.id}] {email.subject} ---")
    
    # Gọi chain phân loại
    classification = classify_email_chain(email)
    
    # Trả về dict chứa các trường cần cập nhật trong State
    return {"classification": classification}
