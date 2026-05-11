def generate_answer(state: dict) -> dict:
    """
    현재까지 정리된 정보를 바탕으로 임시 답변을 생성하는 노드입니다.
    아직 실제 RAG 검색은 연결하지 않았습니다.
    """

    question_type = state["question_type"]
    missing_info = state["missing_info"]
    need_more_info = state["need_more_info"]
    selected_docs = state["selected_docs"]

    if question_type == "general":
        answer = (
            "현재 준비된 문서 범위에서는 답변하기 어려운 질문입니다.\n"
            "청년월세지원 또는 전세사기 예방과 관련된 질문을 입력해주세요."
        )

    elif need_more_info:
        answer = (
            "현재 질문만으로는 정확한 안내가 어렵습니다.\n"
            f"추가로 확인이 필요한 정보: {', '.join(missing_info)}\n"
            f"참고 예정 문서: {', '.join(selected_docs)}"
        )

    else:
        answer = (
            f"질문 유형: {question_type}\n"
            f"선택된 문서: {', '.join(selected_docs)}\n"
            "해당 문서를 기반으로 답변을 생성할 수 있습니다."
        )

    return {
        "answer": answer
    }