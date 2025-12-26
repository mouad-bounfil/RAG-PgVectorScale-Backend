from openai import OpenAI
import os
from dotenv import load_dotenv
from timescale_vector import client as ts_client

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = "text-embedding-3-small"


vec_client = ts_client.Sync(
    os.getenv("TIMESCALE_SERVICE_URL"),
    "embeddings",
    1536,
)


def get_embeddings(text):
    embedding = (
        client.embeddings.create(
            input=[text],
            model=model,
        )
        .data[0]
        .embedding
    )
    return embedding


def get_similar_embeddings(text, limit=5):
    embedding = get_embeddings(text)
    search_args = {
        "limit": limit,
    }
    results = vec_client.search(embedding, **search_args)
    return [result[2] for result in results]
