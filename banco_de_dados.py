import mysql.connector



def abre_conexao_mysql(usuario, senha, host_, banco_dados):
    """
    Função que abre conexão com um servidor MySQL e retorna
    um objeto CONEXAO.

    Parâmetros obrigatórios:

    usuario: nome de usuário no servidor de banco de dados MySQL.
    senha: senha de usuário no servidor de banco de dados MySQL.
    host_: nome de host no servidor de banco de dados MySQL.
    banco_dados: nome do banco de dados que será manipulado.
    """
    CONEXAO = mysql.connector.connect(
        user=usuario,
        password=senha,
        host=host_,
        database=banco_dados
    )
    return CONEXAO



def fecha_conexao_mysql(CONEXAO):
    """
    Função que fecha conexão com um servidor MySQL.

    Parâmetros obrigatórios:
    CONEXAO: Constante que representa a conexão com 
    o servidor. 

    """
    CONEXAO.close()



def executa_query(CONEXAO, query, dml=True):
    """
    Função que executa uma query no MySQL e retona um objeto CURSOR 
    que pode ser usado para executar queries mais específicas.

    Parâmetros obrigatórios:

    CONEXAO: Você deve fornecer uma constante 'CONEXAO' que é um tipo de dado
    retornado pela função: mysql.connector.connect; contendo usuário, senha, 
    host, e banco de dados do servidor MySQL a qual seu programa se conectará.

    Parâmetros opcionais:

    dml: Variável booleana que é usada para identificar se estamos manipulando
    os dados existentes na tabela: INSERT; UPDATE OR DELETE; Por padrão, seu
    valor é True, o que significa que, por padrão, esta função manipulará dados
    existentes no banco.

    """
    CURSOR = CONEXAO.cursor()
    CURSOR.execute(query)
    if dml == True:
        CONEXAO.commit()
    return CURSOR
   

    
def substitui_aspas_simples_por_espaco(dado):
    """
    A função recebe determinado dado e remove todas as aspas 
    simples do mesmo. Ao final da função, um novo dado é 
    retornado com aspas simples no começo e no final da string.

    Parâmetros obrigatórios:
    dado: um valor de tipo primitivo seja: string, int ou float.

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
    e insere os dados numa tabela informada pelo usuário de um banco de dados
    MySQL.

    Parâmetros obrigatórios:

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
    referenciando a tabela do banco de dados.
    """
    query = f'INSERT INTO {tabela} VALUES ('
    for valor in dados_planilha.values():
        if valor is None:
            query += 'NULL,'
        else: 
            query += f"{substitui_aspas_simples_por_espaco(valor)},"
    query = query[:len(query) - 1] + ');'
    executa_query(CONEXAO, query)



def atualiza_dados_no_banco_de_dados(CONEXAO, dados_planilha, tabela, condicao):
    """
    Esta função recebe dados de um dicionário chamado 'dados_planilha'
    e atualiza esses novos dados numa tabela informada pelo usuário de 
    um banco de dados MySQL.

    Parâmetros obrigatórios:

    CONEXAO: Você deve fornecer uma constante 'CONEXAO' que é um tipo 
    de dado retornado pela função: mysql.connector.connect; contendo 
    usuário, senha, host, e banco de dados do servidor MySQL a qual 
    seu programa se conectará.

    dados_planilha: Um dicionário contendo todos os novos dados 
    que serão atualizados no banco de dados. Cada chave dele representa 
    um campo do banco e seu valor, uma célula do respectivo campo.

    tabela: Nome da tabela na qual serão inseridos os dados.

    condicao: Em qual(is) linha(s) serão aplicadas atualizações.
    A condição que vai a frente do WHERE. 
    
    Obs: A condicao deve ser uma chave de dados_planilha.
    A chave do dicionário que representa chave primária no banco de
    dados.

    IMPORTANTE: O dicionário 'dados_planilha' DEVE conter todos os 
    campos do banco de dados. Ou seja, cada chave dessa variável 
    deve referenciar-se exatamente a um campo da tabela informada. 
    Não pode haver um número maior ou menor de chaves referenciando 
    a tabela do banco de dados.
    """
    query = f'UPDATE {tabela} SET '
    for chave, valor in dados_planilha.items():
        if valor is None:
            query += f'{chave} = NULL,'
        else:
            query += f'{chave} = {substitui_aspas_simples_por_espaco(valor)},'
    query = query[:len(query) - 1] + f' WHERE {condicao} = {dados_planilha[condicao]};'
    executa_query(CONEXAO, query)
   


def exclui_registro_do_banco_de_dados(CONEXAO, tabela, dados_planilha, condicao):
    """
    Esta função deleta apenas um registro de um banco de dados MySQL.

    Parâmetros obrigatórios:

    CONEXAO: Você deve fornecer uma constante 'CONEXAO' que é um tipo 
    de dado retornado pela função: mysql.connector.connect; contendo 
    usuário, senha, host, e banco de dados do servidor MySQL a qual 
    seu programa se conectará.

    tabela: Nome da tabela na qual serão excluídos os dados.

    dados_planilha: Um dicionário contendo os dados que será usada 
    para referenciar O VALOR DO ATRIBUTO na claúsula WHERE.

    condicao: Condição que será usada NO NOME DO ATRIBUTO na claúsula WHERE. 

    IMPORTANTE: O dicionário 'dados_planilha' DEVE conter todos os 
    campos do banco de dados. Ou seja, cada chave dessa variável 
    deve referenciar-se exatamente a um campo da tabela informada. 
    Não pode haver um número maior ou menor de chaves referenciando 
    a tabela do banco de dados.
    """
    query = f'DELETE FROM {tabela} WHERE {condicao} = {dados_planilha[condicao]};'
    executa_query(CONEXAO, query)


def busca_registros_no_banco_de_dados(CONEXAO, tabela, campo=None, condicao=None, dados_planilha=None):
    """
    Função que retorna todos os registros de um campo de uma tabela 
    de banco de dados MySQL.

    Parâmetros obrigatórios:
    
    CONEXAO: Você deve fornecer uma constante 'CONEXAO' que é um tipo 
    de dado retornado pela função: mysql.connector.connect; contendo 
    usuário, senha, host, e banco de dados do servidor MySQL a qual 
    seu programa se conectará.


    tabela: Nome da tabela na qual serão excluídos os dados.
    

    Parâmetros opcionais:

    campo: Campo do banco de dados que será retornado. Se não passado,
    será retornado todos os campos da tabela.
    
    condicao: Você pode especificar uma linha para retornar um valor
    único. Caso não passado, será retornado todas as linhas da tabela.
    OBS: A condição deve ser uma chave de dados_planilha.
    
    dados_planilha: Um dicionário contendo os dados que será usada 
    para referenciar O VALOR DO ATRIBUTO na claúsula WHERE.
    
    OBS: Se você passar uma condicao na assinatura da função, você DEVE PASSAR
    o dicionário contendo as chaves que referenciam a tabela.
    Caso contrário, uma exceção será lançada.
    """
    if campo is None and condicao is None:
        query = f'SELECT * FROM {tabela}'

    elif campo is None:
        query = f'SELECT * FROM {tabela} WHERE {condicao} = {dados_planilha[condicao]} ;'
        if dados_planilha is None:
                raise Exception('Você passou a condição, mas' + \
                    ' não especificou o dicionário que contém o valor da condição;')
        
    elif condicao is None:
        query = f'SELECT {campo} FROM {tabela};'

    else:
        query = f'SELECT {campo} FROM {tabela}' + \
            f' WHERE {condicao} = {dados_planilha[condicao]} ;'
        if dados_planilha is None:
                raise Exception('Você passou a condição, mas' + \
                    ' não especificou o dicionário que contém o valor da condição;')
        
    CURSOR = executa_query(CONEXAO, query, dml=False)
    resposta = CURSOR.fetchall()
    return (resposta if len(resposta) > 1  or len(resposta) == 0 else resposta[0])
   






CONEXAO = abre_conexao_mysql('root', '12345678', 
    'localhost', 'importacao_mysql')

dados_planilha = {
        "contrato" : 694699,								
        "nome" : '111PEDRO LUCAS PAULO SILVA111',
        "endereco" : 'MARCELINO',
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

# insere_dados_no_banco_de_dados(CONEXAO, dados_planilha, 'basededados') 
#atualiza_dados_no_banco_de_dados(CONEXAO, dados_planilha, 
#    'basededados',"contrato")
# exclui_registro_do_banco_de_dados(CONEXAO, 'basededados', 
#    dados_planilha, "contrato")
resposta = busca_registros_no_banco_de_dados(CONEXAO, 'basededados')
print(resposta)