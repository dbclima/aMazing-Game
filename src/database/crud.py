import json
import networkx as nx
from labirinto import Labirinto
from labirinto import criar_labirinto
from labirinto import Dificuldade

def saveLab(L: Labirinto):
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
    labirinto["vida inicial"] = L.vida_inicial
    labirinto["dificuldade"] = L.dificuldade.value
    
    with open("fases.json", "r") as arquivo:
        antigo = json.load(arquivo)
        antigo[L.id] = labirinto
    
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
    
    if labirinto["dificuldade"] == 1:
        dificuldade = Dificuldade.DIFICIL
    else:
        dificuldade = Dificuldade.FACIL
    
    vida_inicial = labirinto["vida inicial"]
    arestas = []
    aux_arestas = labirinto["arestas"]
    for i, j in aux_arestas:
        arestas.append((tuple(i), tuple(j)))
    
    grafo = nx.Graph()
    for i, j in arestas:
        grafo.add_edge(i, j)
    return Labirinto(id, grafo, dimensoes, origem, chegada, checkpoints, vida_inicial, dificuldade)

def saveStats(id: int, username: str, score: int, time: float):
    stats = {}
    
    stats["score"] = score
    stats["time"] = time
    
    id_str = str(id)
    with open("leaderboard.json", "r") as arquivo:
        antigo = json.load(arquivo)
        if id_str not in antigo.keys():
            antigo[id_str] = dict()
        antigo[id_str][username] = stats
    
    with open("leaderboard.json", "w") as arquivo:
        json.dump(antigo, arquivo)

def getStats(id: int):
    id_str = str(id)
    
    with open("leaderboard.json", "r") as arquivo:
        antigo = json.load(arquivo)
        leaderboard = antigo[id_str]
    
    leaderboard_ordenado = sorted(leaderboard.items(), key=lambda x: (-x[1]["score"], x[1]["time"]))
    output = leaderboard_ordenado
    if len(leaderboard_ordenado) >10:
        output = leaderboard_ordenado[:10]

    return output

if __name__ == "__main__":
    #saveStats(0, "didi", 20, 10.5)
    #saveStats(0, "tonhao", 20, 14)
    #saveStats(0, "giovanna", 25, 20)
    #saveStats(0, "joao", 12, 19)
    #saveStats(0, "arrasca", 33, 200)
    #saveStats(0, "mann", 33, 199.9)
    #saveStats(0, "bh", 25, 20.9)
    #saveStats(0, "ortiz", 19, 23)
    #saveStats(0, "gabigol", 19, 99)
    #saveStats(0, "er", 19, 7)
    #saveStats(0, "fili", 19, 16)
    #saveStats(0, "ana", 200, 21)
    #saveStats(1, "didi", 10, 12)
    print(getStats(0))