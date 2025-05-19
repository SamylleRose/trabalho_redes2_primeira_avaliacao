
import os

class Cores:
    LARANJA = '\033[38;2;224;167;106m'
    VERDE = '\033[38;2;66;191;161m'
    ROXO = '\033[38;2;161;114;243m'
    AZUL = '\033[38;2;114;186;243m'
    VERMELHO = '\033[38;2;243;138;138m'
    AMARELO = '\033[38;2;243;228;114m'
    SEM_COR = '\033[0m'



def pegar_roteadores() -> list:
   
    saida = os.popen("docker ps --filter 'name=router' --format '{{.Names}}'").read()
    return sorted(saida.splitlines())

def pegar_tRoteamento(container) -> str:
   
    cmd = f"docker exec {container} ip route"
    print(f"{cmd}")
    return os.popen(cmd).read()



for container in pegar_roteadores():
    print(pegar_tRoteamento(container))