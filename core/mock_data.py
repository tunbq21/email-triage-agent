from schemas.email import EmailInput

def get_mock_emails() -> list[EmailInput]:
    """Trả về danh sách email mẫu để kiểm tra."""
    return [
        EmailInput(
            id="mock_1",
            sender="boss@company.com",
            subject="Khẩn cấp: Lỗi hệ thống trên Production",
            body="Hệ thống đang sập. Em vào kiểm tra server ngay nhé, client đang réo.",
            date="2023-10-27T10:00:00Z"
        ),
        EmailInput(
            id="mock_2",
            sender="newsletter@marketing.com",
            subject="Top 10 AI Tools năm 2023",
            body="Khám phá ngay danh sách các công cụ AI không thể bỏ lỡ trong năm nay...",
            date="2023-10-27T08:00:00Z"
        ),
        EmailInput(
            id="mock_3",
            sender="hr@company.com",
            subject="Nhắc nhở: Cập nhật thông tin BHXH",
            body="Chào mọi người, vui lòng điền form thông tin BHXH trước ngày 30/10 nhé. Cảm ơn.",
            date="2023-10-26T15:30:00Z"
        ),
        EmailInput(
            id="mock_4",
            sender="spammer@unknown.net",
            subject="🎉 Bạn đã trúng giải thưởng 1 TRIỆU ĐÔ",
            body="Click vào link sau để nhận thưởng ngay lập tức: http://spam-link.net",
            date="2023-10-25T11:11:11Z"
        ),
    ]
