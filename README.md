# 📘 BodhAI - Study Research Assistant

BodhAI is a multi-session academic research assistant built with Streamlit and the Hugging Face Router API.

## Features

- **Multi-session Support**: Create, manage, and switch between multiple research chats in the sidebar.
- **Academic Focus**: Study-mode enabled system prompt for scholarly assistance.
- **Auto-Title Generation**: Automatically names your chats based on your first question.
- **Session Persistence**: Chats are saved as JSON files in the `sessions/` directory.
- **Session Management**: Easily create and switch between multiple research chats.
- **Clean Sidebar**: Simplified interface focused on session management.

## Project Structure

```text
chatbot-memory/
|-- app.py             # BodhAI UI and session management logic
|-- model.py           # Hugging Face Router API client
|-- sessions/          # Directory for storing chat JSON files
|-- requirements.txt   # Project dependencies
|-- .env               # Hugging Face API token
|-- .gitignore
```

## How It Works

- `app.py`: Handles the Streamlit interface, session CRUD operations, and interaction with the model client.
- `model.py`: Uses the `openai` Python client to connect to the Hugging Face Router.
- `sessions/`: Each chat is stored as a JSON object containing a `title` and a list of `messages`.

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
3. Add your Hugging Face token to `.env`:
   ```env
   HF_TOKEN="your_token_here"
   ```

## Run the App

```powershell
streamlit run app.py
```

## Configuration

Default model: `meta-llama/Llama-3.1-8B-Instruct`.
Max context: Last 12 messages are sent to the model for context persistence.
