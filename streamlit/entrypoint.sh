#!/bin/bash
set -e

echo ">>> Tentando enviar arquivo estático para o MinIO..."

python upload_static_file.py || true

echo ">>> Iniciando Streamlit..."
streamlit run app.py --server.port=8501 --server.address=0.0.0.0

