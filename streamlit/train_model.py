import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0'  # Mostra logs do TensorFlow

import pandas as pd
import numpy as np
from minio import Minio
from io import BytesIO
import tensorflow as tf
from tensorflow.keras import layers, models

print("🔄 Iniciando treinamento da CNN HMNIST...")

# =================================================
# 🔐 Conectar ao MinIO
# =================================================
print("🔌 Conectando ao MinIO...")

client = Minio(
    "minio:9000",
    access_key="admin",
    secret_key="password",
    secure=False
)

bucket = "datasets"
file_name = "hmnist_28_28_RGB.csv"

print(f"📥 Baixando dataset: {file_name} ...")

# =================================================
# 📥 Baixar dataset
# =================================================
try:
    response = client.get_object(bucket, file_name)
    data = response.read()
    df = pd.read_csv(BytesIO(data))
    print("📄 CSV carregado com sucesso!")
except Exception as e:
    print("❌ Erro ao baixar CSV do MinIO:", e)
    exit()

print("📊 Shape do dataset:", df.shape)

# =================================================
# 🔧 Preparar dados
# =================================================
print("🔧 Preparando dados X e y ...")

X = df.drop("label", axis=1).values.astype("float32") / 255.0
y = df["label"].values.astype("int32")

print("📦 Normalizando e convertendo formato...")

X = X.reshape(-1, 28, 28, 3)

print("📐 Novo shape de X:", X.shape)
print("🏷️ Número de classes:", len(np.unique(y)))

# =================================================
# 🧠 Modelo CNN
# =================================================
print("🧠 Construindo modelo CNN...")

model = models.Sequential([
    layers.Conv2D(32, (3,3), activation="relu", input_shape=(28,28,3)),
    layers.MaxPooling2D((2,2)),

    layers.Conv2D(64, (3,3), activation="relu"),
    layers.MaxPooling2D((2,2)),

    layers.Flatten(),
    layers.Dense(128, activation="relu"),
    layers.Dense(7, activation="softmax"),
])

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

print("🏋️ Treinando modelo (isso pode demorar um pouco)...\n")

history = model.fit(
    X, y,
    epochs=8,
    batch_size=32,
    verbose=1
)

# =================================================
# 💾 Salvar modelo localmente
# =================================================
MODEL_NAME = "cnn_hmnist.h5"

print("\n💾 Salvando modelo localmente:", MODEL_NAME)
model.save(MODEL_NAME)

# =================================================
# 📦 Criar bucket 'models' se não existir
# =================================================
if not client.bucket_exists("models"):
    print("📦 Bucket 'models' não existe. Criando...")
    client.make_bucket("models")
else:
    print("📦 Bucket 'models' já existe.")

# =================================================
# ⬆️ Upload para MinIO
# =================================================
print("⬆️ Enviando modelo para MinIO...")

try:
    client.fput_object("models", MODEL_NAME, MODEL_NAME)
    print("✅ Upload concluído com sucesso!")
except Exception as e:
    print("❌ Falha no upload:", e)
    exit()

print("\n🎉 Modelo treinado e enviado ao MinIO com sucesso!")
