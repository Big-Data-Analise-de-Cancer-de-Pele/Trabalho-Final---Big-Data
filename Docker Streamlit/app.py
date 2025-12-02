# ===============================================================
# Streamlit – Versão OTIMIZADA (Lazy Loading)
# ===============================================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from minio import Minio
from io import BytesIO
# REMOVIDO DAQUI: import tensorflow e keras (vão para dentro do botão)

st.set_page_config(page_title="Análise HMNIST – MinIO", layout="wide")

# ------------------------------------------
# 🔐 Conexão com o MinIO (Com Proteção)
# ------------------------------------------
@st.cache_data
def load_from_minio(file_name):
    try:
        client = Minio(
            "minio:9000",
            access_key="admin",
            secret_key="password",
            secure=False
        )
        bucket = "datasets"
        
        # Verifica se o bucket existe antes de tentar ler
        if not client.bucket_exists(bucket):
            st.error(f"O bucket '{bucket}' ainda não existe ou o MinIO está iniciando.")
            return None

        response = client.get_object(bucket, file_name)
        data = response.read()
        return pd.read_csv(BytesIO(data))
    except Exception as e:
        st.error(f"Erro ao conectar no MinIO: {e}")
        return None

# ------------------------------------------
# 📌 Interface Principal
# ------------------------------------------
csv_files = [
    "hmnist_8_8_L.csv",
    "hmnist_8_8_RGB.csv",
    "hmnist_28_28_L.csv",
    "hmnist_28_28_RGB.csv",
    "HAM10000_metadata.csv"
]

st.title("🔍 Visualizador HMNIST + Metadata (MinIO)")
st.markdown("Selecione um dataset para explorar diretamente do MinIO.")

file_choice = st.selectbox("Escolha um arquivo CSV:", csv_files)
df = load_from_minio(file_choice)

if df is not None:
    st.success(f"Dataset carregado! Shape: {df.shape}")
    st.dataframe(df.head())
    
    # Verifica se é imagem
    is_image_dataset = (
        ("label" in df.columns) and 
        (df.shape[1] > 50) # Assumindo que se tem muitas colunas, é pixel
    )
else:
    st.warning("Aguardando conexão com os dados...")
    st.stop() # Para a execução aqui se não tiver dados

# ------------------------------------------
# 🔥 TREINAMENTO DO MODELO (Agora Leve!)
# ------------------------------------------
st.header("🧠 Treinamento da CNN")

if is_image_dataset:
    if st.button("🚀 Treinar Modelo CNN"):
        st.info("Carregando TensorFlow... (isso pode demorar na primeira vez)")
        
        # --- IMPORTAÇÃO PREGUIÇOSA (SÓ ACONTECE AQUI) ---
        import tensorflow as tf
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
        from sklearn.model_selection import train_test_split
        from tensorflow.keras.utils import to_categorical
        # ------------------------------------------------

        st.info("Iniciando treinamento...")

        # Preparação dos dados
        y = df["label"].astype(int).values
        X = df.drop("label", axis=1).values
        
        # Reshape dinâmico
        if X.shape[1] == 28*28:
            X = X.reshape(-1, 28, 28, 1)
        elif X.shape[1] == 28*28*3:
            X = X.reshape(-1, 28, 28, 3)
        else:
            # Fallback para 8x8 se for o caso
            size = int(np.sqrt(X.shape[1]))
            X = X.reshape(-1, size, size, 1)

        X = X / 255.0
        num_classes = len(np.unique(y))
        y_cat = to_categorical(y, num_classes)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y_cat, test_size=0.2, random_state=42, stratify=y
        )

        model = Sequential([
            Conv2D(32, (3,3), activation="relu", padding='same', input_shape=(X.shape[1:])),
            MaxPooling2D(),
            Flatten(),
            Dense(64, activation="relu"),
            Dense(num_classes, activation="softmax")
        ])

        model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
        
        history = model.fit(X_train, y_train, epochs=5, batch_size=32, validation_split=0.1, verbose=0)
        
        loss, acc = model.evaluate(X_test, y_test, verbose=0)
        st.success(f"🎉 Acurácia: **{acc*100:.2f}%**")
        
        # Salva na sessão para usar depois
        st.session_state["model"] = model
        st.session_state["raw_df"] = df

        # Plot
        fig, ax = plt.subplots()
        ax.plot(history.history["accuracy"], label="Treino")
        ax.plot(history.history["val_accuracy"], label="Validação")
        ax.legend()
        st.pyplot(fig)

# Seção de previsão simplificada...
if "model" in st.session_state:
    st.success("Modelo pronto para previsões!")