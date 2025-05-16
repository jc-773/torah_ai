# torahAI - front end 

## Background
  - This is a simple RAG application that leverages streamlit for the UI and an orchestration layer I created as the backend (ultimately hitting to openAI)


## Backend Application and how it works
### RAG
  - Using the OpenAI embeddings endpoint, I generate embeddings (vectors) from the query received in the streamlit chat 
  - Using Mongo Atlas, I do a vector search with the generated vectors from step one. This will find similar vectors that I have stored in Atlas
  - It is important to know that by using the Sefaria API (https://developers.sefaria.org/reference/getting-started), I was able to store each line of each book as a chunck in Atlas. With each chunck having its own embedding
  - Enabling the $vectorSearch feature in Mongo Atlas, I was able to find similar embeddings to the ones generated from the chat query
  - I take the similar embeddings and build a prompt
  - I take the prompt and pass it to the OpenAI chat endpoint to generate a child friendly answer

### Other things about the backend
  - The chat requests/responses are low latency and non-blocking, which is great. I was able to achieve a less than 2000 millisecond response by using Spring's Project Reactor event driven architecture (and a singleton virtual thread)
  - This basically creates a chain of non-blocking reactive events that execute in the order of the RAG section explained above

## Environment setup
Create a virtual environment for your Python project
  - python3 -m venv env_name
  - Activate the newly created environment - source env_name/bin/activate
  - Once your env is up and running, you can install your packages - pip install package_name

## Running a streamlit project
  - Navigate to the root directory of the project
  - cd project_name
  - Run the project with the following command - streamlit run main_file.py
  - This will open a tab in your default browser with a chat session

## What next?
  - Hopefully the generated images with the responses stop being weird

