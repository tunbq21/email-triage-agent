from typing import TypedDict, Optional
from schemas.email import EmailInput
from schemas.classification import ClassificationResult

class TriageState(TypedDict):
    """Trạng thái (State) được truyền qua các node trong LangGraph."""
    current_email: EmailInput
    classification: Optional[ClassificationResult]
    action_taken: Optional[str]
    draft_reply: Optional[str]
