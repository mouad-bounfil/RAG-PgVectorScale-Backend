from .prompt import SYSTEM_PROMPT
from openai import OpenAI
import os
from dotenv import load_dotenv
from .embeddings import get_similar_embeddings

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print(OPENAI_API_KEY[:4])

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = "gpt-4o-mini"


messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
]


def add_message(message, role="user"):
    messages.append({"role": role, "content": f"User question: {message}"})
    similar_embeddings = get_similar_embeddings(message, limit=3)
    messages.append(
        {
            "role": "assistant",
            "content": f"retrieved context: {'\n'.join(similar_embeddings)}",
        }
    )
    return messages


def conversation_agent(query):
    add_message(query)
    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )
    add_message(response.choices[0].message.content, role="assistant")
    return response.choices[0].message.content
