from typing import Literal
from pydantic import BaseModel, Field

class ClassificationResult(BaseModel):
    """Kết quả phân loại email từ LLM."""
    category: Literal["work", "personal", "spam", "newsletter", "promotion"] = Field(
        ..., description="Phân loại chính của email"
    )
    priority: Literal["P0", "P1", "P2", "P3"] = Field(
        ..., description="Mức độ ưu tiên: P0 (khẩn cấp), P1 (quan trọng), P2 (bình thường), P3 (không quan trọng)"
    )
    confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Độ tự tin của mô hình (từ 0.0 đến 1.0)"
    )
    reasoning: str = Field(
        ..., description="Giải thích ngắn gọn tại sao lại chọn category và priority này"
    )
    requires_action: bool = Field(
        ..., description="Email này có cần người dùng (hoặc hệ thống) phản hồi/hành động không?"
    )
