from app.rag.vector_store import load_vector_store


def make_search_query(state: dict) -> str:
    """
    사용자 질문을 그대로 검색하지 않고,
    질문 유형에 맞게 검색 키워드를 보강합니다.
    """

    question = state["question"]
    question_type = state.get("question_type")

    if question_type == "housing_support":
        return (
            f"{question} "
            "청년월세지원 지원대상 신청대상 신청일 기준 서울시 월세 거주 "
            "19세 39세 이하 청년 소득 기준 신청 자격 제출서류"
        )

    if question_type == "rental_fraud":
        return (
            f"{question} "
            "전세계약 전 확인사항 등기부등본 근저당 보증금 집주인 임대인 확인 "
            "전세사기 예방 체크리스트 깡통주택 전세가율"
        )

    return question


def retrieve_documents(state: dict) -> dict:
    """
    선택된 PDF 문서 안에서 사용자 질문과 관련된 chunk를 검색하는 노드입니다.
    """

    selected_docs = state.get("selected_docs", [])

    if not selected_docs:
        return {
            "retrieved_context": "",
            "retrieved_sources": []
        }

    search_query = make_search_query(state)

    vector_store = load_vector_store()

    try:
        results = vector_store.similarity_search(
            search_query,
            k=5,
            filter={
                "source_file": {
                    "$in": selected_docs
                }
            }
        )

    except Exception:
        all_results = vector_store.similarity_search(search_query, k=10)

        results = [
            doc for doc in all_results
            if doc.metadata.get("source_file") in selected_docs
        ][:5]

    context_list = []
    source_list = []

    for doc in results:
        source_file = doc.metadata.get("source_file", "unknown")
        page = doc.metadata.get("page", 0) + 1

        source_text = f"{source_file} / {page}페이지"
        source_list.append(source_text)

        context_list.append(
            f"[출처: {source_text}]\n{doc.page_content}"
        )

    retrieved_context = "\n\n".join(context_list)

    return {
        "retrieved_context": retrieved_context,
        "retrieved_sources": source_list
    }