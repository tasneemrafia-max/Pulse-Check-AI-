import streamlit as st
import google.generativeai as genai

# --- PAGE SETUP ---
st.set_page_config(page_title="PulseCheck AI", page_icon="🚀", layout="centered")

# --- LOAD API KEY FROM STREAMLIT SECRETS ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing API Key. Please configure it in Streamlit Cloud Secrets.")
    st.stop()

model = genai.GenerativeModel('gemini-2.0-flash')

# --- SYSTEM PROMPT (The logic we built) ---
MASTER_PROMPT = """
[PASTE THE ENTIRE 'MASTER SYSTEM PROMPT' I GAVE YOU EARLIER HERE]
"""

# --- CHAT INTERFACE ---
st.title("🚀 PulseCheck AI")
st.markdown("### The Ultimate Career Diagnostic Engine")

if "messages" not in st.session_state:
    st.session_state.messages = []
    # Initialize with a welcome message logic
    with st.chat_message("assistant"):
        st.markdown("🚀 **Welcome to PulseCheck AI.** I'm ready to begin. What is the **Target Role and Company** you are aiming for?")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Type your response..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    context = MASTER_PROMPT + "\n" + "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
    response = model.generate_content(context)
    
    with st.chat_message("assistant"):
        st.markdown(response.text)
    st.session_state.messages.append({"role": "assistant", "content": response.text})
