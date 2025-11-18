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
     # Hostname da máquina
    dono_maquina = platform.node()

    # Dados de memória ram
    memoria = p.virtual_memory()  
    memoria_total_GB = memoria.total / (1024**3) 
    memoria_GB_free = memoria.available / (1024**3) 
    memoria_usada_GB = memoria_total_GB - memoria_GB_free 
    memoria_formatada_em_uso = f'{memoria_usada_GB:.2f}'


    # Dados do disco
    disco_objeto = p.disk_usage('/')
    disco_percent = disco_objeto.percent  


    # Dados de cpu
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


    time.sleep(1)