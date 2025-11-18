import psutil as p
from mysql.connector import connect, Error
from dotenv import load_dotenv
import os
import datetime
import time
import platform
from tabulate import tabulate


load_dotenv()

config = {
      'user': os.getenv("USER"),
      'password': os.getenv("PASSWORD"),
      'host': os.getenv("HOST"),
      'database': os.getenv("DATABASE"),
      'port': int(os.getenv("PORT", 3306))
    }

def inserir_dados(porcentagem, memoria_usada_GB, disco_percent):
    try:
        db = connect(**config)
        if db.is_connected():
            with db.cursor() as cursor:

                # CPU
                cursor.execute("""
                    INSERT INTO safeclass.captura (fkComponente, registro, dtCaptura)
                    VALUES (%s, %s, %s)
                """, (3, porcentagem, datetime.datetime.now()))

                # Memória
                cursor.execute("""
                    INSERT INTO safeclass.captura (fkComponente, registro, dtCaptura)
                    VALUES (%s, %s, %s)
                """, (1, memoria_usada_GB, datetime.datetime.now()))

                # Disco
                cursor.execute("""
                    INSERT INTO safeclass.captura (fkComponente, registro, dtCaptura)
                    VALUES (%s, %s, %s)
                """, (2, disco_percent, datetime.datetime.now()))

                db.commit()

        db.close()
        print("✅ Inserções concluídas!")

    except Error as e:
        print('❌ Erro ao conectar ou inserir no MySQL:', e)

while True:
 
 # HOSTNAME DA MAQUINA
    dono_maquina = platform.node()

# DADOS DA MEMORIA
  

    memoria = p.virtual_memory()  # Captura todas as métricas da memória
    memoria_total_GB = memoria.total / (1024**3)  # Memória total em GB
    memoria_GB_free = memoria.available / (1024**3)  # Memória livre em GB
    memoria_usada_GB = memoria_total_GB - memoria_GB_free  # Memória usada em GB
    memoria_formatada_em_uso = f'{memoria_usada_GB:.2f}'  # Formata em 2 casas decimais


# DADOS DO DISCO

    disco_objeto = p.disk_usage('/')  # Captura o uso do disco da partição raiz '/'
    disco_percent = disco_objeto.percent  # Porcentagem de uso do disco
    disco_livre_gb = disco_objeto.free / (1024**3)  # Espaço livre em GB
    disco_usado_gb = (disco_objeto.total - disco_objeto.free) / (1024**3)  # Espaço usado em GB
    disco_usado_formatado = f'{disco_usado_gb:.2f}'  # Formata em 2 casas decimais


# dados de cpu
    porcentagem = p.cpu_percent(interval=1, percpu=False)


    

    captura = [
        ["Hostname", dono_maquina],
        ["CPU % (USO)", f"{porcentagem}%"],
        ["Memória em Uso (GB)", f"{memoria_formatada_em_uso} GB"],
        ["Disco % (USO)", f"{disco_percent:.1f}%"]
    ]

    print("""
    ╔════════════════════════════════════════════╗
    ║                                            ║
    ║     ✅ DADOS INSERIDOS COM SUCESSO!       ║
    ║                                            ║
    ║   Os dados foram gravados no banco de      ║
    ║  forma segura e o sistema foi atualizado.  ║
    ╚════════════════════════════════════════════╝
    """)


    print(tabulate(captura, headers=["Componente", "Valor"], tablefmt="fancy_grid"))
    
    inserir_dados(porcentagem, memoria_usada_GB, disco_percent)


    time.sleep(4)