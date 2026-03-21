import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.getenv("HF_TOKEN"),
)

def generate_response(messages, model_id="meta-llama/Llama-3.1-8B-Instruct"):
    completion = client.chat.completions.create(
        model=model_id,
        messages=messages,
        max_tokens=600
    )
    return completion.choices[0].message.content

def summarize_history(messages, model_id="meta-llama/Llama-3.1-8B-Instruct"):
    if not messages:
        return ""
    
    summary_prompt = [
        {"role": "system", "content": "You are a research assistant. Summarize the following conversation history into a concise 2-3 sentence paragraph focusing on the main research topics discussed."},
        {"role": "user", "content": str(messages)}
    ]
    
    try:
        completion = client.chat.completions.create(
            model=model_id,
            messages=summary_prompt,
            max_tokens=150
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Summarization error: {e}")
        return ""