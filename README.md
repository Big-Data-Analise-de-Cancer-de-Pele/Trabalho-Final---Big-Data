
# 📘 Tutorial – Ambiente Streamlit + MinIO + Dataset HAM10000

Este guia apresenta o passo a passo para configurar o ambiente em Docker com Streamlit e MinIO, fazer upload do dataset HAM10000 e rodar a aplicação no navegador.

---

## 🚀 1. Limpar contêineres antigos

Antes de tudo, remova contêineres antigos — principalmente os MinIO criados pelo professor:

```bash
docker container prune
```

---

## 📂 2. Entrar na pasta do projeto Streamlit

```bash
cd /opt/ceub-bigdata/streamlit
```

---

## 🏗️ 3. Subir o ambiente com Docker Compose

```bash
docker-compose up -d
```

---

## 🔌 4. Ajustar portas (caso necessário)

Se houver algo usando a porta **8501** (geralmente Flask), derrube o serviço:

```bash
sudo lsof -i :8501
kill -9 <PID>
```

Garanta que o Docker está expondo a porta:

```
8501 -> 8501
```

---

## 🌐 5. Acessar o MinIO

Abra no navegador:

```
http://localhost:9001
```

### 🔑 Login do MinIO

* **Usuário:** admin
* **Senha:** password

---

## 📁 6. Criar bucket e enviar o dataset HAM10000

### 6.1. Baixar dataset HAM10000 (CSV)

🔗 Google Drive:
[https://drive.google.com/drive/folders/1xGpaP8dTsiaH_kZ5RxjmhL_AYWPwNfsZ?usp=sharing](https://drive.google.com/drive/folders/1xGpaP8dTsiaH_kZ5RxjmhL_AYWPwNfsZ?usp=sharing)

### 6.2. (Opcional) Dataset completo original

🔗 Kaggle:
[https://www.kaggle.com/datasets/kmader/skin-cancer-mnist-ham10000](https://www.kaggle.com/datasets/kmader/skin-cancer-mnist-ham10000)

### 6.3. Criar bucket `datasets` (se não existir)

Acesse:

```
http://localhost:9001/browser
```

E crie o bucket:

```
datasets
```

### 6.4. Fazer upload dos arquivos CSV no MinIO

Acesse:

```
http://localhost:9001/browser/datasets
```

Faça upload dos arquivos do dataset.

---

## 🟩 7. Abrir o Streamlit

Depois de enviar os arquivos ao MinIO, abra:

```
http://localhost:8501/
```

A aplicação deverá carregar normalmente.

---

# 🛠️ DEBUG – Caso algo dê errado

Utilize:

```bash
docker-compose down
docker-compose build
docker-compose up -d
docker logs -f streamlit-app
```

---

## 📚 Dicionário de Dados (HAM10000)

Para entender as colunas do dataset:

🔗 [https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/DBW86T](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/DBW86T)

