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
def selecionar():


    try:
        db = connect(**config)
        if db.is_connected():
            db_info = db.server_info
            print('Connected to MySQL server version -', db_info)
            
            with db.cursor() as cursor:
                query = 'select * from Maquina_Monitoramento where FkMaquina = 1 and Fkescola = 1;'
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
| 1. Consultar por ID da maquina                |\n\
| 2. Consultar por nome cadastrado              |\n\
|===============================================|")
    resposta_menu1 = input("| Insira sua resposta: ")
    
