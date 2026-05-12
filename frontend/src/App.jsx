import { Fragment, useMemo, useState } from 'react'
import './App.css'

function App() {
  const [question, setQuestion] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')

  const canSubmit = useMemo(() => question.trim().length > 0 && !loading, [question, loading])

  async function onSubmit(e) {
    e.preventDefault()
    const q = question.trim()
    if (!q) return

    setLoading(true)
    setError('')
    setResult(null)

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: q }),
      })

      const data = await res.json().catch(() => ({}))
      if (!res.ok) {
        throw new Error(data?.error || '서버 응답에 문제가 있습니다. 잠시 후 다시 시도해주세요.')
      }
      if (data?.error) {
        throw new Error(data.error)
      }

      setResult(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : '요청 처리 중 오류가 발생했습니다.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="page">
      <div className="pageAmbient" aria-hidden="true" />
      <div className="shell">
        <section className="card cardIntro" aria-labelledby="intro-heading">
          <header className="introHeader">
            <p className="introLabel">공공 주거 정보 안내</p>
            <h1 id="intro-heading" className="introTitle">
              청년 주거 안전 지원 AI 에이전트
            </h1>
            <p className="introLead">
              청년월세지원과 전세계약 안전 정보를 문서 근거 기반으로 안내합니다.
            </p>
          </header>
          <ul className="introPills" aria-label="서비스 특징">
            <li className="introPill">문서 근거 기반 답변</li>
            <li className="introPill">질문 유형별 문서 선택</li>
            <li className="introPill">검색 출처 제공</li>
          </ul>
        </section>

        <section className="card cardAsk sectionGap" aria-labelledby="ask-heading">
          <div className="cardHead cardHeadAsk">
            <h2 id="ask-heading" className="cardTitle">
              질문 입력
            </h2>
            <p className="cardDesc">
              청년월세지원 또는 전세계약 관련 질문을 입력해보세요.
            </p>
          </div>
          <form className="askForm" onSubmit={onSubmit}>
            <label className="srOnly" htmlFor="question">
              질문 내용
            </label>
            <textarea
              id="question"
              className="askTextarea"
              placeholder="예) 전세계약 전에 등기부등본에서 어떤 항목을 확인해야 해?"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
            />
            <div className="askActions">
              <button
                className="btn btnGhost"
                type="button"
                disabled={loading || (!question && !result && !error)}
                onClick={() => {
                  setQuestion('')
                  setResult(null)
                  setError('')
                }}
              >
                초기화
              </button>
              <button className="btn btnPrimary" type="submit" disabled={!canSubmit}>
                {loading ? '답변 생성 중…' : '답변 생성'}
              </button>
            </div>
          </form>
          {error ? (
            <div className="alert" role="alert">
              <div className="alertTitle">오류</div>
              <div className="alertBody">{error}</div>
            </div>
          ) : null}
        </section>

        <section className="card cardAnswer sectionGap" aria-labelledby="answer-heading">
          <div className="cardHead">
            <h2 id="answer-heading" className="cardTitle">
              AI 안내 답변
            </h2>
            <p className="cardDesc">문서 검색 결과를 바탕으로 생성된 안내입니다.</p>
          </div>

          {!result && !loading ? (
            <div className="answerEmpty">
              <p className="answerEmptyText">
                질문을 입력하면 문서 근거 기반 답변이 이곳에 표시됩니다.
              </p>
            </div>
          ) : null}

          {loading ? (
            <div className="answerLoading" aria-live="polite">
              <div className="answerLoadingTrack" />
              <p className="answerLoadingNote">관련 문서를 찾고 답변을 준비하고 있습니다.</p>
            </div>
          ) : null}

          {result && !loading ? (
            <div className="answerFlow">
              <div className="pillRow" aria-label="요약">
                {result.question_type ? (
                  <span className="pill pillAccent">{String(result.question_type)}</span>
                ) : (
                  <span className="pill pillMuted">유형 미분류</span>
                )}
                <span className={`pill ${result.need_more_info ? 'pillNavy' : 'pillAccent'}`}>
                  {result.need_more_info ? '추가 정보 필요' : '추가 정보 불필요'}
                </span>
                <SelectedDocPills docs={result.selected_docs} />
                <MissingPills items={result.missing_info} />
              </div>

              <div className="answerBlock">
                <AnswerParagraphs text={result.answer || '답변이 비어 있습니다.'} />
              </div>

              <section className="refsSection" aria-label="참고 문서">
                <h3 className="refsTitle">참고 문서</h3>
                <DocCardGrid sources={result.retrieved_sources} />
              </section>
            </div>
          ) : null}
        </section>

        <footer className="footer">
          문서 근거 기반 안내 결과이며, 실제 신청·계약 전에는 최신 공지 및 원문을 확인하세요.
        </footer>
      </div>
    </div>
  )
}

function SelectedDocPills({ docs }) {
  const list = Array.isArray(docs) ? docs.filter(Boolean) : []
  if (!list.length) return null
  return (
    <>
      {list.map((d, idx) => (
        <span key={`doc-${idx}-${String(d)}`} className="pill pillOutline">
          {String(d)}
        </span>
      ))}
    </>
  )
}

function MissingPills({ items }) {
  const list = Array.isArray(items) ? items.filter(Boolean) : []
  if (!list.length) return null
  return (
    <>
      {list.map((m, idx) => (
        <span key={`miss-${idx}-${String(m)}`} className="pill pillMuted">
          부족: {String(m)}
        </span>
      ))}
    </>
  )
}

function AnswerParagraphs({ text }) {
  const blocks = String(text)
    .split(/\n\s*\n/)
    .map((s) => s.trim())
    .filter(Boolean)

  if (blocks.length === 0) {
    return <p className="answerParagraph">내용이 없습니다.</p>
  }

  return blocks.map((block, i) => (
    <p key={i} className="answerParagraph">
      {block.split('\n').map((line, j, arr) => (
        <Fragment key={j}>
          {line}
          {j < arr.length - 1 ? <br /> : null}
        </Fragment>
      ))}
    </p>
  ))
}

function DocCardGrid({ sources }) {
  const list = Array.isArray(sources) ? sources.filter(Boolean) : []
  if (!list.length) {
    return <p className="refsEmpty">표시할 참고 문서가 없습니다.</p>
  }
  return (
    <div className="docGrid">
      {list.map((src, idx) => (
        <div key={`src-${idx}-${String(src)}`} className="docCard">
          <span className="docCardText">{String(src)}</span>
        </div>
      ))}
    </div>
  )
}

export default App
