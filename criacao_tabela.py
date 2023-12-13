import mysql.connector

CONEXAO = mysql.connector.connect(
  user='root',
  password='12345678',
  host='localhost',
  database='Importacao_MySQL'
)

cursor = CONEXAO.cursor()

cursor.execute('''
  CREATE TABLE IF NOT EXISTS BaseDeDados(
      contrato INT PRIMARY KEY,
      nome VARCHAR(255) NOT NULL,
      endereco VARCHAR(255) NOT NULL,
      numero INT NOT NULL,
      complemento VARCHAR(255),
      bairro VARCHAR(255) NOT NULL,
      cidade VARCHAR(255) NOT NULL,
      regional VARCHAR(30) ,
      tipo_do_contrato VARCHAR(255) NOT NULL,
      plano VARCHAR(255) NOT NULL,
      adicionais TEXT,
      voz VARCHAR(255),
      valor_voz DECIMAL(10, 2),
      valor_do_plano DECIMAL(10, 2) NOT NULL,
      valor_adicionais DECIMAL(10, 2) NOT NULL,
      valor_liquido_do_contrato DECIMAL(10, 2) NOT NULL,
      status VARCHAR(255) NOT NULL,
      data_conexao DATETIME NOT NULL,
      vendedor VARCHAR(255) NOT NULL,
      canal_de_vendas VARCHAR(255) NOT NULL,
      codigo_os INT NOT NULL,
      area_de_despacho VARCHAR(255) NOT NULL,
      equipe TEXT,
      operadora VARCHAR(255) NOT NULL
  );
''')