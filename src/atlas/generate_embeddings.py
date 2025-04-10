import os
import openai 
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient


openai.ap_key = os.environ.get("OPENAI_API_KEY")
model = "text-embedding-3-small"
uri = os.getenv("MONGO_URI")
client = MongoClient(uri)
db = client["torahdb"]
collection = db["genesis_embeddings"]

def fetch_data():
    response = requests.get("https://www.sefaria.org/api/texts/Genesis.1?lang=english")
    data = response.json()
    print(response.text)
    
    clean_verses = []
    for verse in data["text"]:
        soup = BeautifulSoup(verse, "html.parser")
        clean_verses.append(soup.get_text())

    # Print cleaned text
    for i, verse in enumerate(clean_verses, 1):
        create_embeddings(verse)
        print(f"Genesis 1:{i} - {verse}")

def create_embeddings(verse):
    existing = collection.find_one({"text": verse})
    if existing:
        print("Embedding already exists for this verse. Done.")
    else:
        print("creating embeddings...")
        response = openai.embeddings.create(
            input=[verse],
            model=model
        )
        embedding = response.data[0].embedding
        insert_embeddings(verse, embedding, collection)
    

def insert_embeddings(verse, embedding, collection):
    # Check if the verse already exists in the collection
    existing = collection.find_one({"text": verse})
    
    if existing:
        print("Embedding already exists for this verse. Skipping.")
    else:
        collection.insert_one({
            "text": verse,
            "embedding": embedding,
            "source": "Genesis"
        })
        print("Embedding inserted for new verse.")
        

#HELPER
def verify_with_readback(collection):
    doc = collection.find_one({"source": "Genesis"})
    print(f"verify: ", doc)
    

    
fetch_data()
