# 📘 BodhAI - Study Research Assistant

BodhAI is a powerful, multi-session academic research assistant that combines large language models with real-time data retrieval from **arXiv**, **Wikipedia**, and **Tavily Web Search**. It is designed to provide structured, source-backed, and strictly academic responses.

## 🚀 Key Features

- **🌐 Real-Time Research**:
    - **arXiv**: Fetches the latest research papers and summaries.
    - **Wikipedia**: Provides concise definitions and concepts.
    - **Tavily**: Real-time web search for the most current information.
- **🧠 Smart Context Routing**: Automatically detects the best source for your query.
- **🔄 Follow-up Intelligence**: Recognizes follow-up questions and prioritizes conversation memory to maintain context without unnecessary searches.
- **🛡️ Strict Study Mode**: Only answers academic or research-related queries.
- **📚 Source Attribution**: Every external answer cites its source (arXiv, Wikipedia, or Web).
- **📝 Structured Responses**: Always provides answers in a clear format: Definition, Key Points, Example, and Conclusion.
- **📂 Multi-session Support**: Create, manage, and persist multiple research chats.
- **🎨 Premium UI/UX**: Modern glassmorphic design and dark-mode styling.

## 📁 Project Structure

```text
chatbot-memory/
|-- app.py             # Main UI, session management, and chat logic
|-- model.py           # LLM API client (Hugging Face Router)
|-- retriever.py       # Intelligence layer (arXiv, Wikipedia, Tavily)
|-- sessions/          # Directory for chat history JSON files
|-- requirements.txt   # Project dependencies
|-- .env               # API Tokens (HF_TOKEN, TAVILY_API_KEY)
|-- .gitignore         # Comprehensive ignore list for Python & IDEs
```

## ⚙️ Setup

1. **Environment**: Create and activate a virtual environment.
2. **Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **API Keys**: Add your tokens to a `.env` file in the root directory:
   ```env
   HF_TOKEN="your_huggingface_token"
   TAVILY_API_KEY="your_tavily_api_key"
   ```

## 🏃 Run the App

```bash
streamlit run app.py
```

## 💡 Example Queries

- **arXiv**: "What are the latest research papers on Transformers vs State Space Models?"
- **Wikipedia**: "Define Quantum Entanglement."
- **Web**: "Recent breakthroughs in battery technology for 2024."
- **Follow-up**: "Can you elaborate on that last point?" (Uses conversation memory).

## ⚠️ Configuration

- **Default Model**: `meta-llama/Llama-3.1-8B-Instruct` (via Hugging Face Router).
- **Context Management**: 
    - **Memory Summary**: Uses LLM-generated summaries to maintain context across long conversations.
    - **Rolling Window**: Combines the last 10 messages with the summary for maximum relevance.
- **Search Router**: Intelligently switches between arXiv (research), Wikipedia (concepts), and Tavily (web) based on query semantics.

---
*Created with ❤️ for scholarly research.*
