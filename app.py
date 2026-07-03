import streamlit as st
import html
from pipeline import run_research_pipeline

# ── Page Config ──────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchIQ · Multi-Agent Research System",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Custom CSS ────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

/* Base */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0a0a0f;
    color: #e8e8f0;
}

.stApp {
    background: #0a0a0f;
}

/* Hide Streamlit defaults */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 2rem 3rem 4rem 3rem;
    max-width: 1100px;
}

/* ── Hero Header ── */
.hero {
    text-align: center;
    padding: 3rem 0 2rem 0;
    border-bottom: 1px solid #1e1e2e;
    margin-bottom: 2.5rem;
}
.hero-badge {
    display: inline-block;
    background: linear-gradient(135deg, #1a1a2e, #16213e);
    border: 1px solid #7c3aed44;
    color: #a78bfa;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 0.35rem 1rem;
    border-radius: 100px;
    margin-bottom: 1.2rem;
}
.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 3rem;
    font-weight: 700;
    background: linear-gradient(135deg, #e8e8f0 0%, #a78bfa 50%, #60a5fa 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.15;
    margin-bottom: 0.8rem;
}
.hero-sub {
    color: #6b7280;
    font-size: 1rem;
    font-weight: 400;
    max-width: 520px;
    margin: 0 auto;
    line-height: 1.6;
}

/* ── Agent Pipeline Visual ── */
.pipeline {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0;
    margin: 2rem 0 2.5rem 0;
    flex-wrap: wrap;
}
.agent-node {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.4rem;
}
.agent-icon {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
    border: 1px solid #1e1e2e;
}
.agent-icon.search { background: #1a1a2e; border-color: #7c3aed44; }
.agent-icon.reader { background: #0f1e2e; border-color: #3b82f644; }
.agent-icon.writer { background: #0f2e1a; border-color: #10b98144; }
.agent-icon.critic { background: #2e1a0f; border-color: #f59e0b44; }
.agent-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: #6b7280;
}
.pipeline-arrow {
    color: #2d2d3d;
    font-size: 1.2rem;
    padding: 0 0.6rem;
    padding-bottom: 1.2rem;
}

/* ── Search Box ── */
.stTextInput > div > div > input {
    background: #111118 !important;
    border: 1px solid #1e1e2e !important;
    border-radius: 12px !important;
    color: #e8e8f0 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.85rem 1.2rem !important;
    transition: border-color 0.2s ease !important;
}
.stTextInput > div > div > input:focus {
    border-color: #7c3aed !important;
    box-shadow: 0 0 0 3px #7c3aed18 !important;
}
.stTextInput > div > div > input::placeholder {
    color: #3d3d52 !important;
}

/* ── Button ── */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 2rem !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.02em !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 25px #7c3aed44 !important;
}

/* ── Step Cards ── */
.step-card {
    background: #111118;
    border: 1px solid #1e1e2e;
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.2rem;
}
.step-header {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin-bottom: 0.8rem;
}
.step-number {
    background: linear-gradient(135deg, #7c3aed22, #4f46e522);
    border: 1px solid #7c3aed44;
    color: #a78bfa;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    padding: 0.2rem 0.6rem;
    border-radius: 6px;
}
.step-title {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
    font-size: 0.95rem;
    color: #e8e8f0;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #111118;
    border-radius: 10px;
    padding: 0.3rem;
    border: 1px solid #1e1e2e;
    gap: 0.2rem;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #6b7280 !important;
    border-radius: 8px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    padding: 0.5rem 1rem !important;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    background: #1e1e2e !important;
    color: #a78bfa !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: #111118;
    border: 1px solid #1e1e2e;
    border-radius: 12px;
    padding: 1.5rem;
    margin-top: 0.5rem;
}

/* ── Score Badge ── */
.score-badge {
    display: inline-block;
    background: linear-gradient(135deg, #f59e0b22, #d9770022);
    border: 1px solid #f59e0b44;
    color: #fbbf24;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    padding: 0.5rem 1.2rem;
    border-radius: 10px;
    margin-bottom: 1rem;
}

/* ── Download Button ── */
.stDownloadButton > button {
    background: #1e1e2e !important;
    color: #a78bfa !important;
    border: 1px solid #7c3aed44 !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.85rem !important;
}
.stDownloadButton > button:hover {
    background: #2d2d3d !important;
    border-color: #7c3aed !important;
}

/* ── Progress / Spinner ── */
.stSpinner > div {
    border-color: #7c3aed !important;
}

.progress-card {
    background: #111118;
    border: 1px solid #1e1e2e;
    border-radius: 12px;
    padding: 1rem 1.1rem;
    margin-bottom: 1rem;
}
.progress-topline {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    margin-bottom: 0.8rem;
}
.progress-title {
    color: #e8e8f0;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
    font-size: 0.95rem;
}
.progress-percent {
    color: #a78bfa;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 0.85rem;
}
.stage-list {
    display: grid;
    grid-template-columns: repeat(5, minmax(0, 1fr));
    gap: 0.6rem;
}
.stage-pill {
    border: 1px solid #1e1e2e;
    background: #0d0d14;
    border-radius: 10px;
    padding: 0.75rem;
    min-height: 76px;
}
.stage-pill.running {
    border-color: #7c3aed88;
    background: #171225;
}
.stage-pill.success {
    border-color: #10b98166;
    background: #0d1f17;
}
.stage-pill.error {
    border-color: #ef444466;
    background: #251112;
}
.stage-name {
    color: #d8d8e8;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.78rem;
    font-weight: 600;
    line-height: 1.25;
}
.stage-status {
    color: #6b7280;
    font-size: 0.72rem;
    margin-top: 0.45rem;
}
.stage-pill.running .stage-status { color: #a78bfa; }
.stage-pill.success .stage-status { color: #6ee7b7; }
.stage-pill.error .stage-status { color: #fca5a5; }
.error-box {
    background: #251112;
    border: 1px solid #ef444466;
    color: #fca5a5;
    border-radius: 10px;
    padding: 1rem 1.1rem;
    margin-top: 0.8rem;
    font-size: 0.9rem;
    line-height: 1.6;
}

@media (max-width: 900px) {
    .stage-list {
        grid-template-columns: 1fr;
    }
}

/* ── Success / Warning ── */
.stSuccess {
    background: #0f2e1a !important;
    border-color: #10b98144 !important;
    color: #6ee7b7 !important;
    border-radius: 10px !important;
}
.stWarning {
    background: #2e1a0f !important;
    border-color: #f59e0b44 !important;
    border-radius: 10px !important;
}

/* Content text */
.content-text {
    color: #c4c4d4;
    font-size: 0.93rem;
    line-height: 1.8;
    white-space: pre-wrap;
}
</style>
""", unsafe_allow_html=True)


# ── Hero ─────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">🧠 Multi-Agent AI System</div>
    <div class="hero-title">ResearchIQ</div>
    <div class="hero-sub">Enter any topic. Four specialized AI agents search, scrape, write, and critique a full research report — automatically.</div>
</div>
""", unsafe_allow_html=True)

# ── Pipeline Visual ───────────────────────────────────────────
st.markdown("""
<div class="pipeline">
    <div class="agent-node">
        <div class="agent-icon search">🔍</div>
        <div class="agent-label">Search</div>
    </div>
    <div class="pipeline-arrow">→</div>
    <div class="agent-node">
        <div class="agent-icon reader">📄</div>
        <div class="agent-label">Reader</div>
    </div>
    <div class="pipeline-arrow">→</div>
    <div class="agent-node">
        <div class="agent-icon writer">✍️</div>
        <div class="agent-label">Writer</div>
    </div>
    <div class="pipeline-arrow">→</div>
    <div class="agent-node">
        <div class="agent-icon critic">🧠</div>
        <div class="agent-label">Critic</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────
col1, col2 = st.columns([5, 1])
with col1:
    topic = st.text_input(
        label="topic",
        label_visibility="collapsed",
        placeholder="e.g. impact of AI on healthcare, quantum computing, PCOS treatment..."
    )
with col2:
    run = st.button("Research →", use_container_width=True)

st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

PROGRESS_STAGES = [
    ("searching", "Searching..."),
    ("reading", "Reading Sources..."),
    ("writing", "Writing Report..."),
    ("critiquing", "Critiquing Report..."),
    ("completed", "Completed"),
]


def render_progress_tracker(placeholder, progress_value, stage_statuses, current_message=""):
    stage_html = ""
    for stage_key, stage_name in PROGRESS_STAGES:
        status = stage_statuses.get(stage_key, "pending")
        if status == "success":
            indicator = "✓ Done"
        elif status == "running":
            indicator = "• Running"
        elif status == "error":
            indicator = "× Error"
        else:
            indicator = "Waiting"

        stage_html += f"""
        <div class="stage-pill {status}">
            <div class="stage-name">{html.escape(stage_name)}</div>
            <div class="stage-status">{indicator}</div>
        </div>
        """

    safe_message = html.escape(current_message or "Preparing the research agents...")
    with placeholder.container():
        st.markdown(f"""
        <div class="progress-card">
            <div class="progress-topline">
                <div>
                    <div class="progress-title">Research progress</div>
                    <div style="color:#6b7280;font-size:0.82rem;margin-top:0.25rem;">{safe_message}</div>
                </div>
                <div class="progress-percent">{progress_value}%</div>
            </div>
            <div class="stage-list">{stage_html}</div>
        </div>
        """, unsafe_allow_html=True)
        st.progress(progress_value)

if run:
    if not topic.strip():
        st.warning("Please enter a research topic to continue.")
    else:
        state = {}
        progress_placeholder = st.empty()
        stage_statuses = {stage_key: "pending" for stage_key, _ in PROGRESS_STAGES}

        render_progress_tracker(
            progress_placeholder,
            0,
            stage_statuses,
            "Preparing the research agents...",
        )

        def update_progress(stage, status, progress, message=None):
            if stage == "completed":
                for stage_key, _ in PROGRESS_STAGES:
                    stage_statuses[stage_key] = "success"
            else:
                stage_statuses[stage] = status

            render_progress_tracker(
                progress_placeholder,
                progress,
                stage_statuses,
                message or "Pipeline is running...",
            )

        try:
            state = run_research_pipeline(topic, progress_callback=update_progress)
        except Exception as exc:
            st.markdown(f"""
            <div class="error-box">
                <strong>Research stopped.</strong><br>
                {html.escape(str(exc))}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.success("✅ Research complete!")
            st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

            tab1, tab2, tab3, tab4 = st.tabs([
                "🔎 Search Results",
                "📄 Scraped Content",
                "📝 Final Report",
                "🧠 Critic Feedback"
            ])

            with tab1:
                st.markdown("#### What the Search Agent found")
                st.markdown(f"<div class='content-text'>{state.get('search_results', 'No results.')}</div>", unsafe_allow_html=True)

            with tab2:
                st.markdown("#### What the Reader Agent scraped")
                st.markdown(f"<div class='content-text'>{state.get('scraped_content', 'No content scraped.')}</div>", unsafe_allow_html=True)

            with tab3:
                st.markdown("#### Full Research Report")
                st.markdown(state.get("report", "No report generated."))
                st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
                st.download_button(
                    label="📥 Download Report as .txt",
                    data=state.get("report", ""),
                    file_name=f"{topic[:40].replace(' ', '_')}_report.txt",
                    mime="text/plain"
                )

            with tab4:
                feedback = state.get("feedback", "")
                score_line = ""
                for line in feedback.split("\n"):
                    if line.strip().startswith("Score:"):
                        score_line = line.strip().replace("Score:", "").strip()
                        break
                if score_line:
                    st.markdown(f"<div class='score-badge'>⭐ {score_line}</div>", unsafe_allow_html=True)
                st.markdown(feedback)
