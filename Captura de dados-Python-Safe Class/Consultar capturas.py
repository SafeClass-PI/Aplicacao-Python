import psutil
from mysql.connector import connect, Error
from dotenv import load_dotenv
import time as t
import os
load_dotenv()
config = {
        'user': os.getenv("USER_DB"),
        'password': os.getenv("PASSWORD_DB"),
        'host': os.getenv("HOST_DB"),
        'database': os.getenv("DATABASE_DB")
        }
def selecionar(query):


    try:
        db = connect(**config)
        if db.is_connected():            
            with db.cursor() as cursor:
                cursor.execute(query)
                resultado = cursor.fetchall() 
                
            cursor.close()
            db.close()
            return resultado
    
    except Error as e:
        print('Error to connect with MySQL -', e) 

def validarinep(inep) :
    
    try:
        db = connect(**config)
        if db.is_connected():
            
            with db.cursor() as cursor:
                query = f"SELECT * FROM safeClass.Escola WHERE Codigo_INEP = '{inep}';"
                cursor.execute(query)
                resultado = cursor.fetchall() 
                if len(resultado) == 0:
                    return False
            cursor.close()
            db.close()
            return True
    
    except Error as e:
        print('Error to connect with MySQL -', e) 
def validarcodigo(codigo_configuracao, inep):
       
    try:
        db = connect(**config)
        if db.is_connected(): 
            with db.cursor() as cursor:
                query = f"SELECT * FROM safeClass.Escola WHERE Codigo_INEP = '{inep}' and Codigo_Config = '{codigo_configuracao}';"
                cursor.execute(query)
                resultado = cursor.fetchall() 
                if len(resultado) == 0:
                    return False
            cursor.close()
            db.close()
            return resultado
    
    except Error as e:
        print('Error to connect with MySQL -', e) 

while True:
    os.system("cls")
   
    inep = input("insira o Codigo Inep: ")
    validacao1 = validarinep(inep)
    if validacao1 == False:
        print("\ncodigo INEP não reconhecido!\n")
        t.sleep(1)
        os.system("cls")
        continue
        
    else:
        senha = input("Insira o Codigo de configuração: ")
        validacao2 = validarcodigo(senha, inep)
        
    if validacao2 == False:
        print("\nCodigo de Confirmação incorreto\n")
        t.sleep(2)
        os.system("cls")
        continue
    print("Acesso realizado!")
    t.sleep(2)
    os.system("cls")
    print(f"\n|=================== M E N U ===================| \n\
| {validacao2[0][1]} \n\
|-----------------------------------------------|") 

    print("\
| 1. Consultar por Nome cadastrado              |\n\
| 2. Consultar por ID de maquina                |\n\
|===============================================|")
    resposta_menu1 = input("| Insira sua resposta: ")
    if resposta_menu1 == "1":
        maquinas_cadastradas = selecionar(f"SELECT a.Nome_indetificao FROM Escola join Maquina as a on Escola.IdEscola = a. FkEscola WHERE Codigo_INEP = '{inep}' and Codigo_Config = '{senha}';")
        if len(maquinas_cadastradas) == 0:
            print("\n\nNenhuma maquina cadastrada nessa escola!")
            t.sleep(2)
            continue
        else:
            print("\n Maquinas Cadastrada(s):")
            for i, Maquina in enumerate(maquinas_cadastradas, start=1):
                print(i,"º ", Maquina[0])
            resp_maquina = input(f"Insira o nome da maquina que você quer consultar:")
            print(f"\n\
| Maquina = {resp_maquina}             \n\
|============Exibir-dados============|\n\
| 1. Todos dados                     |\n\
| 2. Somente uso de RAM              |\n\
| 3. Somente Porcentagem de CPU      |\n\
| 4. Somente Espaço livre disco      |\n\
|====================================|\n")
            resp_dados = input("Insira quais dados você quer listar:")
            if resp_dados == "1":
                Dados = selecionar(f'select c.Metrica,e.Medida,c.Unidade_medida,\
                                    e.Data_captura from Escola as a\
 join Leitura as e  on a.IdEscola = e.Fkescola \
	join Maquina as b on b.idMaquina = e.Fkmaquina\
		join Componentes_a_monitorar as c on c.idComponente = e.FkComponente\
			where b.Nome_indetificao = "{resp_maquina}" order by e.Data_captura desc;')
                if len(Dados) == 0:
                    print("Sem dados para esse id")
                    t.sleep(2)
                    print("Reiniciando sistema")
                    os.system("cls")
                else:
                    os.system("cls")
                    print (f"\n\n| DADOS DA MAQUINA = {resp_maquina}\n")
                    t.sleep(2)
                    i = 0
                    while i < len(Dados):
                        print(f" \
    | {Dados[i][0]}: {Dados[i][1]}{Dados[i][2]} Data: {Dados[i][3]} \n ")
                        i += 1
                    fechar = input("Fechar Programa? (s/n)")
                    if fechar == "s":
                        print("\nBye")
                        t.sleep(2)
                        break
                    elif fechar == "n":
                        print("reiniciando programa")
                        continue
                    else:
                        print("Comando não reconhecido, reiniciando programa!")
                        continue
            elif resp_dados == "2":
                Dados = selecionar(f'select c.Metrica as \
"componente",e.Medida,c.Unidade_medida as "UM", e.Data_captura from Escola as a\
 join Leitura as e  on a.IdEscola = e.Fkescola \
	join Maquina as b on b.idMaquina = e.Fkmaquina\
		join Componentes_a_monitorar as c on c.idComponente = e.FkComponente\
			where b.Nome_indetificao = "{resp_maquina}" and c.Metrica = "Uso da Memória RAM" order by e.Data_captura desc ;')
                if len(Dados) == 0:
                    print("Sem dados para esse id")
                    t.sleep(2)
                    print("Reiniciando Sistema.")
                    t.sleep(2)
                    os.system("cls")
                else:
                    os.system("cls")
                    print (f"\n\n| DADOS DA MAQUINA = {resp_maquina}\n")
                    t.sleep(2)
                    i = 0
                    while i < len(Dados):
                        print(f" \
    | {Dados[i][0]}: {Dados[i][1]}{Dados[i][2]} |   Data: {Dados[i][3]} \n ")
                        i += 1       
                    fechar = input("Fechar Programa? (s/n)")
                    if fechar == "s":
                        print("\nBye")
                        t.sleep(2)
                        break
                    elif fechar == "n":
                        print("reiniciando programa")
                        continue
                    else:
                        print("Comando não reconhecido, reiniciando programa!")
                        continue
            elif resp_dados == "3":
                Dados = selecionar(f'select c.Metrica as \
"componente",e.Medida,c.Unidade_medida as "UM", e.Data_captura from Escola as a\
 join Leitura as e  on a.IdEscola = e.Fkescola \
	join Maquina as b on b.idMaquina = e.Fkmaquina\
		join Componentes_a_monitorar as c on c.idComponente = e.FkComponente\
			where b.Nome_indetificao = "{resp_maquina}" and c.Metrica = "Porcentagem de uso da CPU" order by e.Data_captura desc;')
                if len(Dados) == 0:
                    print("Sem dados para esse id")
                    t.sleep(2)
                    print("Reiniciando Sistema.")
                    t.sleep(2)
                    os.system("cls")
                else:
                    os.system("cls")
                    print (f"\n\n| DADOS DA MAQUINA COM ID = {resp_maquina}\n")
                    t.sleep(2)
                    i = 0
                    while i < len(Dados):
                        print(f" \
    | {Dados[i][0]}: {Dados[i][1]}{Dados[i][2]} Data: {Dados[i][3]} \n ")
                        i += 1
                    fechar = input("Fechar Programa? (s/n)")
                    if fechar == "s":
                        print("\nBye")
                        t.sleep(2)
                        break
                    elif fechar == "n":
                        print("reiniciando programa")
                        continue
                    else:
                        print("Comando não reconhecido, reiniciando programa!")
                        continue
            elif resp_dados == "4":
                Dados = selecionar(f'select c.Metrica as \
"componente",e.Medida,c.Unidade_medida as "UM", e.Data_captura from Escola as a\
join Leitura as e  on a.IdEscola = e.Fkescola \
	join Maquina as b on b.idMaquina = e.Fkmaquina\
		join Componentes_a_monitorar as c on c.idComponente = e.FkComponente\
			where b.Nome_indetificao = "{resp_maquina}" and c.Metrica = "Espaço do Disco" order by e.Data_captura desc;')
                if len(Dados) == 0:
                    print("Sem dados para esse id")
                    t.sleep(2)
                    print("Reiniciando Sistema.")
                    t.sleep(2)
                    os.system("cls")
                else:
                    os.system("cls")
                    print (f"\n\n| DADOS DA MAQUINA COM ID = {resp_maquina}\n")
                    t.sleep(2)
                    i = 0
                    while i < len(Dados):
                        print(f" \
    | {Dados[i][0]}: {Dados[i][1]}{Dados[i][2]} Data: {Dados[i][3]} \n ")
                        i += 1
                    fechar = input("Fechar Programa? (s/n)")
                    if fechar == "s":
                        print("\nBye")
                        t.sleep(2)
                        break
                    elif fechar == "n":
                        print("reiniciando programa")
                        continue
                    else:
                        print("Comando não reconhecido, reiniciando programa!")
                        continue

    elif resposta_menu1 == "2":       
        maquinas_cadastradas = selecionar(f"SELECT a.IdMaquina FROM Escola join Maquina as a on Escola.IdEscola = a. FkEscola WHERE Codigo_INEP = '{inep}' and Codigo_Config = '{senha}';")
        if len(maquinas_cadastradas) == 0:
            print("Nenhuma maquina cadastrada nessa escola!")
            t.sleep(2)
            continue
        else:
            print("\n ID das maquinas Cadastrada(s):")
            for i, Maquina in enumerate(maquinas_cadastradas, start=1):
                print(Maquina[0])
            resp_maquina = input("Insira o ID da maquina que você quer consultar:")
            print(f"\n\
| ID Selecionado = {resp_maquina}             \n\
|============Exibir-dados============|\n\
| 1. Todos dados                     |\n\
| 2. Somente uso de RAM              |\n\
| 3. Somente Porcentagem de CPU      |\n\
| 4. Somente Espaço livre disco      |\n\
|====================================|\n")
            resp_dados = input("Insira quais dados você quer listar:")
            if resp_dados == "1":
                Dados = selecionar(f'select c.Metrica,e.Medida,c.Unidade_medida,\
                                    e.Data_captura from Escola as a\
 join Leitura as e  on a.IdEscola = e.Fkescola \
	join Maquina as b on b.idMaquina = e.Fkmaquina\
		join Componentes_a_monitorar as c on c.idComponente = e.FkComponente\
			where b.IdMaquina = "{resp_maquina}" order by e.Data_captura desc;')
                if len(Dados) == 0:
                    print("Sem dados para esse id")
                    t.sleep(2)
                    os.system("cls")
                else:
                    os.system("cls")
                    print (f"\n\n| DADOS DA MAQUINA COM ID = {resp_maquina}\n")
                    t.sleep(2)
                    i = 0
                    while i < len(Dados):
                        print(f" \
    | {Dados[i][0]}: {Dados[i][1]}{Dados[i][2]} Data: {Dados[i][3]} \n ")
                        i += 1
                    fechar = input("Fechar Programa? (s/n)")
                    if fechar == "s":
                        print("\nBye")
                        t.sleep(2)
                        break
                    elif fechar == "n":
                        print("reiniciando programa")
                        continue
                    else:
                        print("Comando não reconhecido, reiniciando programa!")
                        continue
            elif resp_dados == "2":
                Dados = selecionar(f'select c.Metrica as \
"componente",e.Medida,c.Unidade_medida as "UM", e.Data_captura from Escola as a\
 join Leitura as e  on a.IdEscola = e.Fkescola \
	join Maquina as b on b.idMaquina = e.Fkmaquina\
		join Componentes_a_monitorar as c on c.idComponente = e.FkComponente\
			where b.IdMaquina = "{resp_maquina}" and c.Metrica = "Uso da Memória RAM" order by e.Data_captura desc ;')
                if len(Dados) == 0:
                    print("Sem dados para esse id")
                    t.sleep(2)
                    print("Reiniciando Sistema.")
                    t.sleep(2)
                    os.system("cls")
                else:
                    os.system("cls")
                    print (f"\n\n| DADOS DA MAQUINA COM ID = {resp_maquina}\n")
                    t.sleep(2)
                    i = 0
                    while i < len(Dados):
                        print(f" \
    | {Dados[i][0]}: {Dados[i][1]}{Dados[i][2]} |   Data: {Dados[i][3]} \n ")
                        i += 1
                    fechar = input("Fechar Programa? (s/n)")
                    if fechar == "s":
                        print("\nBye")
                        t.sleep(2)
                        break
                    elif fechar == "n":
                        print("reiniciando programa")
                        continue
                    else:
                        print("Comando não reconhecido, reiniciando programa!")
                        continue
            elif resp_dados == "3":
                Dados = selecionar(f'select c.Metrica as \
"componente",e.Medida,c.Unidade_medida as "UM", e.Data_captura from Escola as a\
 join Leitura as e  on a.IdEscola = e.Fkescola \
	join Maquina as b on b.idMaquina = e.Fkmaquina\
		join Componentes_a_monitorar as c on c.idComponente = e.FkComponente\
			where b.IdMaquina = "{resp_maquina}" and c.Metrica = "Porcentagem de uso da CPU" order by e.Data_captura desc;')
                if len(Dados) == 0:
                    print("Sem dados para esse id")
                    t.sleep(2)
                    print("Reiniciando Sistema.")
                    t.sleep(2)
                    os.system("cls")
                else:
                    os.system("cls")
                    print (f"\n\n| DADOS DA MAQUINA COM ID = {resp_maquina}\n")
                    t.sleep(2)
                    i = 0
                    while i < len(Dados):
                        print(f" \
    | {Dados[i][0]}: {Dados[i][1]}{Dados[i][2]} Data: {Dados[i][3]} \n ")
                        i += 1
                    fechar = input("Fechar Programa? (s/n)")
                    if fechar == "s":
                        print("\nBye")
                        t.sleep(2)
                        break
                    elif fechar == "n":
                        print("reiniciando programa")
                        continue
                    else:
                        print("Comando não reconhecido, reiniciando programa!")
                        continue
            elif resp_dados == "4":
                Dados = selecionar(f'select c.Metrica as \
"componente",e.Medida,c.Unidade_medida as "UM", e.Data_captura from Escola as a\
 join Leitura as e  on a.IdEscola = e.Fkescola \
	join Maquina as b on b.idMaquina = e.Fkmaquina\
		join Componentes_a_monitorar as c on c.idComponente = e.FkComponente\
			where b.IdMaquina = "{resp_maquina}" and c.Metrica = "Espaço do Disco" order by e.Data_captura desc;')
                if len(Dados) == 0:
                    print("Sem dados para esse id")
                    t.sleep(2)
                    print("Reiniciando Sistema.")
                    t.sleep(2)
                    os.system("cls")
                else:
                    os.system("cls")
                    print (f"\n\n| DADOS DA MAQUINA COM ID = {resp_maquina}\n")
                    t.sleep(2)
                    i = 0
                    while i < len(Dados):
                        print(f" \
    | {Dados[i][0]}: {Dados[i][1]}{Dados[i][2]} Data: {Dados[i][3]} \n ")
                        i += 1
                    fechar = input("Fechar Programa? (s/n)")
                    if fechar == "s":
                        print("\nBye")
                        t.sleep(2)
                        break
                    elif fechar == "n":
                        print("reiniciando programa")
                        continue
                    else:
                        print("Comando não reconhecido, reiniciando programa!")
                        continue
    else:
        print("Comando Invalido")
        t.sleep(1)
        print("Reiniciando...")

