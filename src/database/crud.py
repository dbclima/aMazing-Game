import json
import networkx as nx
from labirinto import Labirinto
from labirinto import criar_labirinto

def saveLab(L: Labirinto, id: int):
    labirinto = {}
    arestas = []
    for i, j in L.grafo.edges:
        arestas.append([list(i), list(j)])
    
    dimensoes = list(L.dimensoes)
    origem = list(L.origem)
    chegada = list(L.chegada)
    checkpoints = {}

    for i in L.checkpoints.keys():
        checkpoints[",".join(map(str, i))] = L.checkpoints[i]
    
    labirinto["arestas"] = arestas
    labirinto["dimensoes"] = dimensoes
    labirinto["origem"] = origem
    labirinto["chegada"] = chegada
    labirinto["checkpoints"] = checkpoints
    
    with open("fases.json", "r") as arquivo:
        antigo = json.load(arquivo)
        antigo[id] = labirinto
    
    with open("fases.json", "w") as arquivo:
        json.dump(antigo, arquivo)

def loadLab(id: int):
    with open("fases.json", "r") as arquivo:
        antigo = json.load(arquivo)
        labirinto = antigo[id]
    
    dimensoes = tuple(labirinto["dimensoes"])
    origem = tuple(labirinto["origem"])
    chegada = tuple(labirinto["chegada"])
    checkpoints = {}
    aux_check = labirinto["checkpoints"]
    for i in aux_check.keys():
        checkpoints[tuple(map(int, i.split(",")))] = aux_check[i]
    
    arestas = []
    aux_arestas = labirinto["arestas"]
    for i, j in aux_arestas:
        arestas.append((tuple(i), tuple(j)))
    
    grafo = nx.Graph()
    for i, j in arestas:
        grafo.add_edge(i, j)
    return Labirinto(grafo, dimensoes, origem, chegada, checkpoints)


if __name__ == "__main__":
    lab = criar_labirinto(3, 3)
    saveLab(lab, 0)
    print(lab)
    lab1 = loadLab("0")
    print(lab1)
    