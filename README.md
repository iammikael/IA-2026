# Maze Solver — Comparação de Algoritmos de Busca

Projeto-base (esqueleto) para o trabalho de Inteligência Artificial:
implementação e comparação dos algoritmos **BFS**, **DFS** e **A\*** na
resolução de um labirinto.

## Como executar

```bash
pip install -r requirements.txt
python main.py
```

Uma janela deve abrir com:

- um **tabuleiro** (labirinto gerado aleatoriamente), com o ponto de
  início em **verde** (canto superior esquerdo) e o objetivo em
  **vermelho/rosa**; obstáculos em **preto** e células livres em cinza;
- um **dropdown** para escolher o algoritmo: `BFS`, `DFS` ou `A*`;
- um botão **Executar**, que roda o algoritmo escolhido sobre o
  labirinto atual;
- um botão **Novo Labirinto**, que gera um novo tabuleiro aleatório;
- uma linha de **estatísticas** (tamanho do caminho, nós expandidos e
  tempo de execução) e uma **legenda** de cores.

Ao clicar em **Executar** antes de implementar os algoritmos, a
aplicação mostra a mensagem `Algoritmo ainda não implementado` — isso é
esperado. Assim que vocês implementarem cada função, o resultado passa
a ser desenhado no tabuleiro (células exploradas em azul e o caminho
final em areia/laranja).

## Estrutura do projeto

```
maze_solver/
├── main.py         # Ponto de entrada: janela, loop principal, eventos (PRONTO)
├── ui.py           # Cores, botão, dropdown e desenho do tabuleiro (PRONTO)
├── maze.py         # Representação e geração do labirinto (PRONTO)
├── algorithms.py   # <<< AQUI vocês vão implementar BFS, DFS e A* >>>
└── requirements.txt
```

**Só é necessário editar `algorithms.py`.** Os demais arquivos já
contêm toda a estrutura de janela, tabuleiro e interface pronta.

## O que vocês vão implementar (próxima etapa)

Em `algorithms.py` há três funções, cada uma recebendo um objeto
`Maze` e devendo devolver um `SearchResult`:

```python
def bfs(maze: Maze) -> SearchResult: ...
def dfs(maze: Maze) -> SearchResult: ...
def astar(maze: Maze) -> SearchResult: ...
```

`SearchResult` tem os campos:

| Campo         | Descrição                                                  |
|---------------|--------------------------------------------------------------|
| `encontrado`  | `True`/`False` — se um caminho até o objetivo foi encontrado |
| `caminho`     | Lista de células `(linha, coluna)` do início ao objetivo      |
| `explorados`  | Lista de células visitadas, na ordem em que foram exploradas  |
| `expandidos`  | Quantidade de nós expandidos durante a busca                  |
| `tempo`       | Tempo de execução em segundos                                 |

Ferramentas já prontas para usar dentro dos algoritmos:

- `maze.inicio`, `maze.objetivo` — coordenadas de início e fim;
- `maze.vizinhos(celula)` — devolve os vizinhos válidos (livres) de uma célula;
- `reconstruir_caminho(veio_de, inicio, objetivo)` — reconstrói o
  caminho a partir de um dicionário de predecessores;
- `heuristica(a, b)` — distância de Manhattan, para uso no A*.

Cada função contém, em seus comentários, um roteiro/pseudocódigo
sugerido para a implementação.

## Sobre a comparação entre algoritmos

Nesta primeira entrega, o projeto mostra **um único tabuleiro** com
**um único dropdown**, para focar na implementação correta de cada
algoritmo isoladamente. Numa etapa seguinte, vocês vão evoluir este
projeto para comparar dois algoritmos lado a lado (como no exemplo de
referência), reaproveitando as mesmas funções de `algorithms.py`.

## Requisitos

- Python 3.10+
- pygame (`pip install pygame`)
