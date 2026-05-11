def ask_more_info(state: dict) -> dict:
    """
    정보가 부족할 때 사용자에게 추가 정보를 요청하는 노드입니다.
    """

    missing_info = state["missing_info"]

    answer = (
        "현재 질문만으로는 정확한 안내가 어렵습니다.\n"
        f"추가로 확인이 필요한 정보: {', '.join(missing_info)}\n"
        "위 정보를 함께 알려주시면 더 정확하게 안내할 수 있습니다."
    )

    return {
        "answer": answer
    }