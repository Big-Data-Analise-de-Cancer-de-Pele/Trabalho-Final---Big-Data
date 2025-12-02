FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 8501

# Importante: Rodar direto pelo Docker, sem script intermediário
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]