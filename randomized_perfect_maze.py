import networkx as nx
import matplotlib.pyplot as plt
import random


def create_perfect_maze_from_MST(G, algorithm):
    """
    Cria grafo com pesos aleatórios para consequentemente, ao produzir a 
    árvore geradora mínima por Kruskal/Prim/Boruvka, produzir um labirinto 
    perfeito (sem ciclos).
    """
    for u, v in G.edges():
        G.edges[u, v]['weight'] = round(random.uniform(1.0, 10.0), 1)

    random_tree = nx.minimum_spanning_tree(G, algorithm=algorithm)
    
    return random_tree


# Definindo o grafo grid a partir do qual produziremos o labirinto
maze_shape = [4, 4]
G = nx.grid_graph(maze_shape)

MST_algorithm = 'kruskal'
T = create_perfect_maze_from_MST(G, MST_algorithm)

pos = dict((n, n) for n in G.nodes()) # Usa a posição na grid como layout
edge_labels = nx.get_edge_attributes(G, 'weight')

# Mostrando os resultados
plt.figure(figsize=(15, 5))
plt.subplot(131)
nx.draw(G, pos, with_labels=False, node_color='skyblue', node_size=500, edge_color='gray')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
plt.title("G - Original Graph (random weights)\n")

plt.subplot(132)
nx.draw(T, pos, with_labels=False, node_color='skyblue', node_size=500, edge_color='black')
plt.title("T - Random Spanning Tree ("+MST_algorithm+")\n (Random Maze)")

edges_to_remove = T.edges()
M = G.copy()
M.remove_edges_from(edges_to_remove)

plt.subplot(133)
nx.draw(M, pos, with_labels=False, node_color='skyblue', node_size=500, edge_color='black')
plt.title("G-T\n (Maze walls)")
plt.show()

