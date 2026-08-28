"""
Autor: Alexandre Augusto Angelo de Souza
Data: 18/07/2026
-------
Representa o tabuleiro (labirinto) usado no projeto de comparação de
algoritmos de busca (BFS, DFS e A*).

"""

from __future__ import annotations

import random
from collections import deque
from dataclasses import dataclass, field
from typing import List, Tuple

Coord = Tuple[int, int]  # (linha, coluna)

LIVRE = 0
PAREDE = 1


@dataclass
class Maze:
    """Representa o tabuleiro como uma matriz de 0 (livre) e 1 (parede)."""

    linhas: int
    colunas: int
    inicio: Coord
    objetivo: Coord
    grade: List[List[int]] = field(default_factory=list)

    def eh_valida(self, celula: Coord) -> bool:
        """Verifica se a célula está dentro dos limites do tabuleiro."""
        r, c = celula
        return 0 <= r < self.linhas and 0 <= c < self.colunas

    def eh_livre(self, celula: Coord) -> bool:
        """Verifica se a célula está dentro do tabuleiro e não é parede."""
        if not self.eh_valida(celula):
            return False
        r, c = celula
        return self.grade[r][c] == LIVRE

    def vizinhos(self, celula: Coord) -> List[Coord]:
        """
        Retorna a lista de células vizinhas válidas (livres) de `celula`,
        considerando movimentos nas 4 direções (cima, baixo, esquerda,
        direita). Use este método dentro dos seus algoritmos de busca.
        """
        r, c = celula
        candidatos = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
        return [pos for pos in candidatos if self.eh_livre(pos)]


def _tabuleiro_soluvel(grade: List[List[int]], inicio: Coord, objetivo: Coord) -> bool:
    """
    Verificação interna (usada apenas na geração do labirinto) de que
    existe um caminho entre início e objetivo. Isso NÃO é o algoritmo de
    busca do trabalho — é só uma checagem de sanidade para não gerarmos
    labirintos impossíveis de resolver.
    """
    linhas, colunas = len(grade), len(grade[0])
    visitados = {inicio}
    fila = deque([inicio])
    while fila:
        r, c = fila.popleft()
        if (r, c) == objetivo:
            return True
        for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
            if (
                0 <= nr < linhas
                and 0 <= nc < colunas
                and grade[nr][nc] == LIVRE
                and (nr, nc) not in visitados
            ):
                visitados.add((nr, nc))
                fila.append((nr, nc))
    return False


def gerar_labirinto(
    linhas: int = 15,
    colunas: int = 15,
    densidade_paredes: float = 0.28,
    inicio: Coord = (0, 0),
    objetivo: Coord | None = None,
    semente: int | None = None,
) -> Maze:
    """
    Gera um labirinto aleatório `linhas` x `colunas` com aproximadamente
    `densidade_paredes` da área ocupada por obstáculos, garantindo que
    exista pelo menos um caminho entre `inicio` e `objetivo`.

    Tenta várias vezes até encontrar uma configuração solúvel.
    """
    if objetivo is None:
        objetivo = (linhas - 1, colunas - 1)

    rng = random.Random(semente)

    for _ in range(200):  # tenta até 200 vezes gerar um labirinto válido
        grade = [
            [PAREDE if rng.random() < densidade_paredes else LIVRE for _ in range(colunas)]
            for _ in range(linhas)
        ]
        grade[inicio[0]][inicio[1]] = LIVRE
        grade[objetivo[0]][objetivo[1]] = LIVRE

        if _tabuleiro_soluvel(grade, inicio, objetivo):
            return Maze(linhas=linhas, colunas=colunas, inicio=inicio, objetivo=objetivo, grade=grade)

    # fallback: labirinto vazio (sem obstáculos), sempre solúvel
    grade = [[LIVRE for _ in range(colunas)] for _ in range(linhas)]
    return Maze(linhas=linhas, colunas=colunas, inicio=inicio, objetivo=objetivo, grade=grade)
