# Projeto de Redes - Protocolo Link-State com Docker

Este projeto inclui:

* **Roteamento Dinâmico (OSPF):** Implementação de um protocolo de roteamento OSPF para simular
a descoberta e atualização automática de rotas na rede.
* **Contêineres Docker:** Utilização de Docker para isolar e gerenciar cada roteador e host como 
um contêiner individual, facilitando a criação e o desmantelamento do ambiente de rede.
* **Testes de Conectividade:** Scripts para verificar a conectividade (`ping`) entre os hosts, 
validando o funcionamento do roteamento.
* **Análise de Desempenho:** Ferramentas e scripts para coletar e analisar métricas cruciais:
* **Tempo de Convergência:** Medição do tempo que a rede leva para se recuperar e restabelecer a 
conectividade após a ocorrência de falhas em roteadores.
* **Throughput de LSA:** Análise da capacidade de processamento de Link-State Advertisements (LSAs) 
pelos roteadores sob diferentes volumes de tráfego.
* **Uso de Recursos:** Monitoramento do consumo de CPU e memória dos contêineres de rede durante a 
simulação e sob carga.



## 📋 Como Executar o Projeto

### Pré-requisitos
- Docker instalado
- Docker Compose (normalmente incluso com Docker Desktop)

### 🚀 Execução

1. Clone o repositório:
   git clone [https://github.com/SamylleRose/trabalho_redes2_primeira_avaliacao.git]

2. Inicie a topologia:

   docker-compose up --build

3. Para testar a conectividade entre hosts:

    Para verificar a conectividade entre todos os hosts:
    ```bash
    python3 script/conexao_host.py
    ```
    Este script executará pings de cada host para todos os outros e reportará o status de 
    sucesso/falha e o tempo de resposta.


## 📡 Justificativa dos Protocolos Escolhidos

### UDP para Pacotes LSA

Eficiência: Pacotes LSA são pequenos e frequentes. UDP evita overhead de conexão.

Tolerância a perdas: O protocolo link-state é resiliente a pacotes perdidos 
(atualizações periódicas compensam perdas).

Multicast/Não-confiável: Natural para flooding de atualizações de topologia.

Número de porta 5000: Porta alta não privilegiada, evitando conflitos.

## 🌐 Topologia da Rede


![Diagrama da Topologia da Rede](docs/topologia.jpg)

*Substitua `docs/topologia.png` pelo caminho real da sua imagem. É uma boa prática criar uma pasta `docs` para armazenar imagens e documentação.*

### Como a Topologia Foi Construída

A topologia desta simulação foi cuidadosamente projetada e implementada utilizando o 
**Docker Compose**, que permite definir e executar aplicações multi-container. 
Cada elemento da rede (roteador e host) é instanciado como um contêiner Docker 
separado, facilitando o isolamento e a configuração individual de cada nó.

Os principais componentes e técnicas utilizadas na construção da topologia são:

1.  **Contêineres Docker para Hosts e Roteadores:**
    * Cada **host** é representado por um contêiner Docker que executa um script Python (`host.py`). 
    Este script pode simular as funcionalidades básicas de um host, como a capacidade de enviar e receber pings.
    * Cada **roteador** é representado por um contêiner Docker que executa um script Python (`router.py`). 
    Este script é responsável por implementar a lógica do protocolo de roteamento dinâmico (OSPF), 
    gerenciando as tabelas de roteamento e trocando informações de rota com outros roteadores.

2.  **Redes Docker Personalizadas (Custom Docker Networks):**
    * Para simular sub-redes independentes e a interconexão entre roteadores, foram criadas 
    **redes Docker personalizadas**. 
    Cada segmento de rede, como a conexão entre um roteador e seus hosts, ou a conexão entre dois 
    roteadores, é uma rede Docker distinta.
    * Essas redes são definidas no arquivo `docker-compose.yml` com faixas de IP específicas 
    (e.g., `172.20.X.0/24`), garantindo que cada 
    interface de um contêiner esteja em sua sub-rede correta.

3.  **Configuração de Interfaces e IPs:**
    * Dentro do `docker-compose.yml`, cada serviço (host ou roteador) tem suas interfaces de rede 
    configuradas explicitamente para se conectar às redes Docker apropriadas.
    * Endereços IP estáticos são atribuídos a cada interface de cada contêiner (e.g., `ipv4_address: 172.20.1.11`), 
    replicando a configuração de uma rede física. Isso é crucial para o roteamento correto e
    para a operação do OSPF.

4.  **Protocolo OSPF (Open Shortest Path First):**
    * O OSPF foi escolhido como o protocolo de roteamento dinâmico. A lógica de seu funcionamento 
    (troca de Link-State Advertisements - LSAs, 
    cálculo da árvore de menor caminho, atualização da tabela de roteamento) é implementada nos scripts 
    Python dos roteadores.
    * A natureza "Link-State" do OSPF é ideal para demonstrar a convergência da rede e a resiliência a 
    falhas, pois todos os roteadores 
    constroem uma visão completa da topologia.

5.  **Arquivo `docker-compose.yml`:**
    * Este arquivo central orquestra toda a infraestrutura. Ele define:
        * Os serviços (contêineres de hosts e roteadores).
        * As imagens base (ou a construção de imagens a partir de Dockerfiles).
        * Os comandos de inicialização para cada contêiner (e.g., `python host.py` ou `python router.py`).
        * As redes Docker personalizadas e a atribuição de interfaces e IPs a cada contêiner.

