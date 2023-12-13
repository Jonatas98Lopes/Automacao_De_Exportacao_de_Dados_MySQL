from inicializar import GoogleChrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from time import sleep
from random import randint
import openpyxl
import mysql.connector
from datetime import datetime
import pdb

def pausar():
  """
  Para o funcionamento do programa num intervalo de 5 a 10 segundos.
  Não aceita argumentos.
  """
  sleep(randint(5,10))


def repousar():
  """
  Para o funcionamento do programa num intervalo de 20 a 25 segundos.
  """
  sleep(randint(20, 25))

def remove_aspas_no_meio_da_string(dado):
      novo_dado = ""
      contador = 0
      for caractere in dado:
          if caractere == "'": 
              novo_dado += ' '
          else:
              novo_dado += caractere
      return f"'{novo_dado.strip()}'"    

            

def converte_string_em_data(string):
    substrings = string.split('-')
    dia_hora = substrings.pop(2)
    substrings.append(dia_hora[:2])
    hora = dia_hora.split()[1]
    hora = hora.split(':')
    for dado in hora: substrings.append(dado)
    
    return datetime(*[int(dado) for dado in substrings])



# 1. ACESSO AO GOOGLE DRIVE E DOWNLOAD DA PLANILHA:

""" LINK_GOOGLE_DRIVE = 'https://drive.google.com/drive/folders/1nJn1jdS69k78qC6HckwkkQAkFDUvDbxv'

browser = GoogleChrome()
driver, wait = browser.get_driver(), browser.get_wait()
pausar()

driver.get(LINK_GOOGLE_DRIVE)
repousar()

planilha = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//div[@data-tooltip="Excel: Base de dados .xlsx"]')))
planilha.click()
pausar()

botoes_selecao = driver.find_elements(By.XPATH, '//div[@aria-label="Fazer download"]')
botoes_selecao[2].click()
repousar()
driver.quit() """


CONEXAO = mysql.connector.connect(
  user='root',
  password='12345678',
  host='localhost',
  database='Importacao_MySQL'
) 

CURSOR = CONEXAO.cursor()
# 2. EXTRAINDO DADOS DA PLANILHA:

workbook = openpyxl.load_workbook('Base de dados .xlsx')
sheet_data = workbook['data']
linha = 2



contratos = []
registros_atualizados = {}


# ATUALIZAÇÃO DE DADOS ALTERADOS:
while linha <= sheet_data.max_row:
    
    dados_planilha = {
        "contrato" : sheet_data[f'A{linha}'].value,
        "nome" : sheet_data[f'B{linha}'].value,
        "endereco" : sheet_data[f'C{linha}'].value,
        "numero" : sheet_data[f'D{linha}'].value,
        "complemento" : sheet_data[f'E{linha}'].value,
        "bairro" : sheet_data[f'F{linha}'].value,
        "cidade" : sheet_data[f'G{linha}'].value,
        "regional" : sheet_data[f'H{linha}'].value,
        "tipo_do_contrato" : sheet_data[f'I{linha}'].value,
        "plano" : sheet_data[f'J{linha}'].value,
        "adicionais" : sheet_data[f'K{linha}'].value,
        "voz" : sheet_data[f'L{linha}'].value,
        "valor_voz" : sheet_data[f'M{linha}'].value,
        "valor_do_plano" : sheet_data[f'N{linha}'].value,
        "valor_adicionais" : sheet_data[f'O{linha}'].value,
        "valor_liquido_do_contrato" : sheet_data[f'P{linha}'].value,
        "status" : sheet_data[f'Q{linha}'].value,
        "data_conexao" : sheet_data[f'R{linha}'].value,
        "vendedor" : sheet_data[f'S{linha}'].value,
        "canal_de_vendas" : sheet_data[f'T{linha}'].value,
        "codigo_os" : sheet_data[f'U{linha}'].value,
        "area_de_despacho" : sheet_data[f'V{linha}'].value,
        "equipe" : sheet_data[f'W{linha}'].value,
        "operadora" : sheet_data[f'X{linha}'].value

    }
    
    # SE ALGUM CONTRATO NÃO ESTIVER NA COLUNA DE BANCO DE DADOS:
    query = "SELECT contrato FROM basededados"
    CURSOR.execute(query)
    resultados = CURSOR.fetchall()
    if any(int(dados_planilha["contrato"]) 
           in tupla for tupla in resultados) and dados_planilha["contrato"] is not None:
        # EM CASO, DE MUDANÇA, VAMOS EXIBIR O REGISTRO ANTERIOR
        query = "SELECT * FROM basededados WHERE contrato = '{}';".format(dados_planilha["contrato"])
        CURSOR.execute(query)
        registro_anterior = CURSOR.fetchall() 
        # VAMOS VERIFICAR SE ALGUM CAMPO DAQUELA LINHA FOI ALTERADO
        for chave, valor in dados_planilha.items(): 
            if chave == "contrato": continue
            query = "SELECT {} FROM basededados WHERE contrato = '{}'"\
                .format(chave, dados_planilha["contrato"])
            CURSOR.execute(query)
            resposta = CURSOR.fetchall()
            resposta = resposta[0] if len(resposta) >= 1 else resposta
            if chave == 'data_conexao': valor = converte_string_em_data(valor)
            if valor != resposta[0]:
                valor = dados_planilha[chave]
                query = "UPDATE basededados SET {} = {} WHERE contrato = '{}'"\
                    .format(chave, 
                        f"'{valor}'" if valor is not None else 'NULL', dados_planilha["contrato"])
                CURSOR.execute(query)
                CONEXAO.commit()
        query = "SELECT * FROM basededados WHERE contrato = '{}'"\
            .format(dados_planilha["contrato"])
        CURSOR.execute(query)
        registro_atual = CURSOR.fetchall()
        registro_atual = registro_atual[0] if len(registro_atual) else registro_atual
        if registro_anterior != registro_atual:
            query = "SELECT * FROM basededados WHERE contrato = '{}'".format(dados_planilha["contrato"])
            CURSOR.execute(query)
            resposta = CURSOR.fetchall()
            resposta = resposta[0] if len(resposta) >= 1 else resposta
            registros_atualizados[resposta] = registro_anterior
    elif dados_planilha["contrato"] is None:
        break
    else:
        # REGISTROS NOVOS, VAMOS GUARDÁ-LOS PARA VERIFICAR E DELETAR REGISTROS EXCLUÍDOS
        query = "INSERT INTO basededados VALUES("
        for valor in dados_planilha.values():
            if valor is None:
                query += "NULL, "
            else:
                query += remove_aspas_no_meio_da_string(valor) + ','
        new_query = query[:len(query) - 1] + ');'
        print(new_query)
        CURSOR.execute(new_query)
        CONEXAO.commit()
    contratos.append(dados_planilha["contrato"])
    linha += 1


# REGISTROS EXCLUIDOS
registros_excluidos = []
query = "SELECT contrato FROM basededados"
CURSOR.execute(query)
resultados = CURSOR.fetchall()
resultados = resultados[0] if len(resultados) >= 1 else resultados
for contrato in resultados:
    if contrato not in contratos:
        query = 'SELECT * FROM basededados WHERE contrato = {}'\
            .format(contrato)
        CURSOR.execute(query)
        resposta = CURSOR.fetchall()[0]
        registros_excluidos.append(resposta)

        query = 'DELETE FROM basededados WHERE contrato = {}'\
            .format(contrato)
        CURSOR.execute(query)
        CONEXAO.commit()               

print('Registros atualizados: ' + 20 * '=')
for chave, valor in registros_atualizados.items():
    print(f"Registro anterior: {valor}\n\n")
    print(f"Registro atualizado: {chave}\n\n")
    print(50 * '-')

print('\n\nRegistros excluídos: ' + 20 * '=')
for item in registros_excluidos:
    print(f"Registro excluído: {item}\n\n")
    print(50 * "-")

