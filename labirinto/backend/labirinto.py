import random
from dataclasses import dataclass
from typing import Tuple, List, Dict, Optional
from enum import Enum, auto

import networkx as nx

from randomized_perfect_maze import create_perfect_maze_from_MST

class Dificuldade(Enum):
    FACIL = auto()
    DIFICIL = auto()

@dataclass
class Labirinto:
    id: int
    grafo: nx.Graph
    dimensoes: Tuple[int, int]
    origem: Tuple[int, int]
    chegada: Tuple[int, int]
    checkpoints: Dict[Tuple[int, int], int]
    vida_inicial: int
    dificuldade: Dificuldade

def preencher_checkpoints(T: nx.Graph, checkpoints: Dict[Tuple[int, int], Optional[int]], no_inicio: Tuple[int, int], no_final: Tuple[int, int]) -> None:
    NO_COMUM = 1
    IDA_E_VOLTA = 2

    distancias = nx.single_source_shortest_path(T, no_inicio)
    caminho_trivial = distancias[no_final]

    for vertice in checkpoints.keys():
        n_passos_comuns = 0
        caminho_vertice = distancias[vertice]
        for no_trivial, no_desvio in zip(caminho_trivial, caminho_vertice):
            if no_trivial[0] != no_desvio[0] or no_trivial[1] != no_desvio[1]:
                break
            n_passos_comuns += 1

        n_passos_extra = len(caminho_vertice) - n_passos_comuns
        vida_neutra = n_passos_extra * IDA_E_VOLTA - NO_COMUM

        # Impedimos a possibilidade do checkpoint ser positivo ou nulo
        checkpoints[vertice] = - max(1, vida_neutra + random.randint(-1, 3))
        # checkpoints[vertice] = - vida_neutra - 1

    return None

# Funcao ainda em construcao
def solucionar_labirinto(labirinto: Labirinto) -> Tuple[int, List[Tuple[int, int]]]:
    """"""
    solucoes = []

    distancias = nx.single_source_shortest_path(labirinto.grafo, labirinto.origem)

    VERTICE_INICIO = 1
    solucoes.append((len(distancias[labirinto.chegada]) - VERTICE_INICIO, distancias[labirinto.chegada]))

    for v in labirinto.checkpoints.keys():
        novos_checkpoints = labirinto.checkpoints.copy()
        del novos_checkpoints[v]

        novo_labirinto = Labirinto(
            labirinto.id,
            labirinto.grafo,
            labirinto.dimensoes,
            v,
            labirinto.chegada,
            novos_checkpoints,
            0,
            labirinto.dificuldade
        )

        custo_minimo, caminho = solucionar_labirinto(novo_labirinto) 

        VERTICE_INICIO = 1
        VERTICE_CHECKPOINT = 1
        solucoes.append((custo_minimo + labirinto.checkpoints[v] + len(distancias[v]) - VERTICE_INICIO - VERTICE_CHECKPOINT, distancias[v] + caminho[1:]))

    solucao_otima, caminho_otimo = sorted(solucoes)[0]

    return solucao_otima + labirinto.vida_inicial, caminho_otimo

def criar_labirinto(id: int, n_linhas: int, n_colunas: int, algoritmo="kruskal", maximo_checkpoints=5, dificuldade=Dificuldade.FACIL) -> Labirinto:
    G = nx.grid_graph((n_linhas, n_colunas))
    
    T = create_perfect_maze_from_MST(G, algoritmo)

    center_node = list(T.nodes())[0]
    distances = nx.single_source_shortest_path_length(T, center_node)

    start_node = max(distances, key=distances.get)
    distances = nx.single_source_shortest_path_length(T, start_node)

    end_node = max(distances, key=distances.get)
    
    checkpoints = {vertice: None for vertice in T.nodes() if vertice not in [start_node, end_node] and T.degree(vertice) == 1}

    preencher_checkpoints(T, checkpoints, start_node, end_node)

    while len(checkpoints.keys()) > maximo_checkpoints:
        lista_checkpoints = list(checkpoints.keys())
        del checkpoints[lista_checkpoints[random.randint(0, len(lista_checkpoints) - 1)]]

    T = nx.DiGraph(T)

    for (u, v) in T.edges():
        # Se o destino da aresta for um checkpoint
        if v in checkpoints.keys():
            T.edges[u, v]["weight"] = checkpoints[v]
        else:
            T.edges[u, v]["weight"] = 1

    labirinto = Labirinto(id, T, (n_linhas, n_colunas), start_node, end_node, checkpoints, 0, dificuldade)

    if dificuldade == Dificuldade.FACIL:
        vida_trivial = distances[end_node]
        labirinto.vida_inicial = - vida_trivial

    elif dificuldade == Dificuldade.DIFICIL:
        _, caminho = solucionar_labirinto(labirinto)
        custo = 0
        menor_vida = 0
        for vertice in caminho[1:-1]:
            if vertice in checkpoints.keys():
                custo += (- checkpoints[vertice]) + 1

            custo -= 1
            if custo < menor_vida:
                menor_vida = custo

        vida_dificil = - abs(menor_vida - 1)
        labirinto.vida_inicial = vida_dificil

    else:
        raise TypeError

    return labirinto
    

if __name__ == "__main__":
    labirinto = criar_labirinto(0, 3, 3, maximo_checkpoints=8, dificuldade=Dificuldade.DIFICIL)
    custo, caminho = solucionar_labirinto(labirinto)

    for u,v in labirinto.grafo.edges():
        print(labirinto.grafo.edges[u,v]["weight"])
    # print(labirinto.origem, labirinto.chegada)
    # print(labirinto.checkpoints)
    # print(labirinto.vida_inicial)
    # for u, v in labirinto.grafo.edges():
        # print(f"{u} -> {v}")
        

    # print(custo - 1, caminho)



