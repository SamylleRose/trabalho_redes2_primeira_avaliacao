# Importa tipos para documentação de código (tipagem)
from typing import Dict, Tuple, Any

def dijkstra(origem: str, lsdb: Dict[str, Any]) -> Dict[str, str]:
    """Calcula os caminhos mais curtos do roteador de origem para todos os outros na rede.
    
    Args:
        origem: Endereço IP do roteador de origem
        lsdb: Banco de dados de estado de enlace (topologia da rede)
        
    Returns:
        Dicionário mapeando roteadores de destino para seus próximos saltos
    """

    # Passo 1: Construir o grafo da rede a partir do LSDB
    grafo = {}
    for idRouter, lsa in lsdb.items():
        vizinhanca = {}
        # Processa cada vizinho no LSA
        for v in lsa["vizinhanca"].values():
            ip, custo = v  # Separa IP do vizinho e custo do enlace
            # Só inclui vizinhos que existem no nosso LSDB
            if ip in lsdb:
                vizinhanca[ip] = custo
        grafo[idRouter] = vizinhanca  # Adiciona ao grafo
        
    # Passo 2: Inicializa estruturas de dados do Dijkstra
    distancias = {i: float('inf') for i in grafo}  # Todas distâncias começam infinitas
    anterior = {i: None for i in grafo}  # Nó anterior no caminho ótimo
    distancias[origem] = 0  # Distância para si mesmo é zero
    visitados = set()  # Conjunto de nós já processados
    
    # Passo 3: Loop principal do algoritmo Dijkstra
    while len(visitados) < len(grafo):
        # Encontra o nó não visitado com menor distância conhecida
        x = min((i for i in grafo if i not in visitados), 
               key=lambda i: distancias[i])
        visitados.add(x)  # Marca como visitado
        
        # Atualiza distâncias dos vizinhos
        for v, c in grafo[x].items():
            # Se encontrou um caminho mais curto para o vizinho v
            if distancias[x] + c < distancias[v]:
                distancias[v] = distancias[x] + c  # Atualiza distância
                anterior[v] = x  # Atualiza caminho
                
    # Passo 4: Constrói tabela de roteamento a partir dos caminhos
    tabela = {}
    for destino in grafo:
        # Ignora a origem e nós inalcançáveis
        if destino == origem or anterior[destino] is None:
            continue
            
        # Rastreia o caminho de volta para encontrar o próximo salto
        salto = destino
        while anterior[salto] != origem:
            salto = anterior[salto]
        tabela[destino] = salto  # Mapeia destino para próximo salto
        
    return tabela