# torahAI - front end 

## Background
  - Created by Jonathan Clark (github: jc-773)
  - This is a simple streamlit client for torahAI backend
  - Must have an openAI API key for it to work
  - Unless backend jar is running locally this client won't work. I just containerized the backend and will deploy to prod soon...

## Environment setup
  - Create a virtual environment for your Python project
  - python3 -m venv env_name
  - Activate the newly created environment - source env_name/bin/activate
  - Once your env is up and running, you can install your packages - pip install package_name

## Running a streamlit project
  - Navigate to the root directory of the project
  - cd project_name
  - Run the project with the following command - streamlit run main_file.py
  - This will open a tab in your default browser with a chat session

## Continuous Integration
  - Right now, when a change is made to master, I have a YAML job that kicks off with the following steps:
      - checkout the repo
      - downloads jdk 23
      - run the unit tests using the  maven wrapper (quality gate)
      - if the tests pass, build the project with maven wrapper (quality gate)
      - sets up AWS credentials
      - logs into AWS ECR
      - sets the image URI with ECR repo and ECR registry
      - builds the app into a docker image pointing at image URI at "." (root directory)
      - run docker push to deploy the image to AWS ECR tagged with "latest"
