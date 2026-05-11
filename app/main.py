from app.graph.youth_graph import build_graph


def main():
    graph = build_graph()

    #question = "서울 사는 27살인데 월세지원 받을 수 있어?"
    question = "서울 사는 27살이고 소득 정보도 확인했는데 월세지원 받을 수 있어?"

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

    print("\n최종 답변:")
    print(result.get("answer"))


if __name__ == "__main__":
    main()