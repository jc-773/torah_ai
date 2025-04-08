import requests

def fetch_genesis():
    response = requests.get("https://www.sefaria.org/api/texts/Genesis.2?lang=english")
    print(response.text)
    
fetch_genesis()