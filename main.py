from dotenv import load_dotenv
import os
from langgraph.graph import StateGraph, START, END

# Import schemas and nodes
from schemas.state import TriageState
from agents.classifier_node import classifier_node
from core.mock_data import get_mock_emails

def build_graph():
    """Xây dựng LangGraph cho Email Triage Agent."""
    # Khởi tạo đồ thị với state schema
    workflow = StateGraph(TriageState)
    
    # Thêm các node
    workflow.add_node("classify", classifier_node)
    
    # Định nghĩa luồng cơ bản: START -> classify -> END
    workflow.add_edge(START, "classify")
    workflow.add_edge("classify", END)
    
    # Compile graph
    app = workflow.compile()
    return app

def main():
    # Load biến môi trường
    load_dotenv()
    
    # Kiểm tra API Key
    if not os.getenv("GOOGLE_API_KEY"):
        print("Lỗi: Không tìm thấy GOOGLE_API_KEY trong biến môi trường (.env)")
        return
        
    print("Khởi tạo Email Triage Agent (Phase 1)...")
    app = build_graph()
    
    # Lấy mock data
    emails = get_mock_emails()
    
    # Chạy thử với từng email
    for email in emails:
        # Khởi tạo state ban đầu
        initial_state = {"current_email": email}
        
        # Chạy graph
        result = app.invoke(initial_state)
        
        # In kết quả
        classification = result["classification"]
        print(f"=> Category: {classification.category.upper()}")
        print(f"=> Priority: {classification.priority}")
        print(f"=> Confidence: {classification.confidence}")
        print(f"=> Requires Action: {classification.requires_action}")
        print(f"=> Reasoning: {classification.reasoning}")
        print("-" * 50)

if __name__ == "__main__":
    main()
