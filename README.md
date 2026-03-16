# Student Research Chatbot

A simple Streamlit chatbot for student research help. The app sends chat messages to a hosted language model through the Hugging Face Router API and stores chat history locally in `memory.json`.

## Features

- Streamlit chat interface
- Local chat memory saved to `memory.json`
- Sidebar button to clear saved chat history
- Model responses generated through the OpenAI Python client
- Environment-based API token setup with `.env`

## Project Structure

```text
chatbot-memory/
|-- app.py         # Streamlit UI and chat memory handling
|-- model.py       # Model client setup and response generation
|-- memory.json    # Stored conversation history
|-- .env           # Hugging Face token (local only)
|-- .gitignore
```

## How It Works

`app.py`:
- Builds the Streamlit chat interface
- Loads previous messages from `memory.json`
- Keeps active messages in `st.session_state`
- Sends the latest conversation context to the model
- Saves updated messages after each reply

`model.py`:
- Loads environment variables with `python-dotenv`
- Creates an `OpenAI` client using the Hugging Face Router base URL
- Calls the `meta-llama/Llama-3.1-8B-Instruct` model to generate responses

## Requirements

- Python 3.10+
- A Hugging Face access token with Router/API access

Python packages used:

- `streamlit`
- `openai`
- `python-dotenv`

## Setup

1. Create and activate a virtual environment.

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Install dependencies.

```powershell
pip install streamlit openai python-dotenv
```

3. Add your Hugging Face token to `.env`.

```env
HF_TOKEN="your_hugging_face_token"
```

## Run the App

```powershell
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal, usually:

```text
http://localhost:8501
```

## Chat Memory

- Conversations are saved in `memory.json`
- The app reloads that file when it starts
- Clicking `Clear Chat Memory` removes the saved history from both the UI and file

## Configuration

Current model settings in `model.py`:

- Base URL: `https://router.huggingface.co/v1`
- Model: `meta-llama/Llama-3.1-8B-Instruct`
- Max tokens: `500`

You can change the model name or generation settings directly in `model.py`.

## Notes

- `memory.json` is ignored by Git, so chat history stays local
- `.env` is currently not ignored, so be careful not to commit real tokens
- Error handling exists in the UI, but the current error message may show encoding artifacts for the warning symbol

## Possible Improvements

- Add a `requirements.txt`
- Add token validation and clearer startup errors
- Improve error message formatting
- Add model selection from the UI
- Add memory limits or conversation export
