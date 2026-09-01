from pydantic import BaseModel, Field

class EmailInput(BaseModel):
    """Mô hình dữ liệu cho một email đầu vào."""
    id: str = Field(..., description="ID duy nhất của email")
    sender: str = Field(..., description="Địa chỉ email của người gửi")
    subject: str = Field(..., description="Tiêu đề email")
    body: str = Field(..., description="Nội dung chính của email")
    date: str = Field(..., description="Ngày giờ nhận email")
