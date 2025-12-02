FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Instala curl e mc
RUN apt-get update && apt-get install -y curl \
    && curl -O https://dl.min.io/client/mc/release/linux-amd64/mc \
    && mv mc /usr/local/bin/mc \
    && chmod +x /usr/local/bin/mc

# Copia app e scripts
COPY app.py .
COPY upload_static_file.py .
COPY entrypoint.sh .

# Dá permissão de execução
RUN chmod +x entrypoint.sh

EXPOSE 8501

ENTRYPOINT ["./entrypoint.sh"]

