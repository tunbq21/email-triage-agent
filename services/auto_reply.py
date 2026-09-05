from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from services.llm import get_llm

auto_reply_template = """
Bạn là một trợ lý AI thông minh đang quản lý hòm thư.
Hãy soạn một email phản hồi lịch sự, chuyên nghiệp, và ngắn gọn dựa trên email gốc dưới đây.

THÔNG TIN EMAIL GỐC:
- Người gửi: {sender}
- Tiêu đề: {subject}
- Nội dung:
{body}

CÁCH PHẢN HỒI:
- Trả lời trực tiếp vào vấn đề.
- Thông báo cho người gửi biết rằng email của họ đã được đánh dấu ưu tiên ({priority}) và sẽ có người kiểm tra ngay.
- Ký tên là "Trợ lý AI Triage".
"""

_prompt = PromptTemplate(
    template=auto_reply_template,
    input_variables=["sender", "subject", "body", "priority"]
)


def get_auto_reply_chain():
    """Khởi tạo chain cho tính năng tự động phản hồi."""
    llm = get_llm(temperature=0.5)
    return _prompt | llm | StrOutputParser()


def generate_auto_reply(email_data: dict) -> str:
    """Soạn thảo thư phản hồi tự động dựa trên nội dung email gốc."""
    chain = get_auto_reply_chain()
    return chain.invoke(email_data)
