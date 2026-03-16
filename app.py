import streamlit as st
import json
from model import generate_response

st.title("Student Research Chatbot")

MEMORY_FILE = "memory.json"

# Load memory
def load_memory():
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except:
        return []

# Save memory
def save_memory(messages):
    with open(MEMORY_FILE, "w") as f:
        json.dump(messages, f, indent=2)

# Initialize session memory
if "messages" not in st.session_state:
    st.session_state.messages = load_memory()

messages = st.session_state.messages


# Sidebar controls
if st.sidebar.button("Clear Chat Memory"):
    st.session_state.messages = []
    save_memory([])
    st.rerun()


# Display chat history
for msg in messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


# Chat input
prompt = st.chat_input("Ask your research question")


if prompt:

    # Add user message
    user_message = {"role": "user", "content": prompt}
    messages.append(user_message)

    with st.chat_message("user"):
        st.write(prompt)

    # System prompt
    system_prompt = {
        "role": "system",
        "content": "You are a helpful research assistant chatbot for students. Provide clear and accurate explanations."
    }

    # Send last messages to model
    context = [system_prompt] + messages[-12:]

    try:
        response = generate_response(context)

    except Exception as e:
        response = f"⚠️ Error: {e}"

    # Show assistant message
    with st.chat_message("assistant"):
        st.write(response)

    messages.append({
        "role": "assistant",
        "content": response
    })

    # Save memory
    save_memory(messages)