from langchain_core.prompts import PromptTemplate
from schemas.email import EmailInput
from schemas.classification import ClassificationResult
from services.llm import get_llm

classification_template = """
Bạn là một trợ lý AI quản lý hộp thư đến xuất sắc. Nhiệm vụ của bạn là phân loại email sau đây:

THÔNG TIN EMAIL:
- Người gửi: {sender}
- Tiêu đề: {subject}
- Ngày nhận: {date}
- Nội dung:
{body}

Hãy phân tích email và trả về kết quả phân loại dựa trên các tiêu chí sau:
- category: work (công việc), personal (cá nhân), spam (rác), newsletter (bản tin), promotion (quảng cáo).
- priority: P0 (khẩn cấp, sập hệ thống, sếp gọi gấp), P1 (quan trọng, cần làm trong ngày), P2 (bình thường), P3 (không quan trọng).
- confidence: Độ tự tin của bạn (0.0 đến 1.0).
- reasoning: Giải thích ngắn gọn tại sao.
- requires_action: True nếu email yêu cầu người dùng phải làm gì đó (trả lời, kiểm tra, xác nhận), False nếu chỉ là email thông báo/FYI.
"""

_prompt = PromptTemplate(
    template=classification_template,
    input_variables=["sender", "subject", "date", "body"]
)


def get_classifier_chain():
    """Khởi tạo và trả về LCEL chain phân loại email."""
    llm = get_llm(temperature=0)
    structured_llm = llm.with_structured_output(ClassificationResult)
    return _prompt | structured_llm


def classify_email(email: EmailInput) -> ClassificationResult:
    """Phân loại một email và trả về kết quả có cấu trúc."""
    chain = get_classifier_chain()
    return chain.invoke({
        "sender": email.sender,
        "subject": email.subject,
        "date": email.date,
        "body": email.body
    })
