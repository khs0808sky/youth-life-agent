from app.graph.youth_graph import build_graph


def main():
    graph = build_graph()

    #question = "서울 사는 27살이고 소득 정보도 확인했는데 월세지원 신청 대상은 누구야?"
    question = "전세계약 전에 등기부등본이랑 근저당을 확인해야 해?"

    result = graph.invoke({
        "question": question
    })

    print("사용자 질문:")
    print(result.get("question"))

    print("\n질문 유형:")
    print(result.get("question_type"))

    print("\n추가 확인 필요 여부:")
    print(result.get("need_more_info"))

    print("\n부족한 정보:")
    print(result.get("missing_info", []))

    print("\n선택된 문서:")
    print(result.get("selected_docs", []))

    print("\n검색 출처:")
    print(result.get("retrieved_sources", []))

    print("\n검색된 문서 일부:")
    print(result.get("retrieved_context", "")[:1000])

    print("\n최종 답변:")
    print(result.get("answer"))


if __name__ == "__main__":
    main()