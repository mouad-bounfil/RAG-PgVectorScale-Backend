from timescale_vector import client
from datetime import timedelta
from timescale_vector.client import uuid_from_time
import os
from dotenv import load_dotenv
from chunks import process_pdf
from openai import OpenAI
from datetime import datetime

load_dotenv()

vec_client = client.Sync(
    os.getenv("TIMESCALE_SERVICE_URL"),
    "embeddings",
    1536,
)

vec_client.create_tables()

vec_client.create_embedding_index(client.DiskAnnIndex())

documents = process_pdf(
    pdf_path="/Users/newuser/Desktop/gen-ai/n_f_t_b_v/VECTOR_DATABASE/full-agents-rag/services/AI.pdf"
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = "text-embedding-3-small"

records = []

for document in documents:
    embedding = (
        client.embeddings.create(
            input=[document["page_content"]],
            model="text-embedding-3-small",
        )
        .data[0]
        .embedding
    )
    records.append(
        {
            "id": uuid_from_time(datetime.now()),
            **document,
            "embedding": embedding,
        }
    )

new_records = []
for object_data in records:
    record_id = object_data["id"]
    record_id = str(uuid_from_time(datetime.now()))
    metadata = object_data["metadata"]
    contents = object_data["page_content"]
    embedding = object_data["embedding"]
    new_records.append((record_id, metadata, contents, embedding))
