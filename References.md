## Referências

- networkx vs igraph
  https://dev.to/whoakarsh/comparing-dijkstras-algorithm-in-igraph-vs-networkx-which-one-should-you-use-4d82

- Python Graph Libraries
  https://wiki.python.org/moin/PythonGraphLibraries

- Maze Generation Algorithms - An Exploration 
  https://professor-l.github.io/mazes/


Definição de Labirintos "Perfeitos":
'Labirintos sem laços são conhecidos como labirintos "simplesmente conectados" ou "perfeitos" e são equivalentes a uma árvore na teoria dos grafos.'
 (https://en.wikipedia.org/wiki/Maze-solving_algorithm)

 Isso implica que como não há loops, pelo fato de labirintos "perfeitos" serem árvores, podemos considerar usar o Algoritmo de Bellman-Ford para resolver o problema, já que este lida com pesos negativos.

