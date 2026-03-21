from tavily import TavilyClient
import arxiv
import wikipedia
import os
from dotenv import load_dotenv

load_dotenv()

# --- Tavily Search ---
tavily_api_key = os.getenv("TAVILY_API_KEY")
tavily = TavilyClient(api_key=tavily_api_key) if tavily_api_key else None

def search_tavily(query):
    if not tavily:
        return ""
    try:
        res = tavily.search(query=query, max_results=3)
        return "\n".join([r["content"] for r in res["results"]])
    except Exception as e:
        print(f"Tavily error: {e}")
        return ""

# --- arXiv Search ---
def search_arxiv(query):
    try:
        search = arxiv.Search(query=query, max_results=2)
        results = []
        # The arxiv client search.results() returns a generator
        for r in search.results():
            results.append(f"{r.title}: {r.summary}")
        return "\n".join(results)
    except Exception as e:
        print(f"arXiv error: {e}")
        return ""

# --- Wikipedia Search ---
def search_wikipedia(query):
    try:
        # wikipedia.summary can raise DisambiguationError or PageError
        return wikipedia.summary(query, sentences=3)
    except Exception as e:
        print(f"Wikipedia error: {e}")
        return ""

# --- Smart Router ---
def get_context(query):
    query_lower = query.lower()
    
    # Heuristics for routing
    if any(word in query_lower for word in ["research", "paper", "study", "ai", "model", "arxiv"]):
        source = "arXiv"
        data = search_arxiv(query)
    elif any(word in query_lower for word in ["define", "what is", "meaning", "wikipedia"]):
        source = "Wikipedia"
        data = search_wikipedia(query)
    else:
        source = "Web"
        data = search_tavily(query)
        
    return data, source
