from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass

@dataclass
class Vertice:
    linha: int
    coluna: int

@dataclass
class Grafo:
    dimensoes: Tuple[int, int]
    lista_vertices: List[Vertice]
    hash_adjacencias: Dict[Vertice, Dict[Vertice, int]]

    def at(self, i: int, j: int) -> Vertice:
        n_linhas, n_colunas = self.dimensoes
        assert i < n_linhas and j < n_colunas

        return self.lista_vertices[i * n_colunas + j]
    
    def w(self, v_origem: Vertice, v_destino: Vertice) -> Optional[int]:
        try:
            return self.hash_adjacencias[v_origem][v_destino]
        
        except KeyError:
            return None


class MazeFactory:
    def __init__(self):
        raise PermissionError("Impossível inicializar objeto de classe factory")
    
    @classmethod
    def create(cls, n_linhas: int, n_colunas: int) -> Grafo:
        lista_adjacencias = list()

        for i in range(n_linhas):
            for j in range(n_colunas):
                lista_adjacencias.apppend(list())
            


if __name__ == "__main__":
    pass