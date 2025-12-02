#STREAMLIT
cd /opt/ceub-bigdata/streamlit
docker-compose up -d


#Fluxo de upload de dataset pro minio -> spark -> streamlit

#abrir direcionamento de portas
tirar o do flask 2 
e adicionar uma porta streamlit 
8501 8501

#quando dar erro de docker minio sendo usado: 
docker container prune


  faz o upload no minio do dataset. e depois abre o streamlit #(se nao vier bucket datasets, crie)
http://localhost:9001/browser/datasets
http://localhost:8501/


#======================DEBUG======================

docker-compose down; docker-compose build; docker-compose up -d ; docker logs -f streamlit-app 


#eu parei quando eu tava colocando o dataset d csv dentro do minio pelo comando mc



database pra ser usada
https://www.kaggle.com/datasets/kmader/skin-cancer-mnist-ham10000
#dicionario de dados desse: 
https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/DBW86T


https://github.com/nizpew/appusage-mentalhealth_data-analisys-with-ML/blob/main/user_behavior_dataset.csv


#passo a passo: dar docker compose up ,

cd /opt/ceub-bigdata/streamlit
(
docker-compose down; docker-compose build; docker-compose up -d ; docker logs -f streamlit-app 
)



