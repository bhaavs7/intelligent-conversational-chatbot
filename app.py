import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI


# =========================================================
# 1. LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Streamlit Cloud support
if not GROQ_API_KEY:
    try:
        GROQ_API_KEY = st.secrets.get("GROQ_API_KEY")
    except Exception:
        GROQ_API_KEY = None


# =========================================================
# 2. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AIva - Intelligent Chatbot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)


# =========================================================
# 3. CUSTOM CSS
# =========================================================

st.markdown(
    """
<style>
.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(155, 190, 255, 0.25), transparent 25%),
        radial-gradient(circle at 90% 90%, rgba(190, 160, 255, 0.20), transparent 25%),
        linear-gradient(135deg, #f7f9ff 0%, #eef3ff 50%, #f9f5ff 100%);
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 7rem;
    max-width: 900px;
}


/* ================= SIDEBAR ================= */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(180deg, #f4f7ff 0%, #eef3ff 55%, #f7f2ff 100%);
    border-right: 1px solid #e0e5f3;
}

.sidebar-title {
    font-size: 24px;
    font-weight: 800;
    color: #30395c;
    margin-bottom: 5px;
}

.sidebar-subtitle {
    color: #7b849f;
    font-size: 13px;
    line-height: 1.5;
    margin-bottom: 20px;
}

.feature-card {
    background: rgba(255, 255, 255, 0.78);
    border-radius: 18px;
    padding: 14px;
    margin: 10px 0;
    border: 1px solid rgba(130, 150, 220, 0.15);
}

.feature-title {
    font-weight: 700;
    color: #394362;
    font-size: 14px;
}

.feature-text {
    color: #7c849d;
    font-size: 12px;
    margin-top: 3px;
    line-height: 1.5;
}


/* ================= AI HEADER ================= */

.hero {
    background: rgba(255, 255, 255, 0.82);
    border: 1px solid rgba(255, 255, 255, 0.9);
    border-radius: 28px;
    padding: 25px 28px;
    margin-bottom: 22px;
    box-shadow: 0 12px 40px rgba(70, 90, 150, 0.12);
    backdrop-filter: blur(15px);
}

.hero-content {
    display: flex;
    align-items: center;
    gap: 18px;
}

.robot-icon {
    width: 65px;
    height: 65px;
    border-radius: 20px;
    background: linear-gradient(135deg, #6c8cff, #9b7cff);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 34px;
    box-shadow: 0 8px 20px rgba(108, 140, 255, 0.30);
}

.hero-title {
    font-size: 30px;
    font-weight: 800;
    color: #202846;
    margin: 0;
}

.hero-subtitle {
    font-size: 14px;
    color: #707995;
    margin-top: 5px;
}

.status {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background: #edfdf4;
    color: #258653;
    border-radius: 50px;
    padding: 7px 13px;
    font-size: 12px;
    font-weight: 600;
    margin-top: 12px;
}

.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #36c77b;
}


/* ================= WELCOME CARD ================= */

.welcome-card {
    background:
        linear-gradient(
            135deg,
            rgba(255,255,255,0.96),
            rgba(246,248,255,0.94)
        );
    border-radius: 24px;
    padding: 22px;
    margin: 15px 0 20px 0;
    border: 1px solid rgba(130, 150, 220, 0.15);
    box-shadow: 0 10px 30px rgba(70, 90, 150, 0.08);
}

.welcome-card h3 {
    color: #30395c;
    font-size: 18px;
    margin: 0 0 8px 0;
}

.welcome-card p {
    color: #737c96;
    font-size: 14px;
    line-height: 1.6;
    margin: 0;
}


/* ================= CHAT ================= */

[data-testid="stChatMessage"] {
    border-radius: 20px;
    padding: 10px 14px;
    margin-bottom: 10px;
}

[data-testid="stChatInput"] {
    border-radius: 20px;
}

[data-testid="stChatInput"] textarea {
    border-radius: 18px !important;
    border: 1px solid #dce2f2 !important;
    background: rgba(255, 255, 255, 0.92) !important;
    padding: 15px !important;
}


/* ================= BUTTON ================= */

.stButton > button {
    width: 100%;
    border-radius: 14px;
    border: none;
    background: linear-gradient(135deg, #718cff, #967cff);
    color: white;
    font-weight: 700;
    padding: 10px;
    box-shadow: 0 7px 18px rgba(112, 132, 240, 0.25);
    transition: 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 22px rgba(112, 132, 240, 0.35);
}


/* ================= FOOTER ================= */

.footer {
    text-align: center;
    color: #9aa2b8;
    font-size: 11px;
    margin-top: 30px;
    padding: 15px;
}
</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# 4. CHECK API KEY
# =========================================================

if not GROQ_API_KEY:
    st.error("⚠️ Groq API key was not found.")
    st.info(
        "Please make sure your .env file contains "
        "GROQ_API_KEY=YOUR_KEY"
    )
    st.stop()


# =========================================================
# 5. CREATE GROQ CLIENT
# =========================================================

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_API_KEY
)


# =========================================================
# 6. SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
<div class="sidebar-title">🤖 AIva</div>
<div class="sidebar-subtitle">Your intelligent conversational AI assistant.</div>
""",
        unsafe_allow_html=True
    )

    st.markdown(
        """
<div class="feature-card">
<div class="feature-title">🧠 Natural Language Processing</div>
<div class="feature-text">Understands and responds to natural language.</div>
</div>

<div class="feature-card">
<div class="feature-title">⚡ Generative AI</div>
<div class="feature-text">Powered by Groq and modern language models.</div>
</div>

<div class="feature-card">
<div class="feature-title">💬 Conversation Memory</div>
<div class="feature-text">Keeps track of the current conversation.</div>
</div>
""",
        unsafe_allow_html=True
    )

    st.markdown("---")

    if st.button("🗑️ Clear Conversation"):

        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Hello! 👋 I am AIva, your intelligent "
                    "AI assistant. How can I help you today?"
                )
            }
        ]

        st.rerun()

    st.markdown("---")

    st.caption("Technology")
    st.caption("Python • Streamlit • Groq • NLP")


# =========================================================
# 7. MAIN AI HEADER
# =========================================================

st.markdown(
    """
<div class="hero">
<div class="hero-content">

<div class="robot-icon">🤖</div>

<div>
<div class="hero-title">AIva</div>
<div class="hero-subtitle">Intelligent Conversational Chatbot</div>

<div class="status">
<span class="status-dot"></span>
AI Assistant Online
</div>

</div>

</div>
</div>
""",
    unsafe_allow_html=True
)


# =========================================================
# 8. WELCOME CARD
# =========================================================

st.markdown(
    """
<div class="welcome-card">
<h3>✨ Welcome! How can I help you?</h3>
<p>Ask questions, explore ideas, get explanations, or simply start a conversation with your AI assistant.</p>
</div>
""",
    unsafe_allow_html=True
)


# =========================================================
# 9. INITIALIZE CHAT HISTORY
# =========================================================

if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello! 👋 I am AIva, your intelligent "
                "AI assistant. How can I help you today?"
            )
        }
    ]


# =========================================================
# 10. DISPLAY PREVIOUS MESSAGES
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# =========================================================
# 11. CHAT INPUT
# =========================================================

user_query = st.chat_input(
    "💬 Type your message here..."
)


# =========================================================
# 12. PROCESS USER MESSAGE
# =========================================================

if user_query:

    with st.chat_message("user"):
        st.markdown(user_query)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_query
        }
    )

    with st.chat_message("assistant"):

        with st.spinner("🤔 AIva is thinking..."):

            try:

                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {
                            "role": message["role"],
                            "content": message["content"]
                        }
                        for message in st.session_state.messages
                    ],
                    temperature=0.7,
                    max_tokens=1024
                )

                bot_reply = response.choices[0].message.content

            except Exception as e:

                bot_reply = (
                    "Sorry, I couldn't connect to the AI service. "
                    "Please check your API key and try again."
                )

                st.error(f"Error: {e}")

        st.markdown(bot_reply)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": bot_reply
        }
    )


# =========================================================
# 13. FOOTER
# =========================================================

st.markdown(
    """
<div class="footer">
🤖 AIva • Intelligent Conversational Chatbot
<br>
Built with Python, Streamlit & Generative AI
</div>
""",
    unsafe_allow_html=True
)