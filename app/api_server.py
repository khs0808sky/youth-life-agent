from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.graph.youth_graph import build_graph


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, description="사용자 질문")


class ChatResponse(BaseModel):
    question: str
    question_type: Optional[str] = None
    need_more_info: bool = False
    missing_info: List[str] = []
    selected_docs: List[str] = []
    retrieved_sources: List[str] = []
    answer: str = ""
    error: Optional[str] = None


app = FastAPI(title="Youth Life Agent API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_graph = build_graph()


def _as_list(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v) for v in value]
    return [str(value)]


@app.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    question = (req.question or "").strip()
    if not question:
        return ChatResponse(
            question="",
            error="질문이 비어 있습니다. 질문을 입력해주세요.",
        )

    try:
        result: Dict[str, Any] = _graph.invoke({"question": question})  # type: ignore[assignment]

        return ChatResponse(
            question=str(result.get("question", question)),
            question_type=result.get("question_type"),
            need_more_info=bool(result.get("need_more_info", False)),
            missing_info=_as_list(result.get("missing_info")),
            selected_docs=_as_list(result.get("selected_docs")),
            retrieved_sources=_as_list(result.get("retrieved_sources")),
            answer=str(result.get("answer", "") or ""),
        )
    except Exception as e:
        return ChatResponse(
            question=question,
            error=f"처리 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요. (원인: {e})",
        )

