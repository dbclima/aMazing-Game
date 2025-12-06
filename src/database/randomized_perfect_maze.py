import networkx as nx
import matplotlib.pyplot as plt
import random


### Geração de labirinto

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

if __name__ == "__main__":
    # Definindo o grafo grid a partir do qual produziremos o labirinto
    m, n = [5, 4]
    G = nx.grid_graph([m, n])

    MST_algorithm = 'kruskal'
    T = create_perfect_maze_from_MST(G, MST_algorithm)

    pos_grid = dict((n, n) for n in G.nodes()) # Usa a posição na grid como layout
    pos_spring = nx.spring_layout(G)
    edge_labels = nx.get_edge_attributes(G, 'weight')

    # Mostrando os resultados
    plt.figure(figsize=(15, 5))
    plt.subplot(131)
    nx.draw(G, pos_grid, with_labels=True, node_color='skyblue', node_size=500, edge_color='gray', font_size=9)
    nx.draw_networkx_edge_labels(G, pos_grid, edge_labels=edge_labels, font_color='red', font_size=9)
    plt.title("G - Original Graph (random weights)\n")

    plt.subplot(132)
    nx.draw(T, pos_grid, with_labels=True, node_color='skyblue', node_size=500, edge_color='black', font_size=9)
    plt.title("T - Random Spanning Tree ("+MST_algorithm+")\n (Random Maze)")

    edges_to_remove = T.edges()
    M = G.copy()
    M.remove_edges_from(edges_to_remove)

    plt.subplot(133)
    nx.draw(M, pos_grid, with_labels=False, node_color='skyblue', node_size=500, edge_color='black')
    plt.title("G-T\n (Maze walls)")

    plt.show()



    ### Definindo os vértices de início e fim do labirinto, ou seja, os mais distantes entre si
    center_node = list(T.nodes())[0]
    distances = nx.single_source_shortest_path_length(T, center_node)
    print(distances)

    start_node = max(distances, key=distances.get)
    print(max(distances, key=distances.get), distances[start_node])

    distances = nx.single_source_shortest_path_length(T, start_node)
    print(distances)
    end_node = max(distances, key=distances.get)
    print(max(distances, key=distances.get), distances[end_node])

    # Assign 'color' attribute to specific nodes
    T.nodes[start_node]['color'] = 'yellow'
    T.nodes[end_node]['color'] = 'lightgreen'

    # Create a list of colors for all nodes, defaulting to a color if not specified
    node_colors = [T.nodes[node].get('color', 'skyblue') for node in T.nodes()]

    plt.figure(figsize=(5, 5))
    plt.title(f"Maze with start and end nodes defined\nStart: {start_node}, End: {end_node}")
    nx.draw(T, pos_grid, with_labels=True, node_color=node_colors, node_size=500, edge_color='black', font_size=9)

    plt.show()



    ### Definindo os custos de cada aresta para o jogo
    maze = T.copy()

    # start, end = (0,0), (n-1,m-1)
    # talvez seja mais interessante se o start e end nodes sejam os nós folha
    # mais distantes entre si, o que pode ser descoberto fazendo BFS

    start, end = start_node, end_node
    # start e end nodes definidos como os mais distantes entre si no labirinto

    V = list(maze.nodes())
    E = list(maze.edges())
    checkpoint_nodes = [node for node in V if node not in [start, end] and maze.degree(node)==1]
    # checkpoint nodes são todos os nós folha da árvore geradora, exceto os de start e end.
    # Podemos vê-los também como o final de becos sem saída do labirinto

    print("V:")
    print(V)
    print("Checkpoint nodes:")
    print(checkpoint_nodes)

    for u, v in maze.edges():
      if(v in checkpoint_nodes or u in checkpoint_nodes):
        maze.edges[u, v]['weight'] = +3
        # definir isso de forma automatizada colocando pesos (recompensas de vida)
        # que façam o jogador questionar se vale a pena ou não entrar em algum
        # checkpoint (beco sem saída) para aumentar sua pontuação de vida
      else:
        maze.edges[u, v]['weight'] = -1


    maze_edge_labels = nx.get_edge_attributes(maze, 'weight')

    # Plotando labirinto
    plt.figure(figsize=(5, 5))
    plt.title(f"Maze with game weights\nStart: {start}, End: {end}")
    nx.draw(nx.DiGraph(maze), pos_grid, with_labels=True, node_color=node_colors, node_size=500, edge_color='gray', font_size=9)
    nx.draw_networkx_edge_labels(maze, pos_grid, edge_labels=maze_edge_labels, font_color='red', font_size=9)

    plt.show()

