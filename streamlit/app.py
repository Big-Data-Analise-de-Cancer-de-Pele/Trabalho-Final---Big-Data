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
# 🔐 Conexão com MinIO (DOCKER)
# ================================================================
@st.cache_data
def load_from_minio(file_name):
    # Conecta ao serviço MinIO rodando no Docker
    client = Minio(
        "minio:9000",
        access_key="admin",
        secret_key="password",
        secure=False
    )
    bucket = "datasets"
    try:
        response = client.get_object(bucket, file_name)
        data = response.read()
        df = pd.read_csv(BytesIO(data))
        return df
    except Exception as e:
        st.error(f"❌ Erro ao carregar '{file_name}' do MinIO: {e}")
        return None


# ================================================================
# 🧹 Dicionários de Tradução e Normalização
# ================================================================
dx_dict = {
    'nv': 'Nevo Melanocítico (nv)',
    'mel': 'Melanoma (mel)',
    'bkl': 'Queratose Benigna (bkl)',
    'bcc': 'Carcinoma Basocelular (bcc)',
    'akiec': 'Queratose Actínica (akiec)',
    'vasc': 'Lesão Vascular (vasc)',
    'df': 'Dermatofibroma (df)'
}

sex_dict = {
    'male': 'Masculino',
    'female': 'Feminino',
    'unknown': 'Desconhecido'
}

localization_dict = {
    'abdomen': 'Abdômen',
    'scalp': 'Couro Cabeludo',
    'lower extremity': 'Extremidade Inferior',
    'trunk': 'Tronco',
    'upper extremity': 'Extremidade Superior',
    'back': 'Costas',
    'neck': 'Pescoço',
    'face': 'Rosto',
    'chest': 'Peito',
    'foot': 'Pé',
    'ear': 'Orelha',
    'hand': 'Mão',
    'acral': 'Acral',
    'genital': 'Genital',
    'unknown': 'Desconhecido'
}

dx_type_dict = {
    'histo': 'Histopatologia',
    'follow_up': 'Acompanhamento',
    'consensus': 'Consenso',
    'confocal': 'Microscopia Confocal'
}

# Dicionário para renomear as COLUNAS
column_rename_dict = {
    'lesion_id': 'ID da Lesão',
    'image_id': 'ID da Imagem',
    'dx': 'Diagnóstico',
    'dx_type': 'Tipo de Confirmação',
    'age': 'Idade',
    'sex': 'Sexo',
    'localization': 'Localização'
}


# ================================================================
# Seleção de Arquivo
# ================================================================
st.sidebar.header("📁 Escolha o CSV (MinIO)")

file_options = [
    "HAM10000_metadata.csv",
    "hmnist_28_28_L.csv",
    "hmnist_28_28_RGB.csv",
    "hmnist_8_8_L.csv",
    "hmnist_8_8_RGB.csv"
]

file_choice = st.sidebar.selectbox(
    "Selecione um arquivo",
    file_options
)

# Carrega do MinIO
df = load_from_minio(file_choice)

# Se der erro no carregamento, para o script
if df is None:
    st.stop()


# ================================================================
# 🔄 APLICAÇÃO DA TRADUÇÃO (NORMALIZAÇÃO)
# ================================================================
if file_choice == "HAM10000_metadata.csv":
    # 1. Traduzir os VALORES das linhas (antes de renomear as colunas)
    if 'dx' in df.columns:
        df['dx'] = df['dx'].map(dx_dict).fillna(df['dx'])
    if 'sex' in df.columns:
        df['sex'] = df['sex'].map(sex_dict).fillna(df['sex'])
    if 'localization' in df.columns:
        df['localization'] = df['localization'].map(localization_dict).fillna(df['localization'])
    if 'dx_type' in df.columns:
        df['dx_type'] = df['dx_type'].map(dx_type_dict).fillna(df['dx_type'])
    
    # 2. Traduzir os NOMES das colunas
    df = df.rename(columns=column_rename_dict)


st.write(f"### 📄 Arquivo carregado do MinIO: **{file_choice}**")
st.dataframe(df.head())


# ================================================================
# 🧼 Missing Values
# ================================================================
st.subheader("🔍 Dados Faltantes (Missing Values)")
missing = df.isnull().sum()
st.write(missing)


# ================================================================
# 📊 GRÁFICOS SOMENTE PARA HAM10000_metadata.csv
# ================================================================
if file_choice == "HAM10000_metadata.csv":

    # --------------------------------------------------------------
    # 📊 1 — Distribuição dos Tipos de Diagnóstico
    # --------------------------------------------------------------
    st.header("📊 1️⃣ Distribuição dos Tipos de Diagnóstico")

    if "Diagnóstico" in df.columns:
        fig, ax = plt.subplots(figsize=(10, 6)) 
        sns.countplot(
            data=df,
            y="Diagnóstico",
            order=df["Diagnóstico"].value_counts().index,
            palette="viridis",
            ax=ax
        )
        ax.set_title("Contagem por Diagnóstico")
        ax.set_xlabel("Quantidade de Casos")
        ax.set_ylabel("Diagnóstico")
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.warning("Coluna 'Diagnóstico' não encontrada.")


    # --------------------------------------------------------------
    # 🧁 2 — Distribuição por Sexo
    # --------------------------------------------------------------
    st.header("🧁 2️⃣ Distribuição por Sexo")

    if "Sexo" in df.columns:
        sex_counts = df["Sexo"].value_counts()
        labels = [f"{cat} ({qtd})" for cat, qtd in sex_counts.items()]
        colors = sns.color_palette("pastel")[0:len(sex_counts)]

        fig, ax = plt.subplots(figsize=(6, 6))

        ax.pie(
            sex_counts,
            labels=labels,
            autopct="%1.1f%%",
            startangle=90,
            colors=colors,
            wedgeprops={"edgecolor": "black"},
            radius=0.8,
            textprops={"fontsize": 10},
            labeldistance=1.1,
            pctdistance=0.8
        )

        ax.set_title("Distribuição de Sexo", fontsize=12, fontweight="bold")
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.warning("Coluna 'Sexo' não encontrada.")


    # --------------------------------------------------------------
    # 📈 3 — Histograma da Idade
    # --------------------------------------------------------------
    st.header("📈 3️⃣ Histograma da Idade")

    if "Idade" in df.columns:
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.histplot(
            df["Idade"].dropna(),
            bins=20,
            kde=True,
            color="teal",
            ax=ax
        )
        ax.set_title("Distribuição de Idade dos Pacientes")
        ax.set_xlabel("Idade")
        ax.set_ylabel("Frequência")
        plt.tight_layout()
        st.pyplot(fig)

        # --------------------------------------------------------------
        # 🔟 4 — Distribuição por grupos de idade
        # --------------------------------------------------------------
        st.header("🔟 4️⃣ Distribuição por Grupos de Idade")

        max_age = int(df["Idade"].max())
        bins = list(range(0, (max_age // 10 + 2) * 10, 10))
        labels_age = [f"{bins[i]}-{bins[i+1]-1}" for i in range(len(bins)-1)]
        
        df["Faixa Etária"] = pd.cut(df["Idade"], bins=bins, labels=labels_age, right=False)

        age_group_counts = df["Faixa Etária"].value_counts().sort_index()

        fig, ax = plt.subplots(figsize=(12, 5))
        sns.barplot(
            x=age_group_counts.index,
            y=age_group_counts.values,
            palette="plasma",
            ax=ax
        )
        ax.set_title("Distribuição por Faixa Etária (10 em 10 anos)")
        ax.set_xlabel("Faixa Etária")
        ax.set_ylabel("Quantidade")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.warning("Coluna 'Idade' não encontrada.")


    # ================================================================
    # 🆕 GRUPOS 1 e 2
    # ================================================================

    if "Diagnóstico" in df.columns and "Localização" in df.columns:
        # Atualizando os grupos com os nomes traduzidos (valores)
        group1_dx = [dx_dict.get(k, k) for k in ['nv', 'mel', 'bkl']]
        group2_dx = [dx_dict.get(k, k) for k in ['bcc', 'akiec', 'vasc', 'df']]

        # --------------------------------------------------------------
        # 🟦 5 — Grupo 1
        # --------------------------------------------------------------
        st.header("🟦 5️⃣ Grupo 1: Nevo, Melanoma, Queratose B. — Localização")

        # Filtra usando o nome da coluna em PT 'Diagnóstico'
        df_group1 = df[df['Diagnóstico'].isin(group1_dx)]

        if not df_group1.empty:
            localization_dx_counts_g1 = pd.crosstab(df_group1['Diagnóstico'], df_group1['Localização'])
            localization_dx_melt_g1 = localization_dx_counts_g1.stack().reset_index(name='Contagem')

            fig, ax = plt.subplots(figsize=(12, 6))
            sns.barplot(
                data=localization_dx_melt_g1,
                x='Diagnóstico',
                y='Contagem',
                hue='Localização',
                palette='Spectral',
                ax=ax
            )
            ax.set_title('Grupo 1: Diagnóstico vs. Localização')
            ax.set_xlabel("Diagnóstico")
            ax.set_ylabel("Quantidade")
            plt.xticks(rotation=0)
            ax.legend(title='Localização', bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.info("Nenhum dado encontrado para o Grupo 1.")

        # --------------------------------------------------------------
        # 🟥 6 — Grupo 2
        # --------------------------------------------------------------
        st.header("🟥 6️⃣ Grupo 2: Carcinoma, Vascular, etc. — Localização")

        df_group2 = df[df['Diagnóstico'].isin(group2_dx)]

        if not df_group2.empty:
            localization_dx_counts_g2 = pd.crosstab(df_group2['Diagnóstico'], df_group2['Localização'])
            localization_dx_melt_g2 = localization_dx_counts_g2.stack().reset_index(name='Contagem')

            fig, ax = plt.subplots(figsize=(12, 6))
            sns.barplot(
                data=localization_dx_melt_g2,
                x='Diagnóstico',
                y='Contagem',
                hue='Localização',
                palette='Spectral',
                ax=ax
            )
            ax.set_title('Grupo 2: Diagnóstico vs. Localização')
            ax.set_xlabel("Diagnóstico")
            ax.set_ylabel("Quantidade")
            plt.xticks(rotation=0)
            ax.legend(title='Localização', bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.info("Nenhum dado encontrado para o Grupo 2.")

    else:
        st.warning("Colunas 'Diagnóstico' ou 'Localização' não encontradas.")
