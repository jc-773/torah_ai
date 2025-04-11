import os
import openai 
import requests
from pymongo import MongoClient

openai.ap_key = os.environ.get("OPENAI_API_KEY")
model = "text-embedding-3-small"
uri = os.getenv("MONGO_URI")
client = MongoClient(uri)
db = client["torahdb"]
collection = db["genesis_embeddings"]

def vector_search_query(query):
    print(f"query: ", query)
    response = openai.embeddings.create(
            input=query,
            model=model
        )
    return response.data[0].embedding
    
def search_similar_verses(query_embedding, limit=5):
    results = collection.aggregate([
        {
            "$vectorSearch": {
                "queryVector": query_embedding,
                "path": "embedding",
                "numCandidates": 100,
                "limit": limit,
                "index": "vector_index" 
            }
        }
    ])
    return list(results)

def build_prompt(contexts, question):
    context_text = "\n".join([f"- {doc['text']}" for doc in contexts])
    prompt = f"""You're a friendly Jewish centric teacher with focus on covenant, law, and Jewish identity while explaining the Torah to a child.
    
        Context:
        {context_text}

        Question:
        {question}

        Answer in a way that's simple, clear, and easy for a kid to understand:"""
        
    return prompt
        
    
        
def ask_openai(prompt):
    response = openai.chat.completions.create(
        model="gpt-4",  # or gpt-3.5-turbo
        messages=[{"role": "user", "content": prompt}],
    )
    print(f"openai's response = ", response.choices[0].message.content)
    return response.choices[0].message.content
