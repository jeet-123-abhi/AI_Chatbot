import streamlit as st
import requests
from datetime import datetime
import html

# --- Page Config ---
st.set_page_config(page_title="✨ IntelliBot", layout="wide")

# --- Session State Initialization ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- CSS for background image and UI styling ---
st.markdown("""
<style>
/* Background Image */
.stApp::before {
    content: "";
    background-image: url('https://images.unsplash.com/photo-1601297183303-0c3fbc87f93d?auto=format&fit=crop&w=1350&q=80');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    opacity: 0.25;
    z-index: -1;
}

/* Content background container */
main > div:has(.element-container) {
    background-color: rgba(255, 255, 255, 0.9);
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 0 20px rgba(0,0,0,0.1);
}

/* Title animation */
h1 {
    animation: popIn 0.8s ease-in-out forwards;
}
@keyframes popIn {
    0% { transform: scale(0.9); opacity: 0; }
    100% { transform: scale(1); opacity: 1; }
}

/* Chat bubbles */
.chat-bubble {
    padding: 12px 18px;
    margin: 10px 0;
    border-radius: 12px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
    transition: all 0.3s ease;
    font-size: 16px;
}
.user {
    background-color: #fff8dc;
    text-align: right;
}
.ai {
    background-color: #e0f7fa;
    text-align: left;
}
.timestamp {
    font-size: 12px;
    color: gray;
    margin-top: 4px;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(to right, #6a11cb, #2575fc);
    color: white;
    font-weight: bold;
    border: none;
    border-radius: 10px;
    padding: 0.6rem 1.2rem;
    transition: all 0.3s ease;
}
.stButton > button:hover {
    transform: scale(1.05);
}
</style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown("<h1 style='text-align:center; color:#4B8BBE;'>🤖 IntelliBot: Your AI Knowledge Partner</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:18px;'>Chat with a helpful agent, optionally powered by real-time web search.</p>", unsafe_allow_html=True)

# --- Options ---
col1, col2 = st.columns([4, 1])
with col1:
    allow_web_search = st.checkbox("🌐 Enable Web Search", value=True)
with col2:
    if st.button("🧹 Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

# --- Agent Role (just for UI context) ---
agent_type = st.text_area(
    "🤖 Define your AI Agent (optional):",
    height=70,
    placeholder="E.g. Financial advisor, Python tutor, career coach..."
)
if agent_type.strip():
    st.markdown(f"#### 🧠 Active Agent: `{agent_type.strip()}`", unsafe_allow_html=True)

# --- Input Box ---
user_query = st.text_area("📝 Ask your question:", height=150, placeholder="E.g. How does LangChain work with Azure?")

# --- API Endpoint ---
API_URL = "http://127.0.0.1:8000/chat"

# --- Ask the Agent ---
if st.button("💬 Ask the Agent"):
    if user_query.strip():
        with st.spinner("Thinking..."):
            payload = {
                "messages": [user_query],
                "allow_search": allow_web_search
            }
            try:
                response = requests.post(API_URL, json=payload)
                if response.status_code == 200:
                    result = response.json()

                    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    st.session_state.chat_history.append(("user", user_query, now))
                    st.session_state.chat_history.append(("ai", result, now))

                    st.markdown("### ✅ Response from Intellibot")
                    st.markdown(f"<div class='chat-bubble ai'>{html.escape(result)}<div class='timestamp'>{now}</div></div>", unsafe_allow_html=True)
                else:
                    st.error(f"❌ Error: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"⚠️ Failed to connect to backend: {e}")
    else:
        st.warning("⚠️ Please enter a message before submitting.")

# --- Chat History ---
if st.session_state.chat_history:
    st.markdown("---")
    st.markdown("### 📜 Chat History")
    for role, message, ts in reversed(st.session_state.chat_history):
        bubble_class = "user" if role == "user" else "ai"
        st.markdown(f"""
            <div class='chat-bubble {bubble_class}'>{html.escape(message)}
                <div class='timestamp'>{ts}</div>
            </div>
        """, unsafe_allow_html=True)
