from typing import TypedDict, List

from langgraph.graph import StateGraph, START, END

from app.nodes.classify_node import classify_question
from app.nodes.info_check_node import check_required_info
from app.nodes.route_node import route_document
from app.nodes.answer_node import generate_answer
from app.nodes.ask_more_info_node import ask_more_info


class YouthState(TypedDict):
    question: str
    question_type: str
    missing_info: List[str]
    need_more_info: bool
    selected_docs: List[str]
    answer: str


def route_after_info_check(state: YouthState) -> str:
    """
    정보 확인 결과에 따라 다음 노드를 결정합니다.
    """

    if state["need_more_info"]:
        return "ask_more_info"

    return "route_document"


def build_graph():
    graph_builder = StateGraph(YouthState)

    graph_builder.add_node("classify_question", classify_question)
    graph_builder.add_node("check_required_info", check_required_info)
    graph_builder.add_node("ask_more_info", ask_more_info)
    graph_builder.add_node("route_document", route_document)
    graph_builder.add_node("generate_answer", generate_answer)

    graph_builder.add_edge(START, "classify_question")
    graph_builder.add_edge("classify_question", "check_required_info")

    graph_builder.add_conditional_edges(
        "check_required_info",
        route_after_info_check,
        {
            "ask_more_info": "ask_more_info",
            "route_document": "route_document"
        }
    )

    graph_builder.add_edge("ask_more_info", END)
    graph_builder.add_edge("route_document", "generate_answer")
    graph_builder.add_edge("generate_answer", END)

    graph = graph_builder.compile()

    return graph