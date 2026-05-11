def route_document(state: dict) -> dict:
    """
    질문 유형에 따라 사용할 PDF 문서를 선택하는 노드입니다.
    """

    question_type = state["question_type"]

    if question_type == "housing_support":
        selected_docs = [
            "01_청년월세지원_모집공고_2026.pdf",
            "02_청년월세지원_FAQ_2026.pdf"
        ]

    elif question_type == "rental_fraud":
        selected_docs = [
            "03_전세사기예방_AtoZ.pdf"
        ]

    else:
        selected_docs = []

    return {
        "selected_docs": selected_docs
    }

