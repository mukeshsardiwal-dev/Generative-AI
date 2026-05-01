import streamlit as st
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Funny AI Agent",
    page_icon="🎭",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bangers&family=Nunito:wght@400;600;700&display=swap');

/* ── Root variables ── */
:root {
    --bg:        #0d0d0d;
    --surface:   #1a1a1a;
    --border:    #2e2e2e;
    --accent:    #ff4d4d;
    --accent2:   #ffd93d;
    --user-bg:   #ff4d4d;
    --bot-bg:    #1f1f1f;
    --text:      #f0f0f0;
    --muted:     #888;
    --radius:    16px;
}

/* ── Global ── */
html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    font-family: 'Nunito', sans-serif;
    color: var(--text);
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }

[data-testid="stAppViewContainer"] > .main {
    padding: 0 !important;
}

/* ── Header ── */
.chat-header {
    text-align: center;
    padding: 28px 20px 12px;
    border-bottom: 1px solid var(--border);
    background: var(--surface);
    position: sticky;
    top: 0;
    z-index: 10;
}
.chat-header h1 {
    font-family: 'Bangers', cursive;
    font-size: 2.6rem;
    letter-spacing: 3px;
    color: var(--accent);
    margin: 0;
    text-shadow: 3px 3px 0 var(--accent2);
}
.chat-header p {
    color: var(--muted);
    font-size: 0.85rem;
    margin: 4px 0 0;
}

/* ── Chat window ── */
.chat-window {
    max-width: 720px;
    margin: 0 auto;
    padding: 20px 16px 140px;
    display: flex;
    flex-direction: column;
    gap: 14px;
}

/* ── Message bubbles ── */
.msg-row {
    display: flex;
    align-items: flex-end;
    gap: 10px;
}
.msg-row.user  { flex-direction: row-reverse; }
.msg-row.bot   { flex-direction: row; }

.avatar {
    width: 38px;
    height: 38px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
    flex-shrink: 0;
}
.avatar.user { background: var(--accent); }
.avatar.bot  { background: var(--accent2); }

.bubble {
    max-width: 75%;
    padding: 12px 16px;
    border-radius: var(--radius);
    font-size: 0.95rem;
    line-height: 1.55;
    word-break: break-word;
}
.bubble.user {
    background: var(--user-bg);
    color: #fff;
    border-bottom-right-radius: 4px;
}
.bubble.bot {
    background: var(--bot-bg);
    color: var(--text);
    border: 1px solid var(--border);
    border-bottom-left-radius: 4px;
}

/* ── Typing indicator ── */
.typing {
    display: flex;
    align-items: center;
    gap: 5px;
    padding: 12px 16px;
}
.typing span {
    width: 8px; height: 8px;
    background: var(--accent2);
    border-radius: 50%;
    animation: bounce 1.1s infinite;
}
.typing span:nth-child(2) { animation-delay: 0.2s; }
.typing span:nth-child(3) { animation-delay: 0.4s; }
@keyframes bounce {
    0%, 80%, 100% { transform: translateY(0); }
    40%            { transform: translateY(-8px); }
}

/* ── Input bar ── */
.stChatInputContainer, [data-testid="stChatInput"] {
    background: var(--surface) !important;
    border-top: 1px solid var(--border) !important;
}
[data-testid="stChatInput"] textarea {
    background: var(--bg) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    font-family: 'Nunito', sans-serif !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(255,77,77,0.25) !important;
}

/* ── Sidebar / clear button ── */
.stButton > button {
    background: var(--accent) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px;
    transition: opacity 0.2s;
}
.stButton > button:hover { opacity: 0.85 !important; }

[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="chat-header">
    <h1>🎭 Funny AI Agent</h1>
    <p>Your personal comedian — created by <strong>Mukesh Sardiwal</strong></p>
</div>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content="You are a Funny AI Agent and a Comedian who can crack jokes.")
    ]

if "model" not in st.session_state:
    st.session_state.model = ChatOpenAI(model="gpt-4o-mini", temperature=0.9)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🎪 Chat Controls")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = [
            SystemMessage(content="You are a Funny AI Agent and a Comedian who can crack jokes.")
        ]
        st.rerun()
    st.markdown("---")
    msg_count = len([m for m in st.session_state.messages if not isinstance(m, SystemMessage)])
    st.markdown(f"**Messages exchanged:** {msg_count}")
    st.markdown("---")
    st.markdown("**Tips:**")
    st.markdown("- Ask for a joke on any topic")
    st.markdown("- Request a pun or one-liner")
    st.markdown("- Just chat and laugh!")

# ── Render existing conversation ──────────────────────────────────────────────
chat_html = '<div class="chat-window">'

for msg in st.session_state.messages:
    if isinstance(msg, SystemMessage):
        continue
    if isinstance(msg, HumanMessage):
        chat_html += f"""
        <div class="msg-row user">
            <div class="avatar user">🧑</div>
            <div class="bubble user">{msg.content}</div>
        </div>"""
    elif isinstance(msg, AIMessage):
        chat_html += f"""
        <div class="msg-row bot">
            <div class="avatar bot">🤖</div>
            <div class="bubble bot">{msg.content}</div>
        </div>"""

chat_html += '</div>'
st.markdown(chat_html, unsafe_allow_html=True)

# ── Chat input ────────────────────────────────────────────────────────────────
if prompt := st.chat_input("Say something... or ask for a joke! 😄"):
    st.session_state.messages.append(HumanMessage(content=prompt))

    # Show typing indicator while waiting
    with st.spinner(""):
        response = st.session_state.model.invoke(st.session_state.messages)

    st.session_state.messages.append(AIMessage(content=response.content))
    st.rerun()