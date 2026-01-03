# app/Dockerfile

FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY personal_rag_assistant/ /app/

RUN ls -la /app/*

RUN pip3 install -r /app/requirements.txt

RUN curl -fsSL https://ollama.com/install.sh | sh
RUN ollama pull nomic-embed-text
RUN ollama pull gemma3

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "/app/personal_rag_assistant.py", "--server.port=8501", "--server.address=0.0.0.0"]