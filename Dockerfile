FROM python:3.13.1-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT ["streamlit", "run", "main.py", "--server.address=0.0.0.0"]