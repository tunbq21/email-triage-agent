import os
from langchain_google_genai import ChatGoogleGenerativeAI


def get_llm(temperature: float = 0.0) -> ChatGoogleGenerativeAI:
    """
    Khởi tạo và cấu hình mô hình LLM chính của hệ thống (Gemini).
    Tập trung logic lấy API key và tên model ở một nơi duy nhất.
    """
    model_name = os.getenv("GEMINI_MODEL_NAME", "gemini-3.6-flash")
    llm = ChatGoogleGenerativeAI(model=model_name, temperature=temperature)
    return llm
