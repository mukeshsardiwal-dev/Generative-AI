from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Mood Bot", page_icon="🤖", layout="centered")

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
}

/* Dark background */
.stApp {
    background-color: #0d0d0f;
    color: #e8e8e8;
}

/* Hide Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }

/* Title */
.title-block {
    text-align: center;
    padding: 2rem 0 1rem;
}
.title-block h1 {
    font-size: 3rem;
    font-weight: 800;
    letter-spacing: -2px;
    margin: 0;
    line-height: 1;
}
.title-block p {
    font-family: 'DM Mono', monospace;
    font-size: 0.78rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #666;
    margin-top: 0.4rem;
}

/* Mode cards */
.mode-grid {
    display: flex;
    gap: 1rem;
    justify-content: center;
    margin: 1.5rem 0;
}
.mode-card {
    flex: 1;
    padding: 1.2rem 1rem;
    border-radius: 12px;
    text-align: center;
    cursor: pointer;
    border: 2px solid transparent;
    transition: all 0.2s;
    font-weight: 700;
    font-size: 1rem;
}

/* Angry */
.angry-card  { background: #1a0a0a; border-color: #ff2d2d; color: #ff2d2d; }
/* Funny */
.funny-card  { background: #0d1a08; border-color: #7fff2d; color: #7fff2d; }
/* Sad */
.sad-card    { background: #08101a; border-color: #2d8fff; color: #2d8fff; }

/* Active state via selected class */
.angry-card.selected  { background: #ff2d2d; color: #fff; }
.funny-card.selected  { background: #7fff2d; color: #111; }
.sad-card.selected    { background: #2d8fff; color: #fff; }

/* Streamlit buttons – override */
div[data-testid="column"] button {
    width: 100% !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    padding: 0.9rem !important;
    border: 2px solid !important;
    transition: all 0.2s !important;
}

/* Chat bubbles */
.bubble-wrap { display: flex; margin: 0.6rem 0; }
.bubble-wrap.user  { justify-content: flex-end; }
.bubble-wrap.bot   { justify-content: flex-start; }

.bubble {
    max-width: 72%;
    padding: 0.85rem 1.1rem;
    border-radius: 18px;
    font-size: 0.95rem;
    line-height: 1.5;
    font-family: 'DM Mono', monospace;
    font-weight: 400;
}
.bubble.user { background: #1e1e22; color: #ddd; border-bottom-right-radius: 4px; }
.bubble.bot-angry  { background: #ff2d2d22; border: 1px solid #ff2d2d55; color: #ffaaaa; border-bottom-left-radius: 4px; }
.bubble.bot-funny  { background: #7fff2d22; border: 1px solid #7fff2d55; color: #ccff88; border-bottom-left-radius: 4px; }
.bubble.bot-sad    { background: #2d8fff22; border: 1px solid #2d8fff55; color: #aaccff; border-bottom-left-radius: 4px; }

.mode-badge {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    display: inline-block;
    margin-bottom: 1rem;
}
.badge-angry { background:#ff2d2d22; color:#ff2d2d; border:1px solid #ff2d2d44; }
.badge-funny { background:#7fff2d22; color:#7fff2d; border:1px solid #7fff2d44; }
.badge-sad   { background:#2d8fff22; color:#2d8fff; border:1px solid #2d8fff44; }

/* Input box */
.stTextInput input {
    background: #1a1a1f !important;
    border: 1.5px solid #2a2a35 !important;
    border-radius: 10px !important;
    color: #e8e8e8 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.9rem !important;
    padding: 0.75rem 1rem !important;
}
.stTextInput input:focus {
    border-color: #555 !important;
    box-shadow: none !important;
}

/* Send button */
div[data-testid="stButton"] > button {
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
}

/* Divider */
hr { border-color: #1e1e25; margin: 1rem 0; }
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "mode" not in st.session_state:
    st.session_state.mode = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "lc_messages" not in st.session_state:
    st.session_state.lc_messages = []

# ── Mode config ───────────────────────────────────────────────────────────────
MODE_CONFIG = {
    "angry": {
        "label": "😤 Angry",
        "system": "You are an angry AI Agent. You respond aggressively and impatiently.",
        "bubble_class": "bot-angry",
        "badge_class": "badge-angry",
        "badge_text": "😤 ANGRY MODE",
    },
    "funny": {
        "label": "😂 Funny",
        "system": "You are a funny AI Agent. You respond very funny and crazy and humorous.",
        "bubble_class": "bot-funny",
        "badge_class": "badge-funny",
        "badge_text": "😂 FUNNY MODE",
    },
    "sad": {
        "label": "😢 Sad",
        "system": "You are a sad AI Agent. You respond depressed and sadly with anxiety.",
        "bubble_class": "bot-sad",
        "badge_class": "badge-sad",
        "badge_text": "😢 SAD MODE",
    },
}

# ── Title ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="title-block">
    <h1>MOOD BOT</h1>
    <p>pick a personality · start chatting</p>
</div>
""", unsafe_allow_html=True)

# ── Mode selection ────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)

btn_styles = {
    "angry": "background-color:#1a0a0a; color:#ff2d2d; border-color:#ff2d2d;",
    "funny": "background-color:#0d1a08; color:#7fff2d; border-color:#7fff2d;",
    "sad":   "background-color:#08101a; color:#2d8fff; border-color:#2d8fff;",
}

with col1:
    if st.button("😤  Angry", use_container_width=True):
        st.session_state.mode = "angry"
        st.session_state.messages = []
        st.session_state.lc_messages = [SystemMessage(content=MODE_CONFIG["angry"]["system"])]

with col2:
    if st.button("😂  Funny", use_container_width=True):
        st.session_state.mode = "funny"
        st.session_state.messages = []
        st.session_state.lc_messages = [SystemMessage(content=MODE_CONFIG["funny"]["system"])]

with col3:
    if st.button("😢  Sad", use_container_width=True):
        st.session_state.mode = "sad"
        st.session_state.messages = []
        st.session_state.lc_messages = [SystemMessage(content=MODE_CONFIG["sad"]["system"])]

st.markdown("<hr>", unsafe_allow_html=True)

# ── Chat area ─────────────────────────────────────────────────────────────────
if st.session_state.mode is None:
    st.markdown("""
    <div style="text-align:center; color:#333; padding: 3rem 0; font-family:'DM Mono',monospace; font-size:0.85rem; letter-spacing:2px;">
        SELECT A MODE ABOVE TO BEGIN
    </div>
    """, unsafe_allow_html=True)
else:
    cfg = MODE_CONFIG[st.session_state.mode]

    # Badge
    st.markdown(f'<div class="mode-badge {cfg["badge_class"]}">{cfg["badge_text"]}</div>', unsafe_allow_html=True)

    # Render chat history
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="bubble-wrap user"><div class="bubble user">{msg["content"]}</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bubble-wrap bot"><div class="bubble {cfg["bubble_class"]}">{msg["content"]}</div></div>', unsafe_allow_html=True)

    # Input row
    input_col, btn_col = st.columns([5, 1])
    with input_col:
        user_input = st.text_input("message", placeholder="Type your message…", label_visibility="collapsed", key="chat_input")
    with btn_col:
        send = st.button("Send", use_container_width=True)

    if send and user_input.strip():
        # Append user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.lc_messages.append(HumanMessage(content=user_input))

        # Call model
        model = ChatOpenAI(model="gpt-4o-mini", temperature=0.9)
        response = model.invoke(st.session_state.lc_messages)

        # Append bot message
        st.session_state.lc_messages.append(AIMessage(content=response.content))
        st.session_state.messages.append({"role": "bot", "content": response.content})

        st.rerun()

    # Reset button
    if st.session_state.messages:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Reset Chat", use_container_width=False):
            st.session_state.messages = []
            st.session_state.lc_messages = [SystemMessage(content=cfg["system"])]
            st.rerun()