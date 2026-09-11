import os
import streamlit as st
from google import genai
from google.genai import types

# Page setup
st.set_page_config(
    page_title="EcoBot - Sustainable Living & Climate Action",
    page_icon="🌱",
    layout="centered"
)

# Custom Styling
st.markdown("""
    <style>
    .main-title {
        color: #2E7D32;
        text-align: center;
        font-size: 2.2rem;
        font-weight: bold;
    }
    .sub-title {
        text-align: center;
        color: #555555;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🌱 EcoBot AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Your AI Assistant for Responsible Consumption (SDG 12) & Climate Action (SDG 13)</p>", unsafe_allow_html=True)

# Fetch API key (Supports Streamlit Secrets and Environment Variables)
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key and "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]

if not api_key:
    st.warning("⚠️ GEMINI_API_KEY config nahi mili. Kripya environment variable set karein ya Streamlit Secrets me add karein.")
    st.stop()

# Initialize Client
client = genai.Client(api_key=api_key)

SYSTEM_INSTRUCTION = """
You are EcoBot, an AI specialized in Sustainable Living, Responsible Consumption (UN SDG 12), and Climate Action (UN SDG 13).
Your objectives:
1. Educate users on reducing food waste, single-use plastics, energy consumption, and carbon footprint.
2. Provide actionable, realistic daily tips for sustainable lifestyle choices.
3. Answer climate change queries with facts and encouragement.
4. Maintain a polite, concise, and engaging tone with bullet points when appropriate.
If asked about non-sustainability topics, politely guide the user back to environmental issues.
"""

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "model",
            "content": "Hello! I am EcoBot 🌿. Ask me anything about sustainable living, eco-friendly habits, or how to reduce your carbon footprint!"
        }
    ]

# Render Messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Chat Input
if prompt := st.chat_input("Ask about eco-friendly habits, recycling, climate action..."):
    # Render User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # API Request & Bot Response
    with st.chat_message("model"):
        with st.spinner("Thinking green..."):
            try:
                contents = []
                for msg in st.session_state.messages:
                    role = "user" if msg["role"] == "user" else "model"
                    contents.append(
                        types.Content(
                            role=role,
                            parts=[types.Part.from_text(text=msg["content"])]
                        )
                    )

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        temperature=0.7,
                    )
                )

                response_text = response.text
                st.markdown(response_text)
                st.session_state.messages.append({"role": "model", "content": response_text})

            except Exception as e:
                st.error(f"Error generating response: {str(e)}")
