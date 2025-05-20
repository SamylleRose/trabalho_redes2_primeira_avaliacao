import os
import json

# Obtém o IP do roteador a partir de uma variável de ambiente chamada "rtr_ip"
RTR_IP = os.getenv("rtr_ip")

# Obtém e converte a vizinhança do roteador a partir de uma variável de ambiente JSON chamada "vizinhanca"
NGH = json.loads(os.getenv("vizinhanca"))

class LSA:
    #Classe para criação de pacotes LSA (Link-State Advertisement)
    
    @staticmethod
    def criar_pacote(sequencia: int):
        #Cria um pacote LSA com informações do roteador
      
        pacote = {
            "id": RTR_IP,               # Identificador do roteador (seu IP)
            "vizinhanca": NGH,          # Lista de vizinhos e custos dos enlaces
            "seq": sequencia            # Número de sequência (para controle de versão)
        }
        return pacote