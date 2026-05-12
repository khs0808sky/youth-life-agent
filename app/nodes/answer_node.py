from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


def generate_answer(state: dict) -> dict:
    """
    RAG 검색 결과를 LLM에게 전달해
    사용자에게 자연스러운 답변을 생성하는 노드입니다.
    """

    load_dotenv()

    question = state["question"]
    question_type = state["question_type"]
    missing_info = state["missing_info"]
    need_more_info = state["need_more_info"]
    selected_docs = state.get("selected_docs", [])
    retrieved_context = state.get("retrieved_context", "")
    retrieved_sources = state.get("retrieved_sources", [])

    if question_type == "general":
        answer = (
            "현재 준비된 문서 범위에서는 답변하기 어려운 질문입니다.\n"
            "청년월세지원 또는 전세사기 예방과 관련된 질문을 입력해주세요."
        )

        return {
            "answer": answer
        }

    if need_more_info:
        answer = (
            "현재 질문만으로는 정확한 안내가 어렵습니다.\n"
            f"추가로 확인이 필요한 정보: {', '.join(missing_info)}"
        )

        return {
            "answer": answer
        }

    if not retrieved_context:
        answer = (
            f"질문 유형: {question_type}\n"
            f"선택된 문서: {', '.join(selected_docs)}\n"
            "선택된 문서에서 관련 내용을 찾지 못했습니다."
        )

        return {
            "answer": answer
        }

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    prompt = f"""
당신은 청년 주거지원과 전세계약 안전 정보를 안내하는 AI 상담 도우미입니다.

아래 사용자 질문에 대해 [검색된 문서 근거]만 참고해서 답변하세요.
문서에 없는 내용은 추측하지 말고 "문서에서 확인되지 않습니다"라고 말하세요.
단, 문서에 지원대상, 신청조건, 제출서류, 전세계약 확인사항이 포함되어 있다면 그 내용을 쉽게 요약하세요.

주의사항:
- 검색 출처에 없는 URL을 임의로 만들지 마세요.
- 사용자의 최종 가능 여부를 단정하지 말고, 확인 가능한 조건과 추가 확인이 필요한 조건을 나누어 설명하세요.
- 참고 출처는 Python 리스트 형태로 쓰지 말고, 줄바꿈 목록으로 정리하세요.

답변 형식:

1. 간단한 답변
2. 문서에서 확인한 기준
3. 추가로 확인할 점
4. 참고 출처
- 파일명 / 페이지 형식으로 줄바꿈 목록 작성

[사용자 질문]
{question}

[질문 유형]
{question_type}

[선택된 문서]
{selected_docs}

[검색된 문서 근거]
{retrieved_context}

[검색 출처]
{retrieved_sources}
"""

    response = llm.invoke(prompt)

    return {
        "answer": response.content
    }