# Youth Life Agent

청년 **주거·생활지원·전세계약** 관련 질문에 대해, 사용자 상황을 점검하고 **공개 자료(PDF)** 를 검색한 뒤 **문서 근거**로 답하는 **LangGraph** 기반 AI 에이전트입니다.

> 이 저장소는 학습·데모용 프로젝트입니다. 실제 신청·계약·법률 판단은 반드시 공식 안내와 전문가 상담을 따르세요.

---

## 이 프로젝트가 하는 일

일반적인 RAG는 “문서를 찾아서 답한다”에 가깝습니다. 여기서는 **LangGraph**로 다음 순서를 **노드(단계)** 로 나눕니다.

1. **질문 분류** — 월세지원, 청년수당, 전세·계약 안전 등 유형 파악  
2. **필요 정보 확인** — 답하려면 더 필요한 정보가 있는지 판단  
3. **분기** — 정보가 부족하면 안내 메시지로 종료 / 충분하면 다음 단계로  
4. **문서 라우팅** — 질문에 맞는 PDF 쪽으로 검색 범위를 좁힘  
5. **검색(RAG)** — ChromaDB에서 관련 구절 검색  
6. **답변 생성** — 검색된 내용을 바탕으로 답변과 출처 정리  

이렇게 하면 “항상 같은 검색”이 아니라, **질문 종류와 사용자 정보 상태**에 따라 흐름이 달라질 수 있습니다.

---

## 주요 기능

| 구분 | 설명 |
|------|------|
| 질문 유형 분류 | 질문을 주제별로 나누어 이후 단계에 활용 |
| 정보 부족 시 안내 | 나이·지역·소득 등이 더 필요하면 `need_more_info`와 `missing_info`로 알림 |
| 문서 라우팅 | 질문 유형에 맞는 자료 쪽으로 검색 |
| PDF RAG | `data/raw_pdfs`의 PDF를 잘게 나눈 뒤 벡터 DB에 저장·검색 |
| CLI 실행 | `app/main.py`에서 그래프를 직접 호출해 터미널에 결과 출력 |
| REST API | FastAPI `POST /api/chat` |
| 웹 UI | React(Vite) — 개발 시 API로 프록시 연결 |

---

## 기술 스택

- **Python** · **LangGraph** · **LangChain**  
- **ChromaDB** (로컬 벡터 저장)  
- **OpenAI** (임베딩·채팅 등, API 키 필요)  
- **FastAPI** · **Uvicorn**  
- **React 19** · **Vite 8** (프론트엔드)

---

## 사용 자료(예시)

- 2026년 서울시 청년월세지원 모집 공고  
- 2026년 서울시 청년월세지원 FAQ  
- 전세사기 예방 A to Z  
- 청년수당 참여자 안내책자  

실제 파일은 **`data/raw_pdfs`** 에 PDF로 두면 로더가 읽습니다.

---

## 프로젝트 구조(요약)

```text
youth-life-agent/
├── app/
│   ├── main.py              # CLI 데모 진입점
│   ├── api_server.py        # FastAPI 서버
│   ├── graph/youth_graph.py   # LangGraph 정의
│   ├── nodes/               # 분류·정보확인·라우팅·검색·답변 등
│   └── rag/                 # PDF 로드, Chroma 벡터 스토어
├── data/
│   ├── raw_pdfs/            # 여기에 PDF 배치
│   └── vector_db/           # Chroma 저장 위치(생성 후 생김)
├── frontend/                # Vite + React UI
├── requirements.txt
├── visualize_graph.py       # 그래프 PNG 저장(선택)
└── test_*.py                # 벡터·PDF 등 단순 검증용
```

---

## 사전 준비

- **Python 3.10+** 권장  
- **Node.js 20+** (프론트 실행 시)  
- **OpenAI API 키** — 임베딩·모델 호출에 사용  

프로젝트 루트에 `.env` 파일을 만들고 다음을 넣습니다.

```env
OPENAI_API_KEY=sk-...
```

`.env`는 Git에 올리지 마세요(`.gitignore`에 포함되어 있습니다).

---

## 설치

**백엔드(루트 디렉터리에서)**

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
# source .venv/bin/activate

pip install -r requirements.txt
```

`langchain_text_splitters` 관련 import 오류가 나면 다음을 추가로 설치하세요.

```bash
pip install langchain-text-splitters
```

**프론트엔드**

```bash
cd frontend
npm install
```

---

## 벡터 DB 만들기(최초 1회 또는 PDF 변경 시)

`data/raw_pdfs`에 PDF를 넣은 뒤, 아래 중 하나를 실행합니다.

```bash
python test_vector_store.py
```

또는 코드에서 `build_vector_store()`를 호출해 `data/vector_db/...` 아래에 Chroma 데이터가 생성되면, 검색 노드가 그 저장소를 사용할 수 있습니다.

---

## 실행 방법

### 1) 터미널에서만 테스트 (CLI)

`app/main.py`의 `question` 문자열을 바꾼 뒤:

```bash
python -m app.main
```

출력에는 질문 유형, 부족한 정보, 선택 문서, 검색 출처, 답변 등이 포함됩니다.

### 2) API 서버

```bash
uvicorn app.api_server:app --reload --host 0.0.0.0 --port 8000
```

- **엔드포인트:** `POST http://localhost:8000/api/chat`  
- **본문(JSON):** `{ "question": "질문 내용" }`

### 3) 웹 UI + API 함께 쓰기

1. 터미널 A: 위와 같이 Uvicorn을 **8000** 포트로 실행  
2. 터미널 B:

```bash
cd frontend
npm run dev
```

Vite는 기본적으로 **5173**에서 뜨고, `/api` 요청은 `vite.config.js` 설정에 따라 **localhost:8000**으로 프록시됩니다.

---

## LangGraph 흐름 시각화(선택)

Graphviz 등 Mermaid PNG 생성에 필요한 환경이 갖춰져 있다면:

```bash
python visualize_graph.py
```

실행 후 `langgraph_flow.png`가 생성됩니다.

---

## 관련 스크립트

| 파일 | 용도 |
|------|------|
| `test_vector_store.py` | 벡터 스토어 구축 후 간단 유사도 검색 |
| `test_pdf_loader.py` | PDF 로딩·분할 동작 확인 |

---

## 라이선스·면책

이 프로젝트의 답변은 **공개 자료 검색 결과를 바탕으로 한 AI 생성물**입니다. 최신 모집 요건·법령·지자체 안내는 **공식 사이트·공고문**을 확인하시고, 전세·계약·분쟁은 **등기·법률 전문가** 등에게 문의하세요.

---

**Youth Life Agent** — 청년 주거 정보를 질문 유형과 자료 근거에 맞춰 안내하는 LangGraph 에이전트 데모입니다.
