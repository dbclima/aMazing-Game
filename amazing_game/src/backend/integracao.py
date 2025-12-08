from .labirinto import Labirinto, criar_labirinto
from typing import Tuple, List, Dict, Optional

def transforma_labirinto_para_json_front(labirinto:Labirinto) -> Dict:
  
    dicionario_frontend = dict()

    dicionario_frontend["nivel"] = labirinto.id
    dicionario_frontend["linhas"] = labirinto.dimensoes[0]
    dicionario_frontend["colunas"] = labirinto.dimensoes[1]
    dicionario_frontend["origem"] = list(labirinto.origem)
    dicionario_frontend["chegada"] = list(labirinto.chegada)
    dicionario_frontend["vidaInicial"] = -labirinto.vida_inicial    
    dicionario_frontend["checkpoints"] = [{"pos": key, "bonus": valor} for key, valor in labirinto.checkpoints.items()]
    dicionario_frontend["arestas"] = [{"de": key, "para": valor, "peso": - labirinto.grafo.edges[key,valor]["weight"]} for key,valor in labirinto.grafo.edges()]

    return dicionario_frontend 

if __name__ == "__main__":
    l = criar_labirinto(1, 4, 4)
    print(transforma_labirinto_para_json_front(l))