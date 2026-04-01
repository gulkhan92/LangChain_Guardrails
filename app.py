from __future__ import annotations

from html import escape

import streamlit as st

from langchain_guardrails_demo.app import GuardrailsApplication
from langchain_guardrails_demo.presentation import build_console_payload


PAGE_CSS = """
<style>
    .stApp {
        background:
            radial-gradient(circle at top left, rgba(255, 181, 71, 0.18), transparent 28%),
            radial-gradient(circle at top right, rgba(0, 168, 150, 0.14), transparent 24%),
            linear-gradient(180deg, #f4efe6 0%, #f7f3ec 45%, #efe7dc 100%);
        color: #1d1d1f;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1120px;
    }
    .hero {
        padding: 2rem 2.2rem;
        border-radius: 28px;
        background: rgba(255, 252, 246, 0.82);
        border: 1px solid rgba(46, 77, 74, 0.12);
        box-shadow: 0 24px 80px rgba(84, 63, 44, 0.12);
        backdrop-filter: blur(12px);
        margin-bottom: 1.25rem;
    }
    .hero h1 {
        margin: 0;
        font-size: 2.6rem;
        line-height: 1.05;
        letter-spacing: -0.04em;
        color: #16302b;
    }
    .hero p {
        margin: 0.9rem 0 0;
        max-width: 760px;
        font-size: 1rem;
        line-height: 1.7;
        color: #4c5a57;
    }
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 0.9rem;
        margin: 1.25rem 0 1.4rem;
    }
    .metric-card, .result-card, .history-card {
        background: rgba(255, 255, 255, 0.7);
        border: 1px solid rgba(34, 70, 66, 0.1);
        border-radius: 22px;
        padding: 1rem 1.1rem;
        box-shadow: 0 14px 40px rgba(73, 57, 43, 0.08);
    }
    .metric-label {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #6c7a76;
    }
    .metric-value {
        margin-top: 0.45rem;
        font-size: 1.15rem;
        font-weight: 600;
        color: #17332e;
    }
    .section-title {
        font-size: 0.86rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #6f6b63;
        margin-bottom: 0.75rem;
    }
    .answer-text {
        font-size: 1rem;
        line-height: 1.75;
        color: #222224;
        white-space: pre-wrap;
    }
    .pill {
        display: inline-block;
        margin: 0 0.45rem 0.45rem 0;
        padding: 0.45rem 0.75rem;
        border-radius: 999px;
        background: #ecf4f2;
        color: #214840;
        border: 1px solid rgba(33, 72, 64, 0.08);
        font-size: 0.9rem;
    }
    .history-card + .history-card {
        margin-top: 0.8rem;
    }
    .history-question {
        margin: 0 0 0.5rem;
        font-weight: 600;
        color: #18342e;
    }
    .history-answer {
        margin: 0;
        color: #4c5b58;
        line-height: 1.6;
    }
    @media (max-width: 900px) {
        .metric-grid {
            grid-template-columns: 1fr;
        }
        .hero h1 {
            font-size: 2rem;
        }
    }
</style>
"""


def render_badges(items: list[str]) -> str:
    if not items:
        return "<span class='pill'>None</span>"
    return "".join(f"<span class='pill'>{escape(item)}</span>" for item in items)


def render_history() -> None:
    history = st.session_state.get("history", [])
    if not history:
        return

    st.markdown("### Recent Runs")
    for item in reversed(history[-5:]):
        st.markdown(
            f"""
            <div class="history-card">
                <p class="history-question">{escape(item["prompt"])}</p>
                <p class="history-answer">{escape(item["answer"])}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def main() -> None:
    st.set_page_config(
        page_title="LangChain Guardrails Studio",
        page_icon="🛡️",
        layout="wide",
    )
    st.markdown(PAGE_CSS, unsafe_allow_html=True)

    st.markdown(
        """
        <section class="hero">
            <h1>LangChain Guardrails Studio</h1>
            <p>
                Run general inference requests through a guarded Gemini workflow with
                input filtering, PII handling, structured output, and final-response
                safety review.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-label">Model Provider</div>
                <div class="metric-value">Google Gemini</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Guardrail Layers</div>
                <div class="metric-value">Input, PII, Output</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Response Contract</div>
                <div class="metric-value">Pydantic Structured Output</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if "history" not in st.session_state:
        st.session_state.history = []

    with st.form("inference-form", clear_on_submit=False):
        prompt = st.text_area(
            "Prompt",
            height=180,
            placeholder="Ask for a summary, explanation, or other general inference request.",
        )
        submitted = st.form_submit_button("Run Inference", use_container_width=True)

    if submitted:
        if not prompt.strip():
            st.error("Enter a prompt before running inference.")
        else:
            with st.spinner("Running guarded inference..."):
                try:
                    application = GuardrailsApplication()
                    result = application.run(prompt.strip())
                    payload = build_console_payload(result)
                    st.session_state.history.append(
                        {
                            "prompt": prompt.strip(),
                            "answer": payload.get("answer")
                            or payload.get("message")
                            or "No answer returned.",
                        }
                    )
                except Exception as exc:
                    st.error(f"Inference failed: {exc}")
                else:
                    st.success("Inference completed.")
                    st.markdown(
                        f"""
                        <div class="result-card">
                            <div class="section-title">Topic</div>
                            <div class="answer-text">{escape(str(payload.get("topic", "N/A")))}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        f"""
                        <div class="result-card">
                            <div class="section-title">Answer</div>
                            <div class="answer-text">{escape(str(payload.get("answer") or payload.get("message") or "No answer returned."))}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(
                            f"""
                            <div class="result-card">
                                <div class="section-title">Safety Notes</div>
                                {render_badges(payload.get("safety_notes", []))}
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                    with col2:
                        st.markdown(
                            f"""
                            <div class="result-card">
                                <div class="section-title">Sources</div>
                                {render_badges(payload.get("sources", []))}
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                    with st.expander("Raw Response"):
                        st.json(payload)

    render_history()


if __name__ == "__main__":
    main()
