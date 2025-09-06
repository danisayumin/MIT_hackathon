# python-app/analise_sih.py

import pandas as pd
from pysus import SIH
from datasus import read_dbc # <-- MUDANÇA FINAL: Usando a biblioteca 'read-dbc'

# --- Documentação do Script ---
# Objetivo: Analisar dados de internações (SIH) de São Paulo em 2024
# para identificar casos de Obesidade (CID-10 E66).
# Abordagem:
# - Download: pysus.SIH
# - Leitura do arquivo .DBC: biblioteca 'read-dbc'
# -----------------------------

def analisar_internacoes_obesidade(estado, ano, mes):
    """
    Baixa e processa os dados do SIH para um estado, ano e mês específicos,
    filtrando por internações cujo diagnóstico principal é Obesidade (E66).
    """
    print(f"--- Iniciando análise para {estado}/{ano}, Mês: {mes} ---")

    try:
        # 1. BAIXAR OS DADOS (usando pysus)
        print("Passo 1/3: Baixando arquivo de dados...")
        sih = SIH().load()
        sih_files = sih.get_files(group="RD", uf=estado, year=ano, month=[mes])
        if not sih_files:
            print("Nenhum arquivo encontrado para o período especificado.")
            return None
        sih.describe(sih_files[0])
        dbc_filepath = sih.download(sih_files)
        print(dbc_filepath)
        
        if not dbc_filepath:
            print("Download falhou. Verifique se os dados para este período existem.")
            return None
        
        print(f"Download completo! Arquivo salvo em: {dbc_filepath}")

        # 2. LER O ARQUIVO .DBC (usando read-dbc)
        # Esta é a abordagem mais direta, com uma biblioteca especialista em ler .DBC
        print("Passo 2/3: Lendo e convertendo o arquivo para DataFrame...")
        df = pd.DataFrame(read_dbc(dbc_filepath))
        print("Leitura concluída. Total de registros no mês:", len(df))
        
        # 3. FILTRAR OS DADOS E APRESENTAR
        cid_obesidade = 'E66'
        print(f"Passo 3/3: Filtrando internações por CID principal = '{cid_obesidade}' (Obesidade)...")
        casos_obesidade = df[df['DIAG_PRINC'].str.startswith(cid_obesidade, na=False)]

        total_casos = len(casos_obesidade)
        print("\n--- RESULTADO DA ANÁLISE ---")
        print(f"Número total de internações por obesidade em {estado} no mês {mes}/{ano}: {total_casos}")

        if total_casos > 0:
            print("\nAmostra dos dados encontrados (algumas colunas relevantes):")
            colunas_relevantes = ['MUNIC_RES', 'IDADE', 'SEXO', 'DIAG_PRINC', 'VAL_TOT']
            colunas_existentes = [col for col in colunas_relevantes if col in df.columns]
            print(casos_obesidade[colunas_existentes].head())
        
        print("--- Análise Concluída ---")
        return casos_obesidade

    except Exception as e:
        print(f"Ocorreu um erro durante a análise: {e}")
        return None

# --- Execução Principal ---
if __name__ == "__main__":
    estado_alvo = 'SP'
    ano_alvo = 2024
    mes_alvo = 1

    analisar_internacoes_obesidade(estado_alvo, ano_alvo, mes_alvo)