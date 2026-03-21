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

# --- UI CUSTOMIZATION ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    
    html, body, [class*="st-at"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
    }
    
    .stChatMessage {
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .stChatMessage.user {
        background-color: rgba(52, 152, 219, 0.1);
        border-left: 5px solid #3498db;
    }
    
    .stChatMessage.assistant {
        background-color: rgba(255, 255, 255, 0.05);
        border-left: 5px solid #2ecc71;
    }
    
    .stSidebar {
        background-color: #0d1117 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .source-box {
        background-color: rgba(0, 0, 0, 0.3);
        padding: 12px;
        border-radius: 10px;
        border: 1px solid rgba(52, 152, 219, 0.3);
        font-size: 0.85em;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

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
        return {"title": "New Chat", "messages": [], "summary": "", "topic": "General Research"}

def save_session(session_id, title, messages, summary="", topic="General Research"):
    data = {"title": title, "messages": messages, "summary": summary, "topic": topic}
    with open(os.path.join(SESSIONS_DIR, session_id), "w") as f:
        json.dump(data, f, indent=2)

def create_new_session():
    session_id = f"chat_{int(time.time())}.json"
    save_session(session_id, "New Chat", [], "", "General Research")
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
chat_summary = session_data.get("summary", "")
chat_topic = session_data.get("topic", "General Research")

# Default Model
selected_model_id = "meta-llama/Llama-3.1-8B-Instruct"


# --- SIDEBAR ---
st.sidebar.header("📂 Your Research Chats")

# New Chat Button
if st.sidebar.button("➕ New Chat"):
    st.session_state.current_session_id = create_new_session()
    st.rerun()

# Session Selection
sessions = get_session_files()
if sessions:
    # Build options list with titles (cached for performance)
    session_options = {f: load_session(f)["title"] for f in sessions}
    
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

# --- CHAT MANAGEMENT ---
st.sidebar.divider()
st.sidebar.subheader("⚙️ Chat Settings")

# Rename Chat
new_title = st.sidebar.text_input("Rename Current Chat", value=chat_title)
if new_title != chat_title:
    save_session(st.session_state.current_session_id, new_title, messages)
    st.rerun()

# Delete Chat
if st.sidebar.button("🗑️ Delete Current Chat", type="secondary", use_container_width=True):
    delete_session(st.session_state.current_session_id)
    del st.session_state.current_session_id
    st.rerun()

# Topic Display
st.sidebar.info(f"📍 Topic: {chat_topic}")
st.sidebar.caption(f"📝 Summary: {chat_summary[:100]}..." if chat_summary else "")

# --- MODE SELECTOR ---
st.sidebar.divider()
st.sidebar.subheader("🎯 Intelligence Mode")
selected_mode = st.sidebar.selectbox(
    "Select Mode",
    ["Study Mode", "Research Mode"],
    help="Study Mode: Precise academic answers. Research Mode: Deep search with extensive sources."
)
st.sidebar.info(f"Currently in {selected_mode}")

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
        context_data = []
        source_type = "Previous Conversation"
    else:
        with st.spinner(f"Searching {selected_mode} sources..."):
            context_data, source_type = get_context(prompt)

    # Prepare context string for LLM
    context_str = "\n\n".join([f"Source: {c['title']}\nContent: {c['content']}" for c in context_data])

    # --- STRENGTHENED SYSTEM PROMPT ---
    system_prompt_content = f"""
You are BodhAI, a strict academic research assistant. Current Mode: {selected_mode}.
Current Topic: {chat_topic}
Previous Context Summary: {chat_summary}

CRITICAL RULES:
1. Always follow the conversation context.
2. If the user asks a follow-up question, ONLY use previous discussion.
3. NEVER introduce unrelated topics.
4. Use external data ONLY when needed.
5. If context is unclear, ask for clarification instead of guessing.
6. Rate your confidence from 0-100% based on available information.

STRICT STUDY RULE:
- Only answer academic questions.
- Refuse non-study queries.

FORMAT:
- Definition
- Key Points
- Example
- Conclusion
- Confidence Score: [Score]%

Include 2-3 short follow-up suggestions at the very end in a 'Suggestions' section.
"""
    system_prompt = {"role": "system", "content": system_prompt_content}

    # --- COMBINE MEMORY + CONTEXT ---
    augmented_user_message = {
        "role": "user",
        "content": f"""
User Question:
{prompt}

Relevant External Information:
{context_str if context_str else "No additional context found."}

IMPORTANT:
- If this is a follow-up question, ONLY use previous conversation.
- Use the provided context to answer accurately.
- Mention the sources provided if used.
"""
    }

    # Send messages to model
    llm_messages = [system_prompt] + messages[-11:-1] + [augmented_user_message]

    try:
        response = generate_response(llm_messages, model_id=selected_model_id)
        if response:
            # --- ADD SOURCE CITATIONS ---
            if context_data:
                citation_text = "\n\n---\n**📚 Sources Used:**\n"
                for i, source in enumerate(context_data, 1):
                    citation_text += f"{i}. [{source['title']}]({source['link']})\n"
                response += citation_text
            else:
                response += f"\n\n📚 Source: {source_type}"

    except Exception as e:
        st.error(f"Failed to get response from the model. Error: {e}")
        response = None

    if response:
        # Update Topic for new chats
        if chat_topic == "General Research" and len(messages) >= 2:
            chat_topic = chat_title

        # Update Summary every 3 messages
        if len(messages) % 6 == 0:
            from model import summarize_history
            chat_summary = summarize_history(messages)

        # Show assistant message
        with st.chat_message("assistant"):
            st.write(response)

        messages.append({
            "role": "assistant",
            "content": response
        })

        # Save session
        save_session(st.session_state.current_session_id, chat_title, messages, chat_summary, chat_topic)
        st.rerun()