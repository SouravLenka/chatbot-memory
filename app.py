import streamlit as st
import json
import os
import time
from model import generate_response
from retriever import get_context

# --- STUDY FILTER (Improved) ---
def is_study_related(prompt):
    non_study = ["game", "movie", "song", "actor", "valorant", "netflix", "youtube"]
    if any(word in prompt.lower() for word in non_study):
        return False
    return True

# --- FOLLOW-UP DETECTION ---
def is_followup(prompt):
    follow_words = ["explain", "elaborate", "detail", "continue", "more", "expand", "why", "how"]
    return any(word in prompt.lower() for word in follow_words)

# Branding
st.set_page_config(page_title="BodhAI")
st.title("BodhAI")
st.caption("Study Mode Enabled: Only academic queries allowed")

SESSIONS_DIR = "sessions"
if not os.path.exists(SESSIONS_DIR):
    os.makedirs(SESSIONS_DIR)

# Session Management Functions
def get_session_files():
    files = [f for f in os.listdir(SESSIONS_DIR) if f.endswith(".json")]
    # Sort by modification time (newest first)
    files.sort(key=lambda x: os.path.getmtime(os.path.join(SESSIONS_DIR, x)), reverse=True)
    return files

def load_session(session_id):
    try:
        with open(os.path.join(SESSIONS_DIR, session_id), "r") as f:
            return json.load(f)
    except:
        return {"title": "New Chat", "messages": []}

def save_session(session_id, title, messages):
    data = {"title": title, "messages": messages}
    with open(os.path.join(SESSIONS_DIR, session_id), "w") as f:
        json.dump(data, f, indent=2)

def create_new_session():
    session_id = f"chat_{int(time.time())}.json"
    save_session(session_id, "New Chat", [])
    return session_id

def delete_session(session_id):
    path = os.path.join(SESSIONS_DIR, session_id)
    if os.path.exists(path):
        os.remove(path)

# Initialize Session State
if "current_session_id" not in st.session_state:
    sessions = get_session_files()
    if sessions:
        st.session_state.current_session_id = sessions[0]
    else:
        st.session_state.current_session_id = create_new_session()

# Load current session data
session_id = st.session_state.current_session_id
session_data = load_session(session_id)
messages = session_data["messages"]
chat_title = session_data["title"]


# --- SIDEBAR ---
st.sidebar.header("📂 Your Research Chats")

# New Chat Button
if st.sidebar.button("➕ New Chat"):
    st.session_state.current_session_id = create_new_session()
    st.rerun()

# Session Selection
sessions = get_session_files()
if sessions:
    # Build options list with titles
    session_options = {f: load_session(f)["title"] for f in sessions}
    
    # We need to find the index of the current session
    try:
        current_index = sessions.index(st.session_state.current_session_id)
    except ValueError:
        current_index = 0
        if sessions:
            st.session_state.current_session_id = sessions[0]

    selected_sid = st.sidebar.selectbox(
        "Select Chat",
        sessions,
        index=current_index,
        format_func=lambda x: session_options[x]
    )
    
    if selected_sid != st.session_state.current_session_id:
        st.session_state.current_session_id = selected_sid
        st.rerun()

# Sidebar options header
st.sidebar.divider()
st.sidebar.header("Options")

# Default Model
selected_model_id = "meta-llama/Llama-3.1-8B-Instruct"

# Delete Chat Button
if st.sidebar.button("🗑️ Delete Current Chat", type="secondary"):
    delete_session(st.session_state.current_session_id)
    # Clear session ID so it gets re-initialized
    del st.session_state.current_session_id
    st.rerun()


# --- MAIN CHAT AREA ---

# Display chat history
for msg in messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


# Chat input
prompt = st.chat_input("Ask your research question")


if prompt:
    # --- STUDY FILTER CHECK ---
    if not is_study_related(prompt):
        st.warning("Please ask only academic or research-related queries.")
        st.stop()

    # Add user message
    user_message = {"role": "user", "content": prompt}
    messages.append(user_message)

    with st.chat_message("user"):
        st.write(prompt)

    # Auto-generate Title for new chats
    if chat_title == "New Chat" and len(messages) == 1:
        new_title = prompt[:30] + ("..." if len(prompt) > 30 else "")
        chat_title = new_title

    # --- CONDITIONAL RETRIEVAL ---
    if is_followup(prompt):
        context_data = ""
        source = "Previous Conversation"
    else:
        with st.spinner(f"Searching archives..."):
            context_data, source = get_context(prompt)

    # --- STRENGTHENED SYSTEM PROMPT ---
    system_prompt = {
        "role": "system",
        "content": """
You are BodhAI, a strict academic research assistant.

CRITICAL RULES:
1. Always follow the conversation context.
2. If the user asks a follow-up question, ONLY use previous discussion.
3. NEVER introduce unrelated topics.
4. Use external data ONLY when needed.
5. If context is unclear, ask for clarification instead of guessing.

STRICT STUDY RULE:
- Only answer academic questions.
- Refuse non-study queries.

FORMAT:
- Definition
- Key Points
- Example
- Conclusion
"""
    }

    # --- COMBINE MEMORY + CONTEXT ---
    augmented_user_message = {
        "role": "user",
        "content": f"""
User Question:
{prompt}

Relevant External Information:
{context_data}

IMPORTANT:
- If this is a follow-up question, ONLY use previous conversation.
- Do NOT introduce new unrelated topics.
- Stay strictly within the discussion context.
"""
    }

    # Send messages to model (System + history + current augmented message)
    llm_messages = [system_prompt] + messages[-11:-1] + [augmented_user_message]

    try:
        response = generate_response(llm_messages, model_id=selected_model_id)
        if response:
            # Add Source in Output
            response += f"\n\n📚 Source: {source}"

    except Exception as e:
        st.error(f"Failed to get response from the model. Error: {e}")
        response = None

    if response:
        # Show assistant message
        with st.chat_message("assistant"):
            st.write(response)

        messages.append({
            "role": "assistant",
            "content": response
        })

        # Save session
        save_session(st.session_state.current_session_id, chat_title, messages)
        st.rerun()