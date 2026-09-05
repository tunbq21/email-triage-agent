from schemas.state import TriageState


def route_email(state: TriageState) -> str:
    """
    Quyết định node tiếp theo dựa trên kết quả phân loại.
    Trả về tên (string) của node sẽ được thực thi tiếp theo.
    """
    classification = state["classification"]

    if classification.category == "spam" or classification.priority == "P3":
        return "archive"

    if classification.requires_action and classification.priority in ["P0", "P1"]:
        return "auto_reply"

    return "human_review"
