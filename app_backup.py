import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI


# ---------------------------------------------------------
# 1. Load environment variables
# ---------------------------------------------------------

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ---------------------------------------------------------
# 2. Page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="Intelligent Conversational Chatbot",
    page_icon="🤖",
    layout="centered"
)


# ---------------------------------------------------------
# 3. Check API key
# ---------------------------------------------------------

if not GROQ_API_KEY:
    st.error("Groq API key was not found.")
    st.info("Please make sure your .env file contains GROQ_API_KEY.")
    st.stop()


# ---------------------------------------------------------
# 4. Create Groq client
# ---------------------------------------------------------

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_API_KEY
)


# ---------------------------------------------------------
# 5. Sidebar
# ---------------------------------------------------------

with st.sidebar:

    st.header("🛠️ Project Controls")

    st.info(
        "Domain: Conversational AI & Support\n\n"
        "Technology: Python, NLP, Streamlit, Groq"
    )

    if st.button("🗑️ Clear Chat History"):

        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Hello! I am your AI assistant. "
                    "How can I help you today?"
                )
            }
        ]

        st.rerun()


# ---------------------------------------------------------
# 6. Application title
# ---------------------------------------------------------

st.title("🤖 Intelligent Conversational Chatbot")

st.markdown(
    "Ask me anything and I will try to help you using "
    "Natural Language Processing and Generative AI."
)


# ---------------------------------------------------------
# 7. Initialize conversation history
# ---------------------------------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello! 👋 I am your AI assistant. "
                "How can I help you today?"
            )
        }
    ]


# ---------------------------------------------------------
# 8. Display previous messages
# ---------------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ---------------------------------------------------------
# 9. Get new user message
# ---------------------------------------------------------

user_query = st.chat_input(
    "Type your message here..."
)


# ---------------------------------------------------------
# 10. Process user message
# ---------------------------------------------------------

if user_query:

    # Display user's message
    with st.chat_message("user"):

        st.markdown(user_query)

    # Save user's message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_query
        }
    )

    # Generate AI response
    with st.chat_message("assistant"):

        with st.spinner("🤔 Thinking..."):

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

    # Save AI response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": bot_reply
        }
    )
