import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from agent import run_cs_agent, SUBJECTS

st.set_page_config(
    page_title="CS Expert Agent",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize persistent session states safely
if "history" not in st.session_state:
    st.session_state["history"] = []
if "should_run" not in st.session_state:
    st.session_state["should_run"] = False
if "main_input" not in st.session_state:
    st.session_state["main_input"] = ""

# Callback function to route button clicks directly to the text input field
def set_active_query(query_text):
    st.session_state["main_input"] = query_text
    st.session_state["should_run"] = True

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] { 
        font-family: 'Inter', -apple-system, sans-serif; 
        -webkit-font-smoothing: antialiased;
    }
    .stApp { 
        background-color: #0d0e11; 
        color: #c9d1d9; 
    }

    .main-content-wrapper {
        padding: 0.5rem 2rem;
    }

    section[data-testid="stSidebar"] {
        background-color: #090a0d !important;
        border-right: 1px solid #1f242c !important;
    }
    section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    .sidebar-label {
        font-size: 0.72rem; 
        font-weight: 600; 
        color: #6e7681;
        text-transform: uppercase; 
        letter-spacing: 0.08em; 
        margin-top: 1.4rem;
        margin-bottom: 0.5rem;
    }
    .subject-chip {
        display: inline-flex; 
        align-items: center;
        background: #161b22; 
        border: 1px solid #21262d;
        border-radius: 4px; 
        padding: 4px 8px; 
        font-size: 0.75rem;
        color: #8b949e; 
        margin: 2px 2px;
    }

    div[data-testid="stHorizontalBlock"] {
        align-items: center !important;
        gap: 0.75rem !important;
    }

    div[data-testid="stTextInput"] {
        padding: 0 !important;
        margin: 0 !important;
    }
    div[data-testid="stTextInput"] input {
        background: #161b22 !important; 
        color: #f0f6fc !important;
        border: 1px solid #30363d !important; 
        border-radius: 6px !important;
        font-size: 0.95rem !important;
        padding: 0.55rem 0.75rem !important;
        height: 38px !important;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #2f81f7 !important; 
        box-shadow: 0 0 0 1px #2f81f7 !important;
    }

    .stButton {
        padding: 0 !important;
        margin: 0 !important;
    }
    .stButton > button {
        background: #161b22 !important;
        color: #c9d1d9 !important; 
        border: 1px solid #30363d !important; 
        border-radius: 6px !important;
        font-weight: 500 !important; 
        font-size: 0.88rem !important;
        transition: all 0.15s ease !important;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    section[data-testid="stSidebar"] .stButton > button {
        text-align: left;
        justify-content: flex-start;
        padding: 0.5rem 0.75rem !important;
        height: auto !important;
        line-height: 1.4 !important;
        white-space: normal !important;
    }
    .stButton > button:hover { 
        border-color: #8b949e !important;
        color: #f0f6fc !important;
        background: #21262d !important;
    }

    div.submit-container button {
        background: #238636 !important;
        color: #ffffff !important;
        border: 1px solid rgba(240,246,252,0.1) !important;
        height: 38px !important;
        width: 100%;
    }
    div.submit-container button:hover {
        background: #2ea043 !important;
    }

    div.subtopic-container button {
        padding: 1rem 1.25rem !important;
        height: auto !important;
        min-height: 72px !important;
        line-height: 1.5 !important;
        white-space: normal !important;
        text-align: left !important;
        justify-content: flex-start !important;
        font-size: 0.85rem !important;
        color: #8b949e !important;
        background: #161b22 !important;
        border: 1px solid #21262d !important;
    }
    div.subtopic-container button:hover {
        border-color: #30363d !important;
        color: #c9d1d9 !important;
        background: #1f242c !important;
    }

    .step-card {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem; 
        color: #8b949e;
        padding: 2px 0;
        border-left: 2px solid #21262d;
        padding-left: 12px;
        margin: 4px 0;
    }
    .architecture-step {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        color: #8b949e;
        line-height: 1.4;
    }

    .subject-badge {
        display: inline-block; 
        background: rgba(47, 129, 247, 0.1); 
        border: 1px solid rgba(47, 129, 247, 0.25);
        color: #58a6ff; 
        border-radius: 4px; 
        padding: 2px 8px;
        font-size: 0.75rem; 
        font-weight: 500; 
        margin-bottom: 1rem;
    }
    .answer-container {
        font-size: 0.98rem;
        line-height: 1.75; 
        color: #e6edf3;
        padding-top: 0.25rem;
    }

    .streamlit-expanderHeader {
        background-color: transparent !important;
        border-bottom: 1px solid #21262d !important;
        padding-left: 0 !important;
    }
    .streamlit-expanderContent {
        padding: 1rem 0.5rem !important;
    }

    hr { border-color: #21262d !important; margin: 1.5rem 0 !important; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### CS Expert Agent")
    
    st.markdown("<div class='sidebar-label'>Groq API Key</div>", unsafe_allow_html=True)
    groq_key = st.text_input(
        "Groq API Key", type="password", placeholder="gsk_...",
        label_visibility="collapsed",
    )
    st.caption("Provision a free token at console.groq.com")

    st.markdown("---")
    st.markdown("<div class='sidebar-label'>Subjects Covered</div>", unsafe_allow_html=True)
    for label in SUBJECTS.values():
        st.markdown(f"<span class='subject-chip'>{label}</span>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<div class='sidebar-label'>Agent Architecture</div>", unsafe_allow_html=True)
    st.markdown("""<div class='architecture-step'>
    Query -> [Classifier]
          -> [Retriever]
          -> [Reasoner Node]
          -> [FollowUp Gen]
          -> Output
    </div>""", unsafe_allow_html=True)
    st.caption("Engine: LangGraph + Llama 3.3 70B")

    st.markdown("---")
    st.markdown("<div class='sidebar-label'>Quick Seed Queries</div>", unsafe_allow_html=True)
    examples = [
        "Explain deadlock and its conditions",
        "What is BCNF normalization?",
        "How does pipelining work in CPU?",
        "Explain backpropagation in neural networks",
        "What is TCP 3-way handshake?",
        "Explain RSA encryption",
    ]
    for ex in examples:
        st.button(ex, key=f"ex_{ex}", on_click=set_active_query, args=(ex,))

st.markdown('<div class="main-content-wrapper">', unsafe_allow_html=True)

st.title("Computer Science Expert Agent")
st.markdown("<p style='color: #8b949e; margin-top: -1rem; margin-bottom: 2rem; font-size: 0.95rem;'>Deep reasoning engine tracking academic CS benchmarks across distributed curricula.</p>", unsafe_allow_html=True)

# Main query bar row
col1, col2 = st.columns([5, 1])

with col1:
    question = st.text_input(
        "Ask your CS question", 
        placeholder="e.g., Explain deadlock and Coffman's conditions...",
        label_visibility="collapsed",
        key="main_input"
    )

with col2:
    st.markdown('<div class="submit-container">', unsafe_allow_html=True)
    ask_clicked = st.button("Ask Agent")
    st.markdown('</div>', unsafe_allow_html=True)

if ask_clicked and question.strip():
    st.session_state["should_run"] = True

# --- Processing & Stream Evaluation ---
if st.session_state["should_run"] and st.session_state["main_input"].strip():
    st.session_state["should_run"] = False
    run_target = st.session_state["main_input"]
    
    if not groq_key:
        st.error("Configuration Error: Please enter your Groq API key in the left configuration sidebar.")
        st.stop()

    os.environ["GROQ_API_KEY"] = groq_key

    st.markdown("---")
    st.markdown("<h5 style='color: #8b949e; font-weight: 400 !important; margin-bottom: 0.5rem;'>Execution Trace</h5>", unsafe_allow_html=True)

    steps_placeholder = st.empty()
    steps_log_display = []

    final_answer = ""
    final_follow_ups = []
    final_subject = ""

    try:
        for update in run_cs_agent(run_target):
            for node_name, node_state in update.items():

                if "steps_log" in node_state:
                    steps_log_display.extend(node_state["steps_log"])
                    steps_html = "".join(
                        f"<div class='step-card'>  {s}</div>" for s in steps_log_display
                    )
                    steps_placeholder.markdown(steps_html, unsafe_allow_html=True)

                if node_state.get("subject_label"):
                    final_subject = node_state["subject_label"]
                if node_state.get("answer"):
                    final_answer = node_state["answer"]
                if node_state.get("follow_ups"):
                    final_follow_ups = node_state["follow_ups"]

        st.markdown("---")
        if final_subject:
            st.markdown(f"<div class='subject-badge'>{final_subject}</div>", unsafe_allow_html=True)

        st.markdown("<div class='answer-container'>", unsafe_allow_html=True)
        st.markdown(final_answer)
        st.markdown("</div>", unsafe_allow_html=True)

        if final_follow_ups:
            st.markdown("---")
            st.markdown("<h5 style='color: #8b949e; font-weight: 400 !important; margin-bottom: 0.75rem;'>Sub-topics to investigate</h5>", unsafe_allow_html=True)
            
            # Formatted multi-column grid with explicit component insulation wrapper
            f_cols = st.columns(len(final_follow_ups))
            for idx, fq in enumerate(final_follow_ups):
                with f_cols[idx]:
                    st.markdown('<div class="subtopic-container">', unsafe_allow_html=True)
                    st.button(f"-> {fq}", key=f"fq_{fq}", on_click=set_active_query, args=(fq,))
                    st.markdown('</div>', unsafe_allow_html=True)

        st.session_state["history"].insert(0, {
            "question": run_target,
            "subject": final_subject,
            "answer": final_answer,
        })

    except Exception as e:
        st.error(f"Agent Engine Error: {e}")
        st.info("Please verify network connectivity or validate API usage caps directly on your Groq console profile.")

if st.session_state["history"]:
    st.markdown("---")
    st.markdown("<h5 style='color: #8b949e; font-weight: 400 !important; margin-bottom: 0.75rem;'>Prior Computations</h5>", unsafe_allow_html=True)
    for h in st.session_state["history"][:3]:
        with st.expander(f"{h['subject'] if h['subject'] else 'General Processing'} - {h['question'][:75]}..."):
            st.markdown(h["answer"])

st.markdown('</div>', unsafe_allow_html=True)