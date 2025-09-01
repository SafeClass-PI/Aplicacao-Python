import psutil as p
import subprocess as sub
from mysql.connector import connect, Error
from dotenv import load_dotenv
import os
import time as t
import sys

load_dotenv()
config = {
      'user': os.getenv("USER_DB"),
      'password': os.getenv("PASSWORD_DB"),
      'host': os.getenv("HOST_DB"),
      'database': os.getenv("DATABASE_DB")
    }
def limpar_tela():
    if os.name == 'nt':
        os.system("cls")
    else:
        os.system("clear")
limpar_tela()

def setup_config_pc():
    # Faz os Comandos no CMD
    serial_number = sub.run(["powershell", "-Command", "(Get-CimInstance Win32_BIOS).SerialNumber"], capture_output=True, text=True, check=True)
    comando_UUID = sub.run(["powershell", "-Command", "(Get-CimInstance Win32_ComputerSystemProduct).UUID"], capture_output=True, text=True, check=True)
    comando_serial_motherboard = sub.run(["powershell", "-Command", "(Get-CimInstance Win32_BaseBoard).SerialNumber"], capture_output=True, text=True, check=True)

    # Formata o Comando
    serial_number = serial_number.stdout.strip().split("\n")[-1].strip()
    UUID = comando_UUID.stdout.strip().split("\n")[-1].strip()
    Motherboard = comando_serial_motherboard.stdout.strip().split("\n")[-1].strip()
    # Chama a busca para ver se é existente
    resultado_existe_maquina = buscar_fk_maquina(serial_number,UUID,Motherboard)
    if resultado_existe_maquina == []:
        Fkescola = config_escola()
        limpar_tela()
        nome_maquina = input("Nomeie a Máquina Cadastrada: ")
        inserir_maquina_a_escola(serial_number,UUID,Motherboard,Fkescola,nome_maquina)
        FkMaquina = buscar_fk_maquina(serial_number,UUID,Motherboard)
        FkMaquina = FkMaquina[0][0]
        configurar_componetes_a_monitorar(FkMaquina,Fkescola)


def config_escola():
    limpar_tela()
    print("-----------------------------------------------------")
    print("Seu computador não está cadastrado em nenhuma escola")
    codigo_inep_input = input("Utilize o código do Inep para cadastrar: ")
    inep_val = validar_codigo_inep(codigo_inep_input)
    if inep_val == []:
        limpar_tela()
        print("-----------------------------------------------------")
        print("Código do INEP Invalído")
        print("Seu computador não está cadastrado em nenhuma escola")
        codigo_inep_input = input("Utilize o código do Inep para cadastrar: ")
        inep_val = validar_codigo_inep(codigo_inep_input)
    else:
        limpar_tela()
        print("-----------------------------------------------------")
        print(f"Deseja cadastrar um computador na {inep_val[0][1]}")
        operacao = input("Continuar (s / n) ").lower()
        while operacao != 's' and operacao != 'n':
            limpar_tela()
            print("-----------------------------------------------------")
            print(f"Deseja cadastrar um computador na escola {inep_val[0][1]}")
            operacao = input("Continuar (s / n)").lower()
        if operacao == "n":
            config_escola()
    codigo_acesso_input = input("Coloque o código de configuração da sua organização: ")
    tentavivas = 3
    while True:
        if tentavivas == 3:
            codigo_vali = validar_codigo_acesso(codigo_acesso_input,codigo_inep_input)
            if codigo_vali != []:
                break
        limpar_tela()
        print(f"Código Invalído. Faltam {tentavivas} Tentativas")
        codigo_acesso_input = input("Coloque o código de configuração da sua organização: ")
        codigo_vali = validar_codigo_acesso(codigo_acesso_input,codigo_inep_input)
        if codigo_vali != []:
            break
        tentavivas = tentavivas - 1
        if tentavivas == 0:
            limpar_tela()
            mensagem = "Números de Tentativas execido, Fechando o programa"
            print(mensagem)
            t.sleep(1)
            limpar_tela()
            mensagem += "."
            print(mensagem)
            t.sleep(1)
            limpar_tela()
            mensagem += "."
            print(mensagem)
            t.sleep(1)
            limpar_tela()
            mensagem += "."
            print(mensagem)
            t.sleep(1)
            sys.exit()
    limpar_tela()
    mensagem = "Cadastro realizado com Sucesso ."
    print(mensagem)
    t.sleep(1)
    limpar_tela()
    mensagem += "."
    print(mensagem)
    t.sleep(1)
    limpar_tela()
    mensagem += "."
    print(mensagem)
    t.sleep(1)
    limpar_tela()
    mensagem += "."
    print(mensagem)
    t.sleep(1)
    print(codigo_vali)
    return codigo_vali[0][0]



def validar_codigo_inep(codigo):
    try:
        db = connect(**config)
        if db.is_connected():
            db_info = db.server_info
            print('Connected to MySQL server version -', db_info)
            limpar_tela()
            with db.cursor() as cursor:
                query = f"SELECT * FROM safeclass.Escola WHERE Codigo_INEP = '{codigo}';"
                cursor.execute(query)
                resultado = cursor.fetchall() 
                
            cursor.close()
            db.close()
            return resultado
    
    except Error as e:
        print('Error to connect with MySQL -', e)

def validar_codigo_acesso(codigo,inep):
    try:
        db = connect(**config)
        if db.is_connected():
            db_info = db.server_info
            print('Connected to MySQL server version -', db_info)
            limpar_tela()
            with db.cursor() as cursor:
                query = f"SELECT * FROM safeclass.Escola WHERE Codigo_Config = '{codigo}' and Codigo_INEP = '{inep}';"
                cursor.execute(query)
                resultado = cursor.fetchall() 
                
            cursor.close()
            db.close()
            return resultado
    
    except Error as e:
        print('Error to connect with MySQL -', e)
def insert_no_banco(query):
    try:
        db = connect(**config)
        if db.is_connected():
            db_info = db.server_info
            print('Connected to MySQL server version -', db_info)
            limpar_tela()
            with db.cursor() as cursor:
                cursor.execute(query)
                
                db.commit()
                print(cursor.rowcount, "registro inserido")
            
            cursor.close()
            db.close()
    
    except Error as e:
        print('Error to connect with MySQL -', e)

def inserir_maquina_a_escola(serial_bios,UUID,serial_motherboard,fkescola,nome):
    try:
        db = connect(**config)
        if db.is_connected():
            db_info = db.server_info
            print('Connected to MySQL server version -', db_info)
            limpar_tela()
            with db.cursor() as cursor:
                query = "INSERT INTO safeclass.Maquina (IdMaquina, UUID,Serial_number_bios,Serial_motherboard,FkEscola,Nome_indetificao) VALUES (default, %s,%s,%s,%s,%s)"
                value = (UUID,serial_bios,serial_motherboard,fkescola,nome)
                cursor.execute(query, value)
                
                db.commit()
                print(cursor.rowcount, "registro inserido")
            
            cursor.close()
            db.close()
    
    except Error as e:
        print('Error to connect with MySQL -', e)


def buscar_fk_maquina(serial_bios,UUID,serial_motherboard):
    try:
        db = connect(**config)
        if db.is_connected():
            db_info = db.server_info
            print('Connected to MySQL server version -', db_info)
            limpar_tela()
            with db.cursor() as cursor:
                query = f"SELECT IdMaquina,FkEscola FROM safeclass.Maquina WHERE Serial_number_bios = '{serial_bios}' and UUID = '{UUID}' and Serial_motherboard = '{serial_motherboard}';"
                cursor.execute(query)
                resultado = cursor.fetchall() 
                
            cursor.close()
            db.close()
            return resultado
    
    except Error as e:
        print('Error to connect with MySQL -', e) 

def configurar_componetes_a_monitorar(FkMaquina,FkEscola):
    limpar_tela()
    print("-----------------------------------------------------------")
    print("Olá vimos que você não configurou sua máquina")
    monitorar_cpu_percent = input("Você deseja monitorar a porcentagem(%) de uso da CPU (s / n) \n").lower()
    while monitorar_cpu_percent != 's' and monitorar_cpu_percent != 'n':
        print("Opção Invalída tente novamente")
        monitorar_cpu_percent = input("Você deseja monitorar a porcentagem(%) de uso da CPU (s / n) \n").lower()
    monitorar_cpu_freq = input("Você deseja monitorar a Frequência(GHz) da CPU (s / n) \n").lower()
    while monitorar_cpu_freq != 's' and monitorar_cpu_freq != 'n':
        print("Opção Invalída tente novamente")
        monitorar_cpu_freq = input("Você deseja monitorar a Frequência(GHz) da CPU (s / n) \n").lower()
    monitorar_memoria_percent = input("Você deseja monitorar o uso de memória RAM(%) (s / n) \n").lower()
    while monitorar_memoria_percent != 's' and monitorar_memoria_percent != 'n':
        print("Opção Invalída tente novamente")
        monitorar_memoria_percent = input("Você deseja monitorar o uso de memória RAM(%) (s / n) \n").lower()
    monitorar_memoria_total = input("Você deseja monitorar a memória RAM total(GB) (s / n) \n").lower()
    while monitorar_memoria_total != 's' and monitorar_memoria_total != 'n':
        print("Opção Invalída tente novamente")
        monitorar_memoria_total = input("Você deseja monitorar a memória RAM total(GB) (s / n) \n").lower()
    monitorar_disco_uso = input("Você deseja monitorar o uso do Disco(GB) (s / n) \n").lower()
    while monitorar_disco_uso != 's' and monitorar_disco_uso != 'n':
        print("Opção Invalída tente novamente")
        monitorar_disco_uso = input("Você deseja monitorar o uso do Disco(GB) (s / n) \n").lower()
    monitorar_disco_livre = input("Você deseja monitorar o espaço disponível do disco(GB) (s / n) \n").lower()
    while monitorar_disco_livre != 's' and monitorar_disco_livre != 'n':
        print("Opção Invalída tente novamente")
        monitorar_disco_livre = input("Você deseja monitorar o espaço disponível do disco(GB) (s / n) \n").lower()
    monitorar_disco_total = input("Você deseja monitorar o espaço total do disco(GB) (s / n) \n").lower()
    while monitorar_disco_total != 's' and monitorar_disco_total != 'n':
        print("Opção Invalída tente novamente")
    monitorar_disco_total = input("Você deseja monitorar o espaço total do disco(GB) (s / n) \n").lower()
    limpar_tela()
    print("-----------------------------------------------------------")
    print("Escolha do monitoramento")
    print(f"Porcentagem de uso da CPU(%): {monitorar_cpu_percent}\nFrequência de uso da CPU(GHz): {monitorar_cpu_freq}\nUso da Memória RAM(%): {monitorar_memoria_percent}\nMemória RAM Total(GB): {monitorar_memoria_total}\nUso do disco(GB): {monitorar_disco_uso}\nEspaço restante do disco(GB): {monitorar_disco_livre}\nEspaço do Disco(GB): {monitorar_disco_total}")
    t.sleep(2)
    acao = input("Confirma todos os monitoramentos ( s / n)  ").lower()
    while acao != 's' and acao != 'n':
        limpar_tela()
        print("-----------------------------------------------------------")
        print(f"Porcentagem de uso da CPU(%): {monitorar_cpu_percent}\nFrequência de uso da CPU(GHz): {monitorar_cpu_freq}\nUso da Memória RAM(%): {monitorar_memoria_percent}\nMemória RAM Total(GB): {monitorar_memoria_total}\nUso do disco(GB): {monitorar_disco_uso}\nEspaço restante do disco(GB): {monitorar_disco_livre}\nEspaço total do disco(GB): {monitorar_disco_total}")
        print("Opção Invalída tente novamente")
        acao = input("Confirma todos os monitoramentos ( s / n)  ").lower()
    if acao == 's':
        if monitorar_cpu_percent == "s":
            query = f"INSERT INTO safeclass.Maquina_monitoramento (FkMaquina,FkComponente,FkEscola) VALUES ({FkMaquina},1,{FkEscola});"
            insert_no_banco(query)
        if monitorar_cpu_freq == "s":
            query = f"INSERT INTO safeclass.Maquina_monitoramento (FkMaquina,FkComponente,FkEscola) VALUES ({FkMaquina},2,{FkEscola});"
            insert_no_banco(query)
        if monitorar_memoria_percent == "s":
            query = f"INSERT INTO safeclass.Maquina_monitoramento (FkMaquina,FkComponente,FkEscola) VALUES ({FkMaquina},3,{FkEscola});"
            insert_no_banco(query)
        if monitorar_memoria_total == "s":
            query = f"INSERT INTO safeclass.Maquina_monitoramento (FkMaquina,FkComponente,FkEscola) VALUES ({FkMaquina},4,{FkEscola});"
            insert_no_banco(query)
        if monitorar_disco_uso == "s":
            query = f"INSERT INTO safeclass.Maquina_monitoramento (FkMaquina,FkComponente,FkEscola) VALUES ({FkMaquina},5,{FkEscola});"
            insert_no_banco(query)
        if monitorar_disco_livre == "s":
            query = f"INSERT INTO safeclass.Maquina_monitoramento (FkMaquina,FkComponente,FkEscola) VALUES ({FkMaquina},6,{FkEscola});"
            insert_no_banco(query)
        if monitorar_disco_total == "s":
            query = f"INSERT INTO safeclass.Maquina_monitoramento (FkMaquina,FkComponente,FkEscola) VALUES ({FkMaquina},7,{FkEscola});"
            insert_no_banco(query)
        limpar_tela()
        
    else:
        configurar_componetes_a_monitorar(FkMaquina,FkEscola)

def select_generico(query):
    try:
        db = connect(**config)
        if db.is_connected():
            db_info = db.server_info
            print('Connected to MySQL server version -', db_info)
            limpar_tela()
            with db.cursor() as cursor:
                cursor.execute(query)
                resultado = cursor.fetchall() 
                
            cursor.close()
            db.close()
            return resultado
    
    except Error as e:
        print('Error to connect with MySQL -', e) 

def func_para_binario(FkComponentes):
    componentes = [item[0] for item in FkComponentes]
    binario = [0,0,0,0,0,0,0]
    contador = 0;
    while contador < len(componentes):
        binario[componentes[contador]-1] = 1
        contador += 1
    return binario

    

setup_config_pc()
serial_number = sub.run(["powershell", "-Command", "(Get-CimInstance Win32_BIOS).SerialNumber"], capture_output=True, text=True, check=True)
comando_UUID = sub.run(["powershell", "-Command", "(Get-CimInstance Win32_ComputerSystemProduct).UUID"], capture_output=True, text=True, check=True)
comando_serial_motherboard = sub.run(["powershell", "-Command", "(Get-CimInstance Win32_BaseBoard).SerialNumber"], capture_output=True, text=True, check=True)
# Formata o Comando
serial_number = serial_number.stdout.strip().split("\n")[-1].strip()
UUID = comando_UUID.stdout.strip().split("\n")[-1].strip()
Motherboard = comando_serial_motherboard.stdout.strip().split("\n")[-1].strip()
Fkescola = buscar_fk_maquina(serial_number,UUID,Motherboard)
FkMaquina = buscar_fk_maquina(serial_number,UUID,Motherboard)
Fkescola = Fkescola[0][1]
FkMaquina = FkMaquina[0][0]
FkComponetes = select_generico(f"SELECT FkComponente FROM safeclass.Maquina_monitoramento WHERE FkEscola = {Fkescola} AND FkMaquina = {FkMaquina};")
binario = func_para_binario(FkComponetes)



habilita_usoCPU = False
habilita_freqCPU = False
habilita_Mem_used = False
habilita_Mem_total = False
habilita_usoDisk = False
habilita_LivreDisk = False
habilita_Disco_total = False

if binario[0] == 1:
    habilita_usoCPU = True
if binario[1] == 1:
    habilita_freqCPU = True
if binario[2] == 1:
    habilita_Mem_used = True
if binario[3] == 1:
    habilita_Mem_total = True
if binario[4] == 1:
    habilita_usoDisk = True
if binario[5] == 1:
    habilita_LivreDisk = True
if binario[6] == 1:
    habilita_Disco_total = True


def captura():
    query = "INSERT INTO safeclass.Leitura (FkEscola,FkMaquina,FkComponente,Medida) VALUES"
    if habilita_usoCPU == True:
        usoCPU = p.cpu_percent(interval=1, percpu=False)
        query += f"({Fkescola},{FkMaquina},1,'{usoCPU}'),"
    if habilita_freqCPU == True:
        freqCPU = round((p.cpu_freq(percpu=False).current)/1000,2)
        query += f"({Fkescola},{FkMaquina},2,'{freqCPU}'),"
    if habilita_Mem_used == True:
        Mem_used = p.virtual_memory().percent
        query += f"({Fkescola},{FkMaquina},3,'{Mem_used}'),"
    if habilita_Mem_total == True:
        Mem_total = round(p.virtual_memory().total / (1024 ** 3),2)
        query += f"({Fkescola},{FkMaquina},4,'{Mem_total}'),"
    if habilita_usoDisk == True:
        usoDisk = round(p.disk_usage("C:/").used/ (1024**3),2)
        query += f"({Fkescola},{FkMaquina},5,'{usoDisk}'),"
    if habilita_LivreDisk == True:
        LivreDisk = round(p.disk_usage("C:/").free/ (1024**3),2)
        query += f"({Fkescola},{FkMaquina},6,'{LivreDisk}'),"
    if habilita_Disco_total == True:
        usoDisk = round(p.disk_usage("C:/").used/ (1024**3),2)
        LivreDisk = round(p.disk_usage("C:/").free/ (1024**3),2)
        Disco_total = usoDisk + LivreDisk
        query += f"({Fkescola},{FkMaquina},7,'{Disco_total}'),"
    if query.endswith(","):
        query = query[:-1] + ";"
    else:
        configurar_componetes_a_monitorar(FkMaquina,Fkescola)
    insert_no_banco(query)
    if habilita_usoCPU == True:
        t.sleep(9)
    else:
        t.sleep(10)
    captura()
    

captura()