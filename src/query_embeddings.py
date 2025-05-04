import os
import openai
import requests
from pymongo import MongoClient

# Load environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")
model = "text-embedding-3-small"
uri = os.getenv("MONGO_URI")

# Connect to MongoDB
client = MongoClient(uri)
db = client["torahdb"]
collection = db["genesis_embeddings"]

# Generate embedding for the query
def vector_search_query(query):
    print(f"query: {query}")
    response = openai.embeddings.create(
        input=query,
        model=model
    )
    return response.data[0].embedding

# Perform vector search on MongoDB Atlas
def search_similar_verses(query_embedding, limit=5):
    results = collection.aggregate([
        {
            "$vectorSearch": {
                "queryVector": query_embedding,
                "path": "embedding",
                "numCandidates": 100,
                "limit": limit,
                "index": "vector_index"  # Update with your actual index name
            }
        }
    ])
    return list(results)

# Build prompt to send to OpenAI
def build_prompt(contexts, question):
    context_text = "\n".join([f"- {doc['text']}" for doc in contexts])
    prompt = f"""You're a friendly Jewish centric teacher explaining the Torah to a child.

Context:
{context_text}

Question:
{question}

Answer in a way that's simple, clear, and easy for a kid to understand:"""
    return prompt

# Ask OpenAI with the constructed prompt
def ask_openai(prompt):
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
    )
    reply = response.choices[0].message.content
    print("openai's response =", reply)
    return reply