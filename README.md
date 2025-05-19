# Projeto de Redes - Protocolo Link-State com Docker

Implementação de um protocolo de roteamento link-state (OSPF-like) usando containers Docker, threads para envio/recebimento de LSAs e algoritmo de Dijkstra para cálculo de rotas.

## 📋 Como Executar o Projeto

### Pré-requisitos
- Docker instalado
- Docker Compose (normalmente incluso com Docker Desktop)

### 🚀 Execução

1. Clone o repositório:
   git clone [URL_DO_REPOSITORIO]

2. Inicie a topologia:

   docker-compose up --build

3. Para testar a conectividade entre hosts:

   docker exec -it host1_1 ping 172.20.4.11  # Exemplo: ping do host1_1 para host4_1

4. Para visualizar logs de um roteador:

   docker logs r1  # Substitua 'r1' pelo nome do container desejado

## 📡 Justificativa dos Protocolos Escolhidos

### UDP para Pacotes LSA

Eficiência: Pacotes LSA são pequenos e frequentes. UDP evita overhead de conexão.

Tolerância a perdas: O protocolo link-state é resiliente a pacotes perdidos (atualizações periódicas compensam perdas).

Multicast/Não-confiável: Natural para flooding de atualizações de topologia.

Número de porta 5000: Porta alta não privilegiada, evitando conflitos.

## 🌐 Topologia da Rede

6 roteadores em topologia parcialmente conectada
2 hosts por sub-rede