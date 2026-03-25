# teste para consumo de API do site brasilapi

import requests
import pandas as pd
import time
from datetime import datetime
import re

# leitura da API BrasilAPI
# retries: número de tentativas que a função executa
# delay = tempo em segundos de delay
def scrap_brasil_api(cnpj, retries=3, delay=1):
    url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj}"
    for i in range(retries):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return response.json()
        except requests.RequestException:
            pass
        time.sleep(delay)
    return None

# leitura da CNPJws
# retries: número de tentativas que a função executa
# delay = tempo em segundos de delay
def scrap_cnpj_ws(cnpj, retries=3, delay=1):
    url = f"https://publica.cnpj.ws/cnpj/{cnpj}"
    for i in range(retries):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return response.json()
        except requests.RequestException:
            pass
        time.sleep(delay)
    return None

# função para buscar o cnpj no banco de dados da API
def scrap_cnpj(cnpj):
    main_data = scrap_brasil_api(cnpj) or {}
    secondary_data = scrap_cnpj_ws(cnpj) or {}
    
    # date_start: armazena data de abertura da empresa
    # date_register: armazena data da última atualização da empresa em relação ao cadastro
    date_start = main_data.get("data_inicio_atividade")
    date_register = main_data.get("data_situacao_cadastral")

    # muda o formatdo da data de: %Y-%m-%d -> %d/%m/%Y
    date_register_read = datetime.strptime(date_register, "%Y-%m-%d")
    date_start_read = datetime.strptime(date_start, "%Y-%m-%d")
    date_register_format = date_register_read.strftime("%d/%m/%Y")
    date_start_format = date_start_read.strftime("%d/%m/%Y")
    

    # lista de dados a serem lidos da API
    scrap = {
        "CNPJ": main_data.get("cnpj"),
        "Nome": main_data.get("razao_social"),
        "Nome Fantasia": main_data.get("nome_fantasia"),
        "Capital Social": main_data.get("capital_social") if main_data.get("capital_social") not in (0, None) else secondary_data.get("capital_social") if secondary_data else None,
        "Situação Cadastral": main_data.get("situacao_cadastral"),
        "Data Situação Cadastral": date_register_format,
        "Data de início de atividades": date_start_format,
        "Endereço": f"{main_data.get('descricao_tipo_de_logradouro')}, {main_data.get('logradouro')}, {main_data.get('numero')} {main_data.get('complemento') or ''}",
        "Bairro": main_data.get("bairro"),
        "Município": main_data.get("municipio"),
        "UF": main_data.get("uf"),
        "CEP": main_data.get("cep"),
        "Telefone 1": main_data.get("ddd_telefone_1"),
        "Telefone 2": main_data.get("ddd_telefone_2"),
        "Fax": main_data.get("ddd_fax"),
        "Email": main_data.get("email"),
        "CNAE Principal": main_data.get("cnae_fiscal"),
        "CNAE Principal descrição": main_data.get("cnae_fiscal_descricao") or "",
        "CNAE Secundário": [item.get("codigo") for item in main_data.get("cnaes_secundarios", [])]
        }
    return scrap

# insira abaixo os cnpjs desejados para scrap
cnpj = [
    "11.398.351/0001-19",
    "28.350.338/0001-92",
    "28.350.338/0010-83",
    "28.350.338/0030-27"
]

searchs = []

for pj in cnpj:
    # retira todos os hifens, pontos e barras do cnpj (caso houver)
    cnpj_format = re.sub(r'\D', '', pj)
    # variavel para executar função scrap_cnpj
    search = scrap_cnpj(cnpj_format)
    # ler apenas "codigo" em CNAE Secundario e juntar todos em apenas uma celula
    search["CNAE Secundário"] = ", ".join(str(c) for c in search.get("CNAE Secundário", []))
    searchs.append(search)

# salvar em arquivo Excel
df = pd.DataFrame(searchs)
df.to_excel("cnpj_info.xlsx", index=False)
print("Arquivo Excel gerado com sucesso!")