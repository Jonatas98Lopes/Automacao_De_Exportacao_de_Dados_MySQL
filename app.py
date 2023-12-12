from inicializar import GoogleChrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from time import sleep
from random import randint
import openpyxl
import mysql.connector


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


# 2. EXTRAINDO DADOS DA PLANILHA:

workbook = openpyxl.load_workbook('Base de dados .xlsx')
sheet_data = workbook['data']
linha = 2


CONEXAO = mysql.connector.connect(
  user='root',
  password='12345678',
  host='localhost',
  database='Importacao_MySQL'
) 
cursor = CONEXAO.cursor()

registros_atualizados = {}
registros_excluidos = {}

# Campos da planilha:
while linha <= sheet_data.max_row:
    
    dados_planiha = {
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
    if dados_planiha["contrato"] in cursor.execute("SELECT contrato FROM basededados"):
        # EM CASO, DE MUDANÇA, VAMOS EXIBIR O REGISTRO ANTERIOR
        registro_anterior = cursor.execute("""
            SELECT * FROM basededados 
            WHERE contrato = %s""", (dados_planiha["contrato"],)) 
        # VAMOS VERIFICAR SE ALGUM CAMPO DAQUELA LINHA FOI ALTERADO
        for chave, valor in dados_planiha.items(): 
           if chave == "contrato": continue
           if valor != cursor.execute("SELECT %s FROM basedados WHERE %s", (chave, dados_planiha["contrato"])):
                cursor.execute("""
                    UPDATE basededados
                    SET %s = %s
                    WHERE contrato = %s
                """, (chave, valor, dados_planiha["contrato"]))
        if registro_anterior != cursor.execute("SELECT * FROM basededados"):
            registros_atualizados[registro_anterior] = cursor.execute("""
                    SELECT * FROM basededados
                    WHERE contrato = %s""", (dados_planiha["contrato"],))
    else:
        pass
    
    linha += 1
    
