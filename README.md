

#baixar zip do github

* baixar essa pasta streamlit e substituir ela pela já existente no ambiente do professor

* 
cd /opt/ceub-bigdata/streamlit
docker container prune

baixar csvs no drive 
https://drive.google.com/drive/folders/1nNo-Jf3Qw0RrtpfJAD9TKpeboQSoUhJx



------------------------------------
FAZER O CODIGO E A MAQUINA RODAR

nós utilizamos o docker do professor do ceub-bigdata so que para que ela rode do jeito certo é necessario alguns passos

1. Substituir a pasta de Streamlit pela pasta de streamlit no drive
https://drive.google.com/drive/folders/1nNo-Jf3Qw0RrtpfJAD9TKpeboQSoUhJx

* baixar essa pasta e substituir ela pela já existente no ambiente do professor

2. conferir se o caminho das portas obedece o seguinte

minio 9001 9001
streamlit 8501 8501
se não o código não irá funcionar

3. realizar os comandos caso necessario

#é necessario entrar na pasta do streamlit primeiro para realizar os proximos comandos
cd /opt/ceub-bigdata/streamlit

#depois disso tudo realizar o build e o up com esse comando que age como um reset
docker-compose down; docker-compose build; docker-compose up -d ; docker logs -f streamlit-app 

OCASIONAL----------------------------------------
#quando dar erro de docker minio sendo usado: 
docker container prune

#depois disso rodar o comando de reset de novo
docker-compose down; docker-compose build; docker-compose up -d ; docker logs -f streamlit-app
OCASIONAL----------------------------------------

database pra ser usada
https://www.kaggle.com/datasets/kmader/skin-cancer-mnist-ham10000
#dicionario de dados desse: 
https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/DBW86T

4. adicionar arquivos no minio
local host do minio:
http://localhost:9001/

depois de deixar o minio na web funcional, adicionar neles os arquivos

* crie um bucket chamado "datasets" no minio
* adicione os datasets no drive que ficam na pasta chamada "dados HAM10000 csvcsv"

5. rodar o streamlit
agora é só abrir na web o local host do streamlit:
http://localhost:8501/
