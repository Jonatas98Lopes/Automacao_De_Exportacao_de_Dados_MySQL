from inicializar import GoogleChrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from time import sleep
from random import randint


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

LINK_GOOGLE_DRIVE = 'https://drive.google.com/drive/folders/1nJn1jdS69k78qC6HckwkkQAkFDUvDbxv'

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

