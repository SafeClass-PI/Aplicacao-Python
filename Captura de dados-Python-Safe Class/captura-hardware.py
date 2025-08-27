import psutil as p
import time as t

def captura_cpu():
    usoCPU = p.cpu_percent(interval=1, percpu=False)
    freqCPU = (p.cpu_freq(percpu=False).current)/1000
    return usoCPU, freqCPU
def captura_memoria():
    Mem_used = p.virtual_memory().percent
    Mem_total = round(p.virtual_memory().total / (1024 ** 3),2)
    return Mem_used, Mem_total
def armazenamento():
    usoDisk = p.disk_usage("C:/").used/ (1024**3)
    LivreDisk = p.disk_usage("C:/").free/ (1024**3)
    Disco_total = usoDisk + LivreDisk
    return round(usoDisk, 2), round(LivreDisk,2), round(Disco_total,2)

while True:
    print("\
|===========================|\n\
| O que deseja capturar?    |\n\
|===========================|\n\
|-Apenas CPU             (1)|\n\
|-Apenas Memória         (2)|\n\
|-Apenas Armazenamento   (3)|\n\
|-CPU e Memória          (4)|\n\
|-CPU e Armazenamento    (5)|\n\
|-Memória e Armazenamento(6)|\n\
|-Capturar todas         (7)|\n\
|-Fechar programa        (S)|\n\
|===========================|")
    resp_painel = input("Insira o comando: ")
    if resp_painel == "S":
        print("\n\n Goodbye\n\n")
        t.sleep(1)
        break
    elif resp_painel == "1":
        print("\n Você Iniciou a captura de apenas CPU\n")
        while True:
            t.sleep(5)
            usoCPU = captura_cpu()[0]
            freqCPU = captura_cpu()[1]
            print(f"|Uso da CPU: {usoCPU}% - Frequencia CPU: {freqCPU}Ghz |")
    elif resp_painel == "2":
        print("\n Você Iniciou a captura de apenas Memória\n")
        while True:
            t.sleep(5)
            Mem_used = captura_memoria()[0]
            Mem_free = captura_memoria()[1]
            print(f"|Uso da Memória: {Mem_used}% - Memória Total : {Mem_free}GB |")
    elif resp_painel == "3":
        print("\n Você Iniciou a captura de apenas armazenamento\n")
        while True:
            t.sleep(5)
            usoDisk = armazenamento()[0]
            LivreDisk = armazenamento()[1]
            Disco_total = armazenamento()[2]
            print(f"|Uso do Disco: {usoDisk}GB - Espaço em Disco Livre: {LivreDisk}GB -  Armazenamento total:{Disco_total}GB |")
    elif resp_painel == "4":
        print("\n Você Iniciou a captura de CPU e Memória\n")
        while True:
            t.sleep(5)
            usoCPU = captura_cpu()[0]
            freqCPU = captura_cpu()[1]
            Mem_used = captura_memoria()[0]
            Mem_free = captura_memoria()[1]
            print(f"|Uso da CPU: {usoCPU}% - Frequencia CPU: {freqCPU}Ghz |")
            print(f"|Uso da Memória: {Mem_used}% - Memória Total : {Mem_free}GB |\n")
    elif resp_painel == "5":
         print("\n Você Iniciou a captura de CPU e Armazenamento\n")
         while True:
            t.sleep(5)
            usoCPU = captura_cpu()[0]
            freqCPU = captura_cpu()[1]
            usoDisk = armazenamento()[0]
            LivreDisk = armazenamento()[1]
            Disco_total = armazenamento()[2]
            print(f"|Uso da CPU: {usoCPU}% - Frequencia CPU: {freqCPU}Ghz |")
            print(f"|Uso do Disco: {usoDisk}GB - Espaço em Disco Livre: {LivreDisk}GB -  Armazenamento total:{Disco_total}GB |\n")
    elif resp_painel == "6":
         print("\n Você Iniciou a captura de Memória e Armazenamento\n")
         while True:
            t.sleep(5)
            Mem_used = captura_memoria()[0]
            Mem_free = captura_memoria()[1]
            usoDisk = armazenamento()[0]
            LivreDisk = armazenamento()[1]
            Disco_total = armazenamento()[2]
            print(f"|Uso da Memória: {Mem_used}% - Memória Total : {Mem_free}GB |")
            print(f"|Uso do Disco: {usoDisk}GB - Espaço em Disco Livre: {LivreDisk}GB -  Armazenamento total:{Disco_total}GB |\n")
    elif resp_painel == "7":
         print("\n Você Iniciou a captura de CPU, Memória e Armazenamento\n")
         while True:
            t.sleep(5)
            Mem_used = captura_memoria()[0]
            Mem_free = captura_memoria()[1]
            usoDisk = armazenamento()[0]
            LivreDisk = armazenamento()[1]
            Disco_total = armazenamento()[2]
            usoCPU = captura_cpu()[0]
            freqCPU = captura_cpu()[1]
            print(f"|Uso da CPU: {usoCPU}% - Frequencia CPU: {freqCPU}Ghz |")
            print(f"|Uso da Memória: {Mem_used}% - Memória Total : {Mem_free}GB |")
            print(f"|Uso do Disco: {usoDisk}GB - Espaço em Disco Livre: {LivreDisk}GB -  Armazenamento total:{Disco_total}GB |\n")
    else:
        print("\n\
|==================|\n\
| Comando invalido |\n\
|==================|\n")
        t.sleep(0.5)
        print("recarregando...")
        t.sleep(0.5)