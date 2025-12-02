docker exec -it streamlit-app python3 - << 'EOF'
import socket
s = socket.socket()
try:
    s.settimeout(3)
    s.connect(("minio", 9000))
    print("CONEXÃO OK -> minio:9000 👍")
except Exception as e:
    print("FALHOU:", e)
EOF

