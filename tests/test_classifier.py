import pytest
import os
from dotenv import load_dotenv

from core.mock_data import get_mock_emails
from chains.classifier import classify_email_chain

# Đảm bảo load biến môi trường để lấy GOOGLE_API_KEY
load_dotenv()

@pytest.fixture
def mock_emails():
    """Fixture cung cấp danh sách email giả lập."""
    return {email.id: email for email in get_mock_emails()}

# Skip tests nếu chưa có API Key
pytestmark = pytest.mark.skipif(
    not os.getenv("GOOGLE_API_KEY"),
    reason="Cần GOOGLE_API_KEY để chạy các test liên quan tới LLM"
)

def test_urgent_system_error_email(mock_emails):
    """Test case: Email khẩn cấp báo sập hệ thống (P0)"""
    email = mock_emails["mock_1"]
    result = classify_email_chain(email)
    
    assert result.category == "work", "Phải là email công việc"
    assert result.priority in ["P0", "P1"], "Lỗi sập hệ thống phải là độ ưu tiên cao nhất"
    assert result.requires_action is True, "Phải yêu cầu hành động (sửa lỗi)"
    assert result.confidence > 0.7, "LLM phải khá chắc chắn về case rõ ràng này"

def test_newsletter_email(mock_emails):
    """Test case: Email bản tin quảng cáo, không quan trọng (P3)"""
    email = mock_emails["mock_2"]
    result = classify_email_chain(email)
    
    assert result.category in ["newsletter", "promotion"], "Phải là bản tin hoặc quảng cáo"
    assert result.priority == "P3", "Bản tin thì priority thấp nhất"
    assert result.requires_action is False, "Đọc bản tin không yêu cầu phải làm gì gấp"

def test_internal_hr_reminder(mock_emails):
    """Test case: Nhắc nhở từ HR (P2, cần điền form)"""
    email = mock_emails["mock_3"]
    result = classify_email_chain(email)
    
    assert result.category == "work", "Thông báo từ HR là công việc"
    assert result.priority in ["P1", "P2"], "Nhắc nhở điền form có thể là P1 (nếu hạn gấp) hoặc P2"
    assert result.requires_action is True, "Cần phải điền form (hành động)"

def test_spam_scam_email(mock_emails):
    """Test case: Email lừa đảo trúng thưởng (spam)"""
    email = mock_emails["mock_4"]
    result = classify_email_chain(email)
    
    assert result.category == "spam", "Email trúng thưởng đáng ngờ phải bị đánh dấu spam"
    assert result.priority == "P3", "Spam không có độ ưu tiên"
    assert result.requires_action is False, "Không được phép tương tác với email lừa đảo"
