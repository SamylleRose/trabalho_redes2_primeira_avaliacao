import time
import socket
import os
import subprocess



def configurar_rota_padrao():
    rtr_ip = os.getenv("rtr_ip")
    if not rtr_ip:
        print("A variável rtr_ip não está definida!")
        exit(1)
    
    try:
        subprocess.run(["ip", "route", "del", "default"], check=True)
        subprocess.run(["ip", "route", "add", "default", "via", rtr_ip], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao configurar rotas: {e}")
        exit(1)

if __name__ == "__main__":
    configurar_rota_padrao()

# Imprime a string [HOST] no terminal
print("[HOST]")
while True:
    print("Iniciando processo de comunicação...")
    time.sleep(5)
    