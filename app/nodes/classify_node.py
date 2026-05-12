def classify_question(state: dict) -> dict:
    """
    사용자 질문을 보고 질문 유형을 분류하는 노드입니다.
    """

    question = state["question"]

    if "월세" in question or "월세지원" in question:
        question_type = "housing_support"

    elif "전세" in question or "계약" in question or "사기" in question:
        question_type = "rental_fraud"

    else:
        question_type = "general"

    return {
        "question_type": question_type
    }