import json  
import os  
import time  
import threading  
import socket  
import subprocess  
import os
import subprocess
from typing import Dict, Tuple, Any  
from dijkstra import dijkstra  
from lsa import LSA  
from typing import Dict, Tuple, Any


def configurar_rota_padrao():

    rtr_ip = os.getenv("rtr_ip")
    if not rtr_ip:
        print("A variável rtr_ip não está definida!")
        exit(1)
    
    try:
        # Remove rota padrão existente
        subprocess.run(["ip", "route", "del", "default"], check=True)
        # Adiciona nova rota padrão
        subprocess.run(["ip", "route", "add", "default", "via", rtr_ip], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao configurar rotas: {e}")
        exit(1)

# Chama a configuração no início da execução
if __name__ == "__main__":
    configurar_rota_padrao()

# Configurações globais do roteador
RTR_IP = os.getenv("rtr_ip")  # IP do roteador (definido por variável de ambiente)
RTR_NAME = os.getenv("rtr_nome")  # Nome do roteador (variável de ambiente)
NGH = json.loads(os.getenv("vizinhanca"))  # Vizinhança (vizinhos e custos em JSON)
PORTA_LSA = 5000  # Porta UDP para comunicação LSA

class Configuracoes:
    #Classe responsável por manipular as rotas do sistema
    
    @staticmethod
    def obter_rotas(rotas: Dict[str, str]) -> Tuple[Dict[str, str], Dict[str, str]]:
        #Compara rotas calculadas com rotas existentes no sistema
        rotas_existentes = {}  # Rotas já configuradas
        rotas_sistema = {}  # Rotas padrão do sistema
        adicionar = {}  # Rotas a serem adicionadas
        substituir = {}  # Rotas a serem substituídas
        
        try:
            # Converte IPs destino para formato de rede (ex: 192.168.1.0/24)
            novas_rotas = {}
            for destino, proximo_salto in rotas.items():
                parts = destino.split('.')
                prefixo = '.'.join(parts[:3])
                network = f"{prefixo}.0/24"
                novas_rotas[network] = proximo_salto
            
            # Obtém rotas atuais do sistema
            resultado = subprocess.run(
                ["ip", "route", "show"],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Processa as rotas existentes
            for linha in resultado.stdout.splitlines():
                partes = linha.split()
                
                # Rotas configuradas manualmente
                if partes[0] != "default" and partes[1] == "via":
                    rede = partes[0]  # ex: 172.20.5.0/24
                    proximo_salto = partes[2]  # ex: 172.20.4.3
                    rotas_existentes[rede] = proximo_salto
                    
                # Rotas do sistema (interfaces locais)
                elif partes[1] == 'dev':
                    rede = partes[0]
                    proximo_salto = partes[-1]
                    rotas_sistema[rede] = proximo_salto
                
            # Identifica rotas para substituição
            for rede, proximo_salto in novas_rotas.items():
                if (rede in rotas_existentes) and (rotas_existentes[rede] != proximo_salto):
                    substituir[rede] = proximo_salto
                    
            # Identifica rotas para adição
            for rede, proximo_salto in novas_rotas.items():
                if (rede not in rotas_existentes) and (rede not in rotas_sistema):
                    adicionar[rede] = proximo_salto

            return adicionar, substituir    
        except Exception as e:
            Log.log(f"Erro ao obter rotas existentes: {e}")
            return {}, {}
        
    @staticmethod
    def adicionar_rotas(salto: str, destino: str) -> bool:
        #Adiciona uma nova rota ao sistema
        try:
            # Formata o destino para o padrão de rede
            p = destino.split('.')
            prefixo = '.'.join(p[:3])
            destino = f"{prefixo}.0/24"
            
            # Executa o comando para adicionar rota
            comando = f"ip route add {destino} via {salto}"
            processo = subprocess.run(
                comando.split(),
                capture_output=True
            )
            Log.log(f"[LOG] Rota adicionada com sucesso!")
        except subprocess.CalledProcessError as error:
            Log.log(f"[ERROR] Erro ao adicionar rota: {error}")
        except Exception as e:
            Log.log(f"[ERROR] Erro ao tentar adicionar rota: {error}")
    
    @staticmethod
    def substitui_rotas(salto: str, destino: str) -> bool:
        #Substitui uma rota existente
        try:
            # Formata o destino para o padrão de rede
            p = destino.split('.')
            prefixo = '.'.join(p[:3])
            destino = f"{prefixo}.0/24"
            
            # Executa o comando para substituir rota
            comando = f"ip route replace {destino} via {salto}"
            processo = subprocess.run(comando.split(), check=True)
            Log.log(f"[LOG] Rota substituída: {destino} via {salto}") if processo.returncode == 0 else Log.log(f"[LOG] Problema ao substituir rota: {processo.stderr.decode()}")
            return True
        except Exception as error:
            Log.log(f"[LOG] Error de substituicao de rotas: {error}")
        return False
    
    @staticmethod
    def configurar_inter(lsdb: Dict[str, Any]) -> None:
        #Configura as rotas no sistema com base no LSDB
        # Calcula as melhores rotas usando Dijkstra
        rotas = dijkstra(RTR_IP, lsdb)
        
        # Filtra apenas rotas para vizinhos diretos
        caminhos = {}
        for destino, salto in rotas.items():
            for v, ip_custo in NGH.items():
                ip, _ = ip_custo
                if salto == ip:
                    caminhos[destino] = salto
                    break
                
        # Obtém rotas para adicionar/substituir
        add, substituir = Configuracoes.obter_rotas(caminhos)
        
        # Aplica as alterações
        for destino, salto in add.items():
            Configuracoes.adicionar_rotas(salto, destino)
                
        for destino, salto in substituir.items():
            Configuracoes.substitui_rotas(salto, destino)

class Log:
    #Classe para registro de logs formatados
    
    @staticmethod
    def log(msg: str) -> None:
        #Registra uma mensagem de log com timestamp
        timestmp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f"[{RTR_IP}] {msg} - {timestmp}", flush=True)

class Roteador:
    #Classe principal que implementa o roteador
    
    def __init__(self) -> None:
        #Inicializa o roteador
        self.lsdb = {}  # Banco de dados de estados de enlace
        self.thread = threading.Lock()  # Lock para sincronização de threads
        
        Log.log(f"Iniciando o roteador!")
        
    def enviar_pacotes(self) -> None:
        #Envia pacotes LSA periodicamente para vizinhos
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sequencia = 0
        
        while True:
            sequencia += 1
            # Cria um novo pacote LSA
            pacote = LSA.criar_pacote(sequencia)
        
            # Envia para todos os vizinhos
            msg = json.dumps(pacote).encode()
            for v, ip_custo in NGH.items():
                ip, custo = ip_custo
                sock.sendto(msg, (ip, PORTA_LSA))
                Log.log(f"[{ip}] A mensagem foi enviado com sucesso!")
                
            # Atualiza o LSDB local e configura rotas
            with self.thread:
                self.lsdb[RTR_IP] = pacote
                self.salvar_lsdb(self.lsdb)
                Configuracoes.configurar_inter(self.lsdb)
                
            time.sleep(10)  # Espera 10 segundos entre envios
            
    def receber_pacotes(self) -> None:
        #Recebe pacotes LSA de outros roteadores
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            sock.bind(("0.0.0.0", PORTA_LSA))  # Escuta em todas as interfaces
        except socket.error as bind_error:
            return

        while True:
            try:
                # Recebe pacote
                dado, end = sock.recvfrom(4096)
                Log.log(f"Pacote recebido de {end}")
                lsa = json.loads(dado.decode())
                origem = lsa["id"]
                
                # Se for um LSA novo, faz flooding e atualiza LSDB
                if origem not in self.lsdb or lsa["seq"] > self.lsdb[origem]["seq"]:
                    # Flooding: envia para todos os vizinhos exceto o remetente
                    for v, ip_custo in NGH.items():
                        ip, _ = ip_custo
                        if ip != end[0]:
                            sock.sendto(dado, (ip, PORTA_LSA))
                
                    # Atualiza LSDB e rotas
                    with self.thread:
                        self.lsdb[origem] = lsa
                        self.salvar_lsdb(self.lsdb)
                        Configuracoes.configurar_inter(self.lsdb)
                
                Log.log(f"Recebendo pacote dessa origem: {origem}")
            except socket.error as error:
                Log.log(f"Erro ao receber LSA: {error}")
            except json.JSONDecodeError:
                Log.log("Erro ao decodificar LSA recebido.")
            except Exception as error:
                Log.log(f"Erro inesperado ao receber LSA: {error}")
          
    def salvar_lsdb(self, lsdb: Dict[str, Any]) -> None:
        #Salva o LSDB em um arquivo JSON
        try:
            with open("lsdb.json", "w") as file:
                json.dump(lsdb, file, indent=4)
        except Exception as error:
            Log.log(f"[{error}] Erro ao salvar o LSDB")
               

if __name__ == "__main__":
    # Ponto de entrada principal
    r1 = Roteador()
    
    # Cria e inicia threads para envio e recebimento
    threads = [
        threading.Thread(target=r1.enviar_pacotes, daemon=True, name="enviar_lsa"),
        threading.Thread(target=r1.receber_pacotes, daemon=True, name="receber_lsa"),
    ]
    
    for thread in threads:
        thread.start()
    
    # Mantém o programa rodando
    threading.Event().wait()