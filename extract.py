import requests
import os
import datetime
import warnings
warnings.filterwarnings('ignore')

# Obtém a data e hora atuais
data_hora_atual = datetime.datetime.now()
# Obtém o ano da data e hora atual
ano_atual = data_hora_atual.year

# Lista de URLs
urls = [
    f'https://balanca.economia.gov.br/balanca/bd/comexstat-bd/ncm/EXP_2023.csv',
    f'https://balanca.economia.gov.br/balanca/bd/tabelas/PAIS.csv'
]

# Diretório de destino
dest_dir = "./" 

print("Fazendo Download dos arquivos...")
for url in urls:
    # Obtém o nome do arquivo 
    filename = os.path.join(dest_dir, os.path.basename(url))

    # Verifica se o arquivo já existe e o exclui
    if os.path.exists(filename):
        os.remove(filename)

    # Faz o download do arquivo
    response = requests.get(url, stream=True, verify=False)
    if response.status_code == 200:
        with open(filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=128):
                file.write(chunk)
        print(f"Download do arquivo '{os.path.basename(filename)}' concluído com sucesso.")
    else:
        print(f"Falha ao baixar o arquivo '{os.path.basename(filename)}'.")
