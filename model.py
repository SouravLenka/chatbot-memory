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
        max_tokens=500
    )

    return completion.choices[0].message.content