import mysql.connector
from datetime import datetime

contratos = []
def importacao_mysql(CONEXAO, dados_planilha, tabela):
    CURSOR = CONEXAO.cursor()
    
    

    registros_atualizados = {}
    contratos.append(dados_planilha["contrato"])
    # ATUALIZAÇÃO DE DADOS ALTERADOS:
    # SE ALGUM CONTRATO NÃO ESTIVER NA COLUNA DE BANCO DE DADOS:
    query = "SELECT contrato FROM {}".format(tabela)
    CURSOR.execute(query)
    resultados = CURSOR.fetchall()
    resultados = resultados[0] if len(resultados) >= 1 else resultados
    if dados_planilha["contrato"] in resultados:
        # EM CASO, DE MUDANÇA, VAMOS EXIBIR O REGISTRO ANTERIOR
        query = "SELECT * FROM {} WHERE contrato = '{}';".format(tabela, dados_planilha["contrato"])
        CURSOR.execute(query)
        registro_anterior = CURSOR.fetchall()
        print(type(registro_anterior))
        # VAMOS VERIFICAR SE ALGUM CAMPO DAQUELA LINHA FOI ALTERADO
        for chave, valor in dados_planilha.items(): 
            if chave == "contrato": continue
            query = "SELECT {} FROM {} WHERE contrato = '{}'"\
                .format(chave, tabela, dados_planilha["contrato"])
            CURSOR.execute(query)
            resposta = CURSOR.fetchall()
            resposta = resposta[0] if len(resposta) >= 1 else resposta
            if chave == 'data_conexao': valor = converte_string_em_data(valor)
            if valor != resposta[0]:
                valor = dados_planilha[chave]
                query = "UPDATE {} SET {} = {} WHERE contrato = '{}'"\
                    .format(tabela, chave, 
                        f"'{valor}'" if valor is not None else 'NULL', dados_planilha["contrato"])
                CURSOR.execute(query)
                CONEXAO.commit()
        query = "SELECT * FROM {} WHERE contrato = '{}'"\
            .format(tabela, dados_planilha["contrato"])
        CURSOR.execute(query)
        registro_atual = CURSOR.fetchall()
        registro_atual = registro_atual[0] if len(registro_atual) else registro_atual
        if registro_anterior != registro_atual:
            query = "SELECT * FROM {} WHERE contrato = '{}'".format(tabela, dados_planilha["contrato"])
            CURSOR.execute(query)
            resposta = CURSOR.fetchall()
            resposta = resposta[0] if len(resposta) >= 1 else resposta
            print(type(resposta))
            registros_atualizados[resposta] = registro_anterior
            
    else:
        # REGISTROS NOVOS, VAMOS GUARDÁ-LOS PARA VERIFICAR E DELETAR REGISTROS EXCLUÍDOS
        query = f"INSERT INTO {tabela} VALUES("
        for valor in dados_planilha.values():
            if valor is None:
                query += "NULL, "
            else:
                query += f"'{valor}', "
        new_query = query[:len(query) - 2] + ');'
        print(new_query)
        CURSOR.execute(new_query)
        CONEXAO.commit()
              
      


    # REGISTROS EXCLUIDOS
    registros_excluidos = []
    query = "SELECT contrato FROM {}".format(tabela)
    CURSOR.execute(query)
    resultados = CURSOR.fetchall()
    resultados = resultados[0] if len(resultados) >= 1 else resultados
    for contrato in resultados:
        if contrato not in contratos:
            query = 'SELECT * FROM {} WHERE contrato = {}'.format(tabela, contrato)
            CURSOR.execute(query)
            registros_excluidos.append(CURSOR.fetchall())

            query = 'DELETE FROM {} WHERE contrato = {}'.format(tabela, contrato)
            CURSOR.execute(query)
            CONEXAO.commit()        

    print('Registros atualizados: ' + 50 * '=')
    for chave, valor in registros_atualizados.items():
        print(f"Registro anterior: {valor}\n\n")
        print(f"Registro atualizado: {chave}\n\n")
        print(50 * '-')

    print('\n\nRegistros excluídos: ' + 50 * '=')
    for item in registros_excluidos:
        query = ''
        print(f"Registro excluído: {item}\n\n")
        print(50 * "-")



CONEXAO = mysql.connector.connect(
		user='root',
		password='12345678',
		host='localhost',
		database='teste_mysql'
) 
	

dados_planilha = {
    "contrato" : 6946234,
    "nome" : 'NOVO_REGISTRO',
    "endereco" : 'JULIA NECCHI PIANA',
    "numero" : 380,
    "complemento" : None,
    "bairro" : 'GERALDO CORREIA DE CARVALHO',
    "cidade" : 'RIO DE JANEIRO',
    "regional" : None,
    "tipo_do_contrato" : 'COMERCIAL',
    "plano" : 'NAVE NOVA',
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
    "codigo_os" : '5431791',
    "area_de_despacho" : 'RIBEIRAO PRETO',
    "equipe" : 'SLN - ROMERO DOS SANTOS MARQUES',
    "operadora" : 'NIU FIBRA' }


def converte_string_em_data(string):
    substrings = string.split('-')
    dia_hora = substrings.pop(2)
    substrings.append(dia_hora[:2])
    hora = dia_hora.split()[1]
    hora = hora.split(':')
    for dado in hora: substrings.append(dado)
    
    return datetime(*[int(dado) for dado in substrings])



resposta = importacao_mysql(CONEXAO, dados_planilha, 'testebasededados')
