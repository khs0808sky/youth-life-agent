from app.rag.vector_store import build_vector_store


def main():
    vector_store = build_vector_store()

    query = "월세지원 신청 대상은 누구야?"

    results = vector_store.similarity_search(query, k=3)

    print("검색 질문:")
    print(query)

    print("\n검색 결과:")
    for idx, doc in enumerate(results, start=1):
        print(f"\n--- 결과 {idx} ---")
        print("출처 파일:", doc.metadata.get("source_file"))
        print("페이지:", doc.metadata.get("page"))
        print(doc.page_content[:500])


if __name__ == "__main__":
    main()