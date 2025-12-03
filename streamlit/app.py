import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from minio import Minio
from io import BytesIO

# ================================================================
# ⚙️ CONFIGURAÇÃO DO STREAMLIT (DEVE SER A PRIMEIRA LINHA DO SCRIPT)
# ================================================================
st.set_page_config(page_title="Análise HMNIST – MinIO", layout="wide")


# ================================================================
# 🔐 Conexão com MinIO
# ================================================================
@st.cache_data
def load_from_minio(file_name):
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


# ================================================================
# Seleção de Arquivo
# ================================================================
st.sidebar.header("📁 Escolha o CSV")
file_choice = st.sidebar.selectbox(
    "Selecione um arquivo",
    [
        "HAM10000_metadata.csv",
        "hmnist_28_28_L.csv",
        "hmnist_28_28_RGB.csv",
        "hmnist_8_8_L.csv",
        "hmnist_8_8_RGB.csv"
    ]
)

df = load_from_minio(file_choice)

st.write(f"### 📄 Arquivo carregado: **{file_choice}**")
st.dataframe(df.head())


# ================================================================
# 🧼 Missing Values
# ================================================================
st.subheader("🔍 Missing Values")
missing = df.isnull().sum()
st.write(missing)


# ================================================================
# 📊 GRÁFICOS SOMENTE PARA HAM10000_metadata.csv
# ================================================================
if file_choice == "HAM10000_metadata.csv":

    # --------------------------------------------------------------
    # 📊 1 — Distribuição dos Tipos de Diagnóstico
    # --------------------------------------------------------------
    st.header("📊 1️⃣ Distribuição dos Tipos de Diagnóstico (dx)")

    fig, ax = plt.subplots(figsize=(10/3, 5/3))
    sns.countplot(
        data=df,
        x="dx",
        order=df["dx"].value_counts().index,
        palette="viridis",
        ax=ax
    )
    ax.set_title("Distribuição dos Tipos de Diagnóstico (dx)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    st.pyplot(fig)


    # --------------------------------------------------------------
    # --------------------------------------------------------------
    st.header("🧁 2️⃣ Distribuição por Sexo (sex) — Gráfico de Pizza")

    sex_counts = df["sex"].value_counts()
    labels = [f"{cat} ({qtd})" for cat, qtd in sex_counts.items()]
    colors = sns.color_palette("pastel")[0:len(sex_counts)]

    fig, ax = plt.subplots(figsize=(7/3, 7/3))

    ax.pie(
        sex_counts,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90,
        colors=colors,
        wedgeprops={"edgecolor": "black"},
        radius=0.66,                 # 🔥 pizza 2x maior que antes
        textprops={"fontsize": 6, "fontweight": "bold"},  # 🔥 TEXTO MELHORADO
        labeldistance=1.15,
        pctdistance=0.75
    )

    ax.set_title("Distribuição de Sexo", fontsize=10, fontweight="bold")
    plt.tight_layout()
    st.pyplot(fig)



    # --------------------------------------------------------------
    # 📈 3 — Histograma da Idade
    # --------------------------------------------------------------
    st.header("📈 3️⃣ Histograma da Idade (age)")

    fig, ax = plt.subplots(figsize=(10/3, 5/3))
    sns.histplot(
        df["age"].dropna(),
        bins=20,
        kde=True,
        color="teal",
        ax=ax
    )
    ax.set_title("Distribuição de Idade")
    plt.tight_layout()
    st.pyplot(fig)


    # --------------------------------------------------------------
    # 🔟 4 — Distribuição por grupos de idade
    # --------------------------------------------------------------
    st.header("🔟 4️⃣ Distribuição por Grupos de Idade (0–9, 10–19...)")

    max_age = int(df["age"].max())
    bins = list(range(0, (max_age // 10 + 2) * 10, 10))
    labels = [f"{bins[i]}-{bins[i+1]-1}" for i in range(len(bins)-1)]
    df["age_group"] = pd.cut(df["age"], bins=bins, labels=labels, right=False)

    age_group_counts = df["age_group"].value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(12/3, 5/3))
    sns.barplot(
        x=age_group_counts.index,
        y=age_group_counts.values,
        palette="plasma",
        ax=ax
    )
    ax.set_title("Distribuição por Grupos de Idade (10 em 10 anos)")
    plt.xticks(rotation=45, ha="right")
    ax.margins(x=0.05)
    plt.tight_layout()
    st.pyplot(fig)


    # ================================================================
    # 🆕 GRUPOS 1 e 2
    # ================================================================

    group1_dx = ['nv', 'mel', 'bkl']
    group2_dx = ['bcc', 'akiec', 'vasc', 'df']


    # --------------------------------------------------------------
    # 🟦 5 — Grupo 1
    # --------------------------------------------------------------
    st.header("🟦 5️⃣ Grupo 1: nv, mel, bkl — Localização por Diagnóstico")

    df_group1 = df[df['dx'].isin(group1_dx)]

    localization_dx_counts_g1 = pd.crosstab(df_group1['dx'], df_group1['localization'])
    localization_dx_melt_g1 = localization_dx_counts_g1.stack().reset_index(name='Contagem')

    fig, ax = plt.subplots(figsize=(14/3, 8/3))
    sns.barplot(
        data=localization_dx_melt_g1,
        x='dx',
        y='Contagem',
        hue='localization',
        palette='Spectral',
        ax=ax
    )
    ax.set_title('Grupo 1: Contagem de Casos (nv, mel, bkl) vs. Localização')

    plt.xticks(rotation=0)
    ax.margins(y=0.1)

    # legenda fora
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()
    st.pyplot(fig)


    # --------------------------------------------------------------
    # 🟥 6 — Grupo 2
    # --------------------------------------------------------------
    st.header("🟥 6️⃣ Grupo 2: bcc, akiec, vasc, df — Localização por Diagnóstico")

    df_group2 = df[df['dx'].isin(group2_dx)]

    localization_dx_counts_g2 = pd.crosstab(df_group2['dx'], df_group2['localization'])
    localization_dx_melt_g2 = localization_dx_counts_g2.stack().reset_index(name='Contagem')

    fig, ax = plt.subplots(figsize=(14/3, 8/3))
    sns.barplot(
        data=localization_dx_melt_g2,
        x='dx',
        y='Contagem',
        hue='localization',
        palette='Spectral',
        ax=ax
    )
    ax.set_title('Grupo 2: Contagem de Casos (bcc, akiec, vasc, df) vs. Localização')

    plt.xticks(rotation=0)
    ax.margins(y=0.1)

    # legenda fora
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()
    st.pyplot(fig)
