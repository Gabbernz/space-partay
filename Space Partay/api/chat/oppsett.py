# setup_kb.py
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# 1) Last opp fil
file = client.files.create(
    file=open("partiprogram.md", "rb"),
    purpose="assistants"
)

# 2) Lag vector store
vs = client.vector_stores.create(
    name="Space Partay KB"
)

# 3) Knytt filen til vector store
client.vector_stores.files.create(
    vector_store_id=vs.id,
    file_id=file.id
)

print("VECTOR_STORE_ID =", vs.id)
