import streamlit as st
from openai import OpenAI

# -------------------- Styling --------------------
st.markdown("""
<style>
body { font-family: 'Segoe UI', sans-serif; background-color: #eef2f7; }
.stChatMessage.user { background-color: #d1e7dd; text-align: right; border-radius: 8px; }
.stChatMessage.assistant { background-color: #f8d7da; text-align: left; border-radius: 8px; }
.stButton > button { width: 100%; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

# -------------------- Title & Language Toggle --------------------
st.title("💼⚖️ HakiBot – Kenyan Legal Assistant")
st.write("""
st.title("🤝 HakiBot: Your Kenyan Legal Companion")
language = st.radio("🌐 Choose Language", ["English", "Swahili"])
sw = language == "Swahili"
Welcome to **HakiBot**, your friendly legal chatbot focused on:
- 🧑‍🏭 **Employment Law** (contracts, rights, workplace disputes)
- 🚓 **Arrest and Court Process** (your rights when arrested, bail, trial procedure)

👋 Type your question below to get started.
""")
# -------------------- API Key Input --------------------
openai_api_key = st.text_input("🔑 OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please enter your API key to start chatting with HakiBot.", icon="🗝️")
    st.stop()

client = OpenAI(api_key=openai_api_key)

# -------------------- Topics --------------------
st.subheader("📌 Legal Topics")
topic = st.selectbox("Pick a topic you need help with:", [
    "Employment Law",
    "Arrest & Court Process"
])

examples = {
    "Employment Law": [
        "What are my rights as a casual worker?",
        "Can my employer fire me without notice?",
        "How do I file a complaint about unfair dismissal?"
    ],
    "Arrest & Court Process": [
        "What should I do when arrested?",
        "How does bail work in Kenya?",
        "What happens after being taken to court?"
    ]
}

st.markdown("💡 Try asking:")
for ex in examples.get(topic, []):
    st.markdown(f"- _{ex}_")

# -------------------- Session State --------------------
if "messages" not in st.session_state:
    welcome = "Karibu! Uliza swali lolote kuhusu sheria za kazi au kukamatwa na kufikishwa mahakamani." if sw else "Welcome! Ask anything about employment law or being arrested and taken to court."
    st.session_state.messages = [{"role": "assistant", "content": welcome}]

# -------------------- Chat Display --------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------- Input --------------------
user_input = st.chat_input("Type your question here..." if not sw else "Andika swali lako hapa...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
        stream=True,
    )

    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

    # -------------------- Feedback Prompt --------------------
    st.success("✅ Was this helpful?")
    col1, col2 = st.columns(2)
    with col1: st.button("👍 Yes")
    with col2: st.button("👎 No")

# -------------------- Legal Disclaimers --------------------
st.divider()
st.caption("⚠️ **Disclaimer:** HakiBot provides general information related to Kenyan employment law and legal procedures after arrest. It does not offer legal advice.")
st.caption("📚 **For Educational Purposes Only:** Always consult a licensed Kenyan advocate for individual legal matters.")
