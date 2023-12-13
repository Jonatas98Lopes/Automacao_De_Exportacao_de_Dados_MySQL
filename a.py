def remove_aspas_no_meio_da_string(dado):
      novo_dado = ""
      contador = 0
      for caractere in dado:
          if caractere == "'": 
              novo_dado += ' '
          else:
              novo_dado += caractere
      return f"'{novo_dado.strip()}'"    



            

string = "'VITO PEDRO DELL'ANTONIA'"
retorno = remove_aspas_no_meio_da_string(string)
print(retorno)