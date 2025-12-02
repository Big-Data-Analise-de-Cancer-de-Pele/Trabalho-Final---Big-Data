# ===============================================================
# Streamlit – Visualização dos datasets HMNIST direto do MinIO
# ===============================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from minio import Minio
from io import BytesIO

st.set_page_config(page_title="Análise HMNIST – MinIO", layout="wide")

# ------------------------------------------
# 🔐 Conexão com o MinIO
# ------------------------------------------
@st.cache_data
def load_from_minio(file_name):
    """Baixa um arquivo CSV do MinIO e retorna como DataFrame."""
    client = Minio(
        "minio:9000",
        access_key="admin",
        secret_key="password",
        secure=False
    )

    bucket = "datasets"

    response = client.get_object(bucket, file_name)
    data = response.read()
    df = pd.read_csv(BytesIO(data))
    return df


# ------------------------------------------
# 📌 Lista dos arquivos disponíveis
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

# ------------------------------------------
# 🗂️ Escolha do dataset
# ------------------------------------------
file_choice = st.selectbox("Escolha um arquivo CSV:", csv_files)

st.info(f"Carregando **{file_choice}** do MinIO...")
df = load_from_minio(file_choice)

st.success(f"Dataset carregado com sucesso! Shape: {df.shape}")

# ------------------------------------------
# 📄 Mostrar primeiras linhas
# ------------------------------------------
st.subheader("📄 Pré-visualização do dataset")
st.dataframe(df.head())

# ------------------------------------------
# 📊 Informações básicas
# ------------------------------------------
st.subheader("📊 Informações Estatísticas")
st.write(df.describe())

# ------------------------------------------
# 🔎 Visualizações específicas por tipo
# ------------------------------------------

# Detectar colunas numéricas
numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

# Detectar se tem coluna "label"
tem_label = "label" in df.columns

# ------------------------------------------
# 🔥 GRÁFICO: distribuição das labels
# ------------------------------------------
if tem_label:

    st.header("1️⃣ Distribuição das classes (label)")

    fig, ax = plt.subplots(figsize=(7,4))
    sns.countplot(x=df["label"], ax=ax)
    ax.set_title("Distribuição das Labels (0 a 6)")
    st.pyplot(fig)

    st.info("""
    **Significado das classes HMNIST:**

    0 → Armadura (sem câncer)  
    1 → Melanocítico (câncer)  
    2 → Benigno queratose (sem câncer)  
    3 → Basocelular (câncer)  
    4 → Ceratose actínica (câncer)  
    5 → Dermatofibroma (sem câncer)  
    6 → Nevus (sem câncer)
    """)

# ------------------------------------------
# 🔥 Correlação (metadata do HAM10000)
# ------------------------------------------
if file_choice == "HAM10000_metadata.csv":
    st.header("2️⃣ Correlação entre variáveis (metadata)")

    numeric_df = df.select_dtypes(include=["number"])

    fig, ax = plt.subplots(figsize=(10,5))
    sns.heatmap(numeric_df.corr(), cmap="Blues", annot=False)
    st.pyplot(fig)

# ------------------------------------------
# 🔥 Gráfico de amostra de pixels (somente datasets de imagens)
# ------------------------------------------
if "pixel" in df.columns[1].lower() or df.shape[1] in [64+1, 784+1, 64*3+1, 784*3+1]:

    st.header("3️⃣ Estatísticas dos Pixels")

    first_pixels = df.iloc[:, 1:].mean().mean()

    st.metric(
        "Média geral dos valores de pixel (0–255)",
        f"{first_pixels:.2f}"
    )

    # Distribuição geral dos pixels
    st.subheader("📌 Distribuição geral dos pixels")

    fig, ax = plt.subplots(figsize=(8,4))
    sns.histplot(df.iloc[:,1:].values.flatten(), bins=50, ax=ax)
    ax.set_title("Distribuição dos valores dos pixels")
    st.pyplot(fig)

# ------------------------------------------
# 🔥 Gráfico de missing values
# ------------------------------------------
st.header("4️⃣ Valores faltantes (Missing Values)")

missing = df.isnull().sum()
missing = missing[missing > 0]

if missing.empty:
    st.success("Nenhuma coluna com valores ausentes! ✔️")
else:
    st.warning("Existem valores ausentes:")
    st.write(missing)

    fig, ax = plt.subplots(figsize=(6,4))
    missing.plot(kind="bar", ax=ax)
    st.pyplot(fig)

# ------------------------------------------
# 🟦 Conclusão
# ------------------------------------------
st.success("🎉 Análise concluída! Escolha outro CSV para continuar explorando.")
