import streamlit as st
from openai import OpenAI

# -------------------- Styling --------------------
st.markdown("""
    <style>
    body { font-family: 'Segoe UI', sans-serif; background-color: #f5f9ff; }
    .main { background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0px 0px 10px rgba(0,0,0,0.05); }
    .stChatMessage { padding: 10px; margin-bottom: 10px; border-radius: 8px; }
    .stChatMessage.user { background-color: #d1e7dd; text-align: right; }
    .stChatMessage.assistant { background-color: #f8d7da; text-align: left; }
    </style>
""", unsafe_allow_html=True)

# -------------------- Title & Description --------------------
st.title("💬 HakiBot – Your Legal Companion")
st.write("Welcome to **HakiBot**, a free chatbot helping Kenyans learn about their legal rights 🇰🇪.\n\n📘 _Ask questions like 'What are land rights for women?' or 'How does divorce work in Kenya?'_")

# -------------------- API Key Input --------------------
openai_api_key = st.text_input("🔑 Enter your OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please enter your OpenAI key to begin the conversation.", icon="🗝️")
    st.stop()

# -------------------- OpenAI Client --------------------
client = OpenAI(api_key=openai_api_key)

# -------------------- Session State --------------------
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "👋 Hi, I'm HakiBot! Ask me any question about Kenyan law."}]

# -------------------- Display Messages --------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------- Chat Input --------------------
user_input = st.chat_input("Type your legal question here...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get response from GPT
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
        stream=True,
    )

    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

# -------------------- Legal Disclaimer --------------------
st.divider()
st.caption("⚠️ **Disclaimer:** HakiBot provides general legal information, not legal advice. For personal matters, please consult a licensed Kenyan advocate or legal professional.")
