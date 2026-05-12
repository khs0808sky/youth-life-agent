def check_required_info(state: dict) -> dict:
    """
    질문 유형에 따라 필요한 정보가 충분한지 확인하는 노드입니다.
    """

    question = state["question"]
    question_type = state["question_type"]

    missing_info = []

    if question_type == "housing_support":
        if not any(word in question for word in ["살", "세", "나이"]):
            missing_info.append("나이")

        if "서울" not in question:
            missing_info.append("거주 지역")

        if "소득" not in question:
            missing_info.append("소득 정보")

    elif question_type == "rental_fraud":
        if not any(word in question for word in ["근저당", "등기부", "보증금", "집주인", "임대인"]):
            missing_info.append("계약 위험 확인 정보")

    need_more_info = len(missing_info) > 0

    return {
        "missing_info": missing_info,
        "need_more_info": need_more_info
    }