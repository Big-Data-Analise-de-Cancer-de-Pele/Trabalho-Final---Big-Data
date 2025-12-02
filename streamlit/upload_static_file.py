from minio import Minio
import time

MINIO_HOST = "minio:9000"
ACCESS_KEY = "minio"
SECRET_KEY = "minio123"

BUCKET_NAME = "datalake-bronze"
OBJECT_NAME = "user_behavior_dataset.csv"
FILE_PATH = "/app/data/user_behavior_dataset.csv"

client = Minio(
    MINIO_HOST,
    access_key=ACCESS_KEY,
    secret_key=SECRET_KEY,
    secure=False
)

# tenta 10 vezes
for i in range(10):
    try:
        client.list_buckets()
        break
    except Exception:
        print("MinIO ainda não está pronto...")
        time.sleep(2)

# cria bucket se não existir
if not client.bucket_exists(BUCKET_NAME):
    client.make_bucket(BUCKET_NAME)

# envia arquivo
client.fput_object(
    bucket_name=BUCKET_NAME,
    object_name=OBJECT_NAME,
    file_path=FILE_PATH
)

print("Arquivo enviado com sucesso!")

