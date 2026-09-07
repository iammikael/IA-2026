"""
Autor: Alexandre Augusto Angelo de Souza
Data: 18/07/2026

Recomendações:

Pessoal, aqui é onde vocês vão trabalhar e incluir o código de vocês

Implementem os três algoritmos de busca abaixo:

  * bfs(maze)    -> Busca em Largura   (Breadth-First Search)
  * dfs(maze)    -> Busca em Profundidade (Depth-First Search)
  * astar(maze)  -> Busca A* (A-estrela)

Todos recebem um objeto `Maze` (veja maze.py) e devem devolver um objeto
`SearchResult` (definido abaixo) com o resultado da busca. USE ISSO, OK?


Cada célula é representada como uma tupla (linha, coluna). Use
`maze.inicio`, `maze.objetivo` e `maze.vizinhos(celula)` para navegar
pelo tabuleiro — vocês NÃO precisam mexer em maze.py.

Dica geral de implementação (para qualquer um dos 3 algoritmos):
  1. Mantenha uma estrutura de "fronteira" (fila para BFS, pilha/recursão
     para DFS, fila de prioridade para A*) com as células a explorar.
  2. Mantenha um dicionário `veio_de` (came_from) que, para cada célula
     visitada, guarda de qual célula ela foi alcançada. Isso é usado no
     final para reconstruir o caminho com `reconstruir_caminho`.
  3. Mantenha um conjunto/dicionário de células já visitadas para não
     processar a mesma célula duas vezes.
  4. Registre, na ordem em que forem exploradas (removidas da fronteira
     para processamento), as células em `explorados` — isso é usado só
     para desenhar a animação na tela, não influencia a lógica da busca.
  5. Ao encontrar o objetivo, pare e reconstrua o caminho.
"""

from __future__ import annotations

import time
import heapq
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from maze import Coord, Maze
from collections import deque


@dataclass
class SearchResult:
    """Resultado de uma busca, usado pela interface para desenhar a tela."""

    encontrado: bool                 # True se um caminho até o objetivo foi achado
    caminho: List[Coord]             # sequência de células do início ao objetivo (inclusive)
    explorados: List[Coord]          # células visitadas, na ordem em que foram exploradas
    expandidos: int                  # quantidade de células expandidas (nós processados)
    tempo: float                     # tempo de execução em segundos


def reconstruir_caminho(veio_de: Dict[Coord, Coord], inicio: Coord, objetivo: Coord) -> List[Coord]:
    """
    Função utilitária (já pronta) que reconstrói o caminho do `inicio`
    até o `objetivo` a partir do dicionário `veio_de`, onde
    `veio_de[celula]` é a célula anterior no caminho encontrado.

    Vocês podem usar esta função nos três algoritmos. ALiás, USEM!!!!
    """
    caminho = [objetivo]
    atual = objetivo
    while atual != inicio:
        atual = veio_de[atual]
        caminho.append(atual)
    caminho.reverse()
    return caminho


def heuristica(a: Coord, b: Coord) -> int:
    """
    Heurística usada pelo A*: distância de Manhattan entre duas células.
    Já está pronta, vocês podem usá-la diretamente em `astar`.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# ---------------------------------------------------------------------------
# 1) BUSCA EM LARGURA (BFS)
# ---------------------------------------------------------------------------
def bfs(maze: Maze) -> SearchResult:
   
    inicio_tempo = time.perf_counter()

    fila       =deque([maze.inicio])
    visto      ={maze.inicio}
    veio_de    ={}
    explorados =[]

    while fila:
        atual = fila.popleft()
        explorados.append(atual)

        if atual == maze.objetivo:

            tempo_final = time.perf_counter() - inicio_tempo

            caminho = reconstruir_caminho(
                veio_de,
                maze.inicio,
                maze.objetivo
            )

            return SearchResult(
                encontrado=True,                 
                caminho=caminho,             
                explorados=explorados,          
                expandidos=len(explorados),      
                tempo=tempo_final
            )
        
        for vizinho in maze.vizinhos(atual):
            if vizinho not in visto:
                visto.add(vizinho)
                veio_de[vizinho]=atual 
                fila.append(vizinho)

    tempo_final = time.perf_counter() - inicio_tempo            

    return SearchResult(
        encontrado=False,                 
        caminho=[],             
        explorado=explorados,          
        expandidos=len(explorados),      
        tempo=tempo_final 
    )

# ---------------------------------------------------------------------------
# 2) BUSCA EM PROFUNDIDADE (DFS)
# ---------------------------------------------------------------------------
def dfs(maze: Maze) -> SearchResult:
    """
    TODO: Implementar a Busca em Profundidade (DFS).

    Estrutura de dados sugerida: pilha (lista Python com append/pop),
    processando sempre a última célula inserida (LIFO).

    Diferente do BFS, o DFS NÃO garante o caminho mais curto — ele
    "mergulha" por um caminho até não poder mais avançar antes de
    voltar (backtrack).
    """
    inicio_tempo = time.perf_counter()

    pilha      =[maze.inicio]
    visto      ={maze.inicio}
    veio_de    ={}
    explorados =[]

    while pilha:
        atual = pilha.pop()
        explorados.append(atual)

        if atual == maze.objetivo:
 
            tempo_final = time.perf_counter() - inicio_tempo

            caminho = reconstruir_caminho(
                veio_de,
                maze.inicio,
                maze.objetivo
            )

            return SearchResult(
                encontrado=True,                 
                caminho=caminho,             
                explorados=explorados,          
                expandidos=len(explorados),      
                tempo=tempo_final 
            )

        for vizinho in maze.vizinhos(atual):
            if vizinho not in visto:
                visto.add(vizinho)
                veio_de[vizinho] = atual
                pilha.append(vizinho)

    tempo_final = time.perf_counter() - inicio_tempo

    return SearchResult(
            encontrado=False,                 
            caminho=caminho,             
            explorados=explorados,          
            expandidos=len(explorados),      
            tempo=tempo_final 
        )
# ---------------------------------------------------------------------------
# 3) BUSCA A* (A-ESTRELA)
# ---------------------------------------------------------------------------
def astar(maze: Maze) -> SearchResult:
    """
    TODO: Implementar a Busca A*.

    Estrutura de dados sugerida: fila de prioridade (heapq), ordenada
    por f(n) = g(n) + h(n), onde:
      * g(n) = custo do caminho do início até n (número de passos);
      * h(n) = heuristica(n, maze.objetivo)  (já implementada acima).

    Dica: como o heapq não permite comparar tuplas com Coord "empatadas"
    facilmente, uma boa prática é inserir na fila tuplas do tipo
    (f, contador, celula), onde `contador` é um número que só aumenta
    (para desempatar sem comparar as células diretamente).
    """
    inicio_tempo = time.perf_counter()


    heap       =[(0+heuristica(maze.inicio, maze.objetivo), 0, maze.inicio,[maze.inicio])]
    explorados =[]
    custo_g    ={maze.inicio: 0}
    veio_de    ={}

    while heap:
        f, g, atual, caminho = heapq.heappop(heap)
        explorados.append(atual)

        if atual == maze.objetivo:

            tempo_final = time.perf_counter() - inicio_tempo

            caminho = reconstruir_caminho(
                veio_de,
                maze.inicio,
                maze.objetivo
            )

            return SearchResult(
                encontrado=True,                 
                caminho=caminho,             
                explorados=explorados,          
                expandidos=len(explorados),      
                tempo=tempo_final 
            )

        for vizinho in maze.vizinhos(atual):

            novo_g = g + 1

            if vizinho not in custo_g or novo_g < custo_g[vizinho]:
                custo_g[vizinho] = novo_g
                veio_de[vizinho]= atual
                h = heuristica(vizinho, maze.objetivo)
                f = novo_g + h 
                heapq.heappush(heap,(f, novo_g, vizinho, caminho + [vizinho]))

    tempo_final = time.perf_counter() - inicio_tempo
     
    return SearchResult(
            encontrado=True,                 
            caminho=caminho,             
            explorados=explorados,          
            expandidos=len(explorados),      
            tempo=tempo_final 
            )
# Mapa usado pela interface para associar o texto do dropdown à função
ALGORITMOS = {
    "BFS": bfs,
    "DFS": dfs,
    "A*": astar,
}
