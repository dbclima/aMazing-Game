import random
from dataclasses import dataclass
from typing import Tuple, List, Dict

import networkx as nx

from randomized_perfect_maze import create_perfect_maze_from_MST

@dataclass
class Labirinto:
    grafo: nx.Graph
    dimensoes: Tuple[int, int]
    origem: Tuple[int, int]
    chegada: Tuple[int, int]
    checkpoints: Dict[Tuple[int, int], int]

def criar_labirinto(n_linhas: int, n_colunas: int, algoritmo="kruskal") -> Labirinto:
    G = nx.grid_graph((n_linhas, n_colunas))
    
    T = create_perfect_maze_from_MST(G, algoritmo)

    center_node = list(T.nodes())[0]
    distances = nx.single_source_shortest_path_length(T, center_node)

    start_node = max(distances, key=distances.get)
    distances = nx.single_source_shortest_path_length(T, start_node)

    end_node = max(distances, key=distances.get)
    
    checkpoints = {vertice: random.randint(3, 10) * -1 for vertice in T.nodes() if vertice not in [start_node, end_node] and T.degree(vertice) == 1}

    T = nx.DiGraph(T)

    for (u, v) in T.edges():
        # Se o destino da aresta for um checkpoint
        if v in checkpoints.keys():
            T.edges[u, v]["weight"] = checkpoints[v]
        else:
            T.edges[u, v]["weight"] = 1


    return Labirinto(T, (n_linhas, n_colunas), start_node, end_node, checkpoints)
    
# Funcao ainda em construcao
def solucionar_labirinto(labirinto: Labirinto) -> Tuple[int, List[Tuple[int, int]]]:
    solucoes = []

    distancias = nx.single_source_shortest_path(labirinto.grafo, labirinto.origem)

    VERTICE_INICIO = 1
    solucoes.append((len(distancias[labirinto.chegada]) - VERTICE_INICIO, distancias[labirinto.chegada]))

    for v in labirinto.checkpoints.keys():
        novos_checkpoints = labirinto.checkpoints.copy()
        del novos_checkpoints[v]

        novo_labirinto = Labirinto(
            labirinto.grafo,
            labirinto.dimensoes,
            v,
            labirinto.chegada,
            novos_checkpoints
        )

        custo_minimo, caminho = solucionar_labirinto(novo_labirinto) 

        VERTICE_INICIO = 1
        VERTICE_CHECKPOINT = 1
        solucoes.append((custo_minimo + labirinto.checkpoints[v] + len(distancias[v]) - VERTICE_INICIO - VERTICE_CHECKPOINT, distancias[v] + caminho[1:]))

    solucao_otima = sorted(solucoes)[0]
    custo, caminho = solucao_otima

    print(custo, caminho)

    return solucao_otima

if __name__ == "__main__":
    labirinto = criar_labirinto(3, 3)
    custo, caminho = solucionar_labirinto(labirinto)

    # print(labirinto.origem, labirinto.chegada)
    print(labirinto.checkpoints)
    # for u, v in labirinto.grafo.edges():
        # print(f"{u} -> {v}")
        

    print(custo, caminho)



