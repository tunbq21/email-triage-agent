from langgraph.graph import StateGraph, START, END
from schemas.state import TriageState
from graph.nodes import classifier_node, archive_node, auto_reply_node, human_review_node
from graph.router import route_email


def build_graph():
    """
    Lắp ráp và biên dịch (compile) đồ thị LangGraph cho Email Triage Agent.
    Trả về một compiled graph sẵn sàng để chạy.
    """
    workflow = StateGraph(TriageState)

    # --- Đăng ký các Node ---
    workflow.add_node("classify", classifier_node)
    workflow.add_node("archive", archive_node)
    workflow.add_node("auto_reply", auto_reply_node)
    workflow.add_node("human_review", human_review_node)

    # --- Vẽ các Edges (Đường đi cố định) ---
    workflow.add_edge(START, "classify")

    # --- Vẽ Conditional Edges (Đường rẽ nhánh) ---
    workflow.add_conditional_edges(
        "classify",
        route_email,
        {
            "archive": "archive",
            "auto_reply": "auto_reply",
            "human_review": "human_review"
        }
    )

    # --- Tất cả các node hành động đều kết thúc tại END ---
    workflow.add_edge("archive", END)
    workflow.add_edge("auto_reply", END)
    workflow.add_edge("human_review", END)

    return workflow.compile()
