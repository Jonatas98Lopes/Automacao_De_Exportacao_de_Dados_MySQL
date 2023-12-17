import mysql.connector



def enviar_dados_ao_banco_de_dados(CONEXAO, query):
    """
    Função que abre conexão com o banco de dados MySQL e 
    executa uma query de manipulação de dados:
    Ex: INSERT; UPDATE; DELETE...

    Parâmetros:

    CONEXAO: Você deve fornecer uma constante 'CONEXAO' que é um tipo de dado
    retornado pela função: mysql.connector.connect; contendo usuário, senha, 
    host, e banco de dados do servidor MySQL a qual seu programa se conectará.

    """
    CURSOR = CONEXAO.cursor()
    CURSOR.execute(query)
    CONEXAO.commit()
   

    
def substitui_aspas_simples_por_espaco(dado):
    """
    A função recebe determinado dado e remove todas as aspas 
    simples do mesmo. Ao final da função, um novo dado é 
    retornado com aspas simples no começo e no final da string.

    A função se faz necessária, pois dados em planilhas podem vir 
    com aspas simples no meio de dados numa célula. Ex: Pera D'Água. 
    O problema destas aspas simples aparece quando tentando inserir 
    novos dados ou atualizar dados já existentes. 
    
    Observe as síntaxes abaixo:
    INSERT INTO Tabela VALUES(09324, 'Pera D'Água');
    UPDATE Tabela SET Fruta = 'Pera D'Fogo' WHERE = 09324 ;
    # Ambas as síntaxes gerarão uma execeção de erro síntaxe no MySQL.
    """
    dado = str(dado)
    novo_dado = ""
    for caractere in dado:
        if caractere == "'": 
            novo_dado += ' '
        else:
            novo_dado += caractere
    return f"'{novo_dado.strip()}'"   




def insere_dados_no_banco_de_dados(CONEXAO, dados_planilha, tabela):
    """
    Esta função recebe dados de um dicionário chamado 'dados_planilha'
    e insere os dados num tabela informada pelo usuário de um banco de dados
    MySQL.

    Parâmetros:

    CONEXAO: Você deve fornecer uma constante 'CONEXAO' que é um tipo de dado
    retornado pela função: mysql.connector.connect; contendo usuário, senha, 
    host, e banco de dados do servidor MySQL a qual seu programa se conectará.

    dados_planilha: Um dicionário contendo os dados todos os dados que serão inseridos
    no banco de dados. Cada chave dele representa um campo do banco e seu valor, 
    uma célula do respectivo campo.

    tabela: Nome da tabela na qual serão inseridos os dados.

    IMPORTANTE: O dicionário 'dados_planilha' DEVE conter todos os campos do banco 
    de dados. Ou seja, cada chave dessa variável deve referenciar-se exatamente a 
    um campo da tabela informada. Não pode haver um número maior ou menor de chaves 
    referenciando a tabela do banco dedados.
    """
    query = f'INSERT INTO {tabela} VALUES ('
    for valor in dados_planilha.values():
        if valor is None:
            query += 'NULL,'
        else: 
            query += f"{substitui_aspas_simples_por_espaco(valor)},"
    query = query[:len(query) - 1] + ');'
    enviar_dados_ao_banco_de_dados(CONEXAO, query)
""" 
CONEXAO = mysql.connector.connect(
  user='root',
  password='12345678',
  host='localhost',
  database='Importacao_MySQL'
) 

dados_planilha = {
        "contrato" : 694699,								
        "nome" : '111PEDRO LUCAS PAULO SILVA111',
        "endereco" : 'JULIA NECCHI PIANA',
        "numero" : 380,
        "complemento" : None,
        "bairro" : 'GERALDO CORREIA DE CARVALHO',
        "cidade" : 'RIBEIRAO PRETO',
        "regional" : None,
        "tipo_do_contrato" : 'RESIDENCIAL',
        "plano" : 'BF23 NIU FIBRA 800MB',
        "adicionais" : 'MAQUINA DE CONTOS - APP BEBANCA - APP E-SAUDE ASSIST - APP FIT ANYWHERE',
        "voz" : None,
        "valor_voz" : None,
        "valor_do_plano" : 59,
        "valor_adicionais" : 35.99,
        "valor_liquido_do_contrato" : 94.99,
        "status" : 'Habilitado',
        "data_conexao" : '2023-12-09 00:00:00',
        "vendedor" : 'MATHEUS HENRIQUE DOS SANTOS ALMEIDA',
        "canal_de_vendas" : 'MCD SANTOS',
        "codigo_os" : 5431791,
        "area_de_despacho" : 'RIBEIRAO PRETO',
        "equipe" : 'SLN - ROMERO DOS SANTOS MARQUES',
        "operadora" : 'NIU FIBRA'

    }

insere_dados_no_banco_de_dados(CONEXAO, dados_planilha, 'basededados')  """

