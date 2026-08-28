"""
Autor: Alexandre Augusto Angelo de Souza
Data: 18/07/2026

-------

Este arquivo já está PRONTO — não é necessário alterar nada aqui para
a primeira entrega. Vocês só precisam implementar as funções `bfs`,
`dfs` e `astar` em algorithms.py.

Para rodar:
    pip install -r requirements.txt
    python main.py
"""

from __future__ import annotations

import sys

import pygame

from algorithms import ALGORITMOS, SearchResult
from maze import gerar_labirinto
import ui

# ---------------------------------------------------------------------------
# Configurações gerais
# ---------------------------------------------------------------------------
LINHAS, COLUNAS = 15, 15
TAMANHO_CELULA = 30
DENSIDADE_PAREDES = 0.28

MARGEM = 20
TOPO_BARRA_ALTURA = 60
LEGENDA_ALTURA = 40
STATS_ALTURA = 30

GRID_LARGURA = COLUNAS * TAMANHO_CELULA
GRID_ALTURA = LINHAS * TAMANHO_CELULA

LARGURA_JANELA = GRID_LARGURA + 2 * MARGEM
ALTURA_JANELA = TOPO_BARRA_ALTURA + GRID_ALTURA + STATS_ALTURA + LEGENDA_ALTURA + MARGEM

# Passos de animação por frame (quantas células "revelar" por frame).
# Ajuste para deixar a animação mais rápida/lenta, ou defina ANIMAR = False
# para mostrar o resultado direto, sem animação.
ANIMAR = True
CELULAS_POR_FRAME = 6


class Aplicacao:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Maze Solver — Comparação de Algoritmos de Busca")
        self.tela = pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA))
        self.relogio = pygame.time.Clock()

        self.fonte = pygame.font.SysFont("segoeui", 16)
        self.fonte_pequena = pygame.font.SysFont("segoeui", 13)
        self.fonte_titulo = pygame.font.SysFont("segoeui", 20, bold=True)

        self.maze = gerar_labirinto(LINHAS, COLUNAS, DENSIDADE_PAREDES)

        self.resultado: SearchResult | None = None
        self.erro: str | None = None
        self.revelados = 0  # quantas células já foram "reveladas" na animação

        # --- elementos de UI -------------------------------------------------
        dropdown_x = MARGEM + 90
        self.dropdown = ui.Dropdown(
            rect=(dropdown_x, 16, 110, 28),
            opcoes=list(ALGORITMOS.keys()),
            selecionado="BFS",
        )

        botao_executar_x = dropdown_x + 120
        self.botao_executar = ui.Botao(
            rect=(botao_executar_x, 16, 100, 28),
            texto="Executar",
            ao_clicar=self.executar_algoritmo,
            cor=ui.COR_BOTAO_DESTAQUE,
            cor_hover=ui.COR_BOTAO_DESTAQUE_HOVER,
        )

        botao_novo_x = botao_executar_x + 110
        self.botao_novo = ui.Botao(
            rect=(botao_novo_x, 16, 130, 28),
            texto="Novo Labirinto",
            ao_clicar=self.novo_labirinto,
        )

        self.grid_origem = (MARGEM, TOPO_BARRA_ALTURA)

    # -------------------------------------------------------------------
    def novo_labirinto(self) -> None:
        self.maze = gerar_labirinto(LINHAS, COLUNAS, DENSIDADE_PAREDES)
        self.resultado = None
        self.erro = None
        self.revelados = 0

    def executar_algoritmo(self) -> None:
        algoritmo = ALGORITMOS[self.dropdown.selecionado]
        self.erro = None
        self.revelados = 0
        try:
            self.resultado = algoritmo(self.maze)
        except NotImplementedError as e:
            self.resultado = None
            self.erro = str(e) or "Algoritmo ainda não implementado."

    # -------------------------------------------------------------------
    def atualizar_animacao(self) -> None:
        if not ANIMAR or self.resultado is None:
            return
        total = len(self.resultado.explorados) + len(self.resultado.caminho)
        if self.revelados < total:
            self.revelados = min(total, self.revelados + CELULAS_POR_FRAME)

    def celulas_visiveis(self):
        """Retorna (explorados_visiveis, caminho_visivel) considerando a animação."""
        if self.resultado is None:
            return [], []
        if not ANIMAR:
            return self.resultado.explorados, self.resultado.caminho

        n_explorados = len(self.resultado.explorados)
        if self.revelados <= n_explorados:
            return self.resultado.explorados[: self.revelados], []
        return self.resultado.explorados, self.resultado.caminho[: self.revelados - n_explorados]

    # -------------------------------------------------------------------
    def desenhar_barra_superior(self) -> None:
        rotulo = self.fonte.render("Algoritmo:", True, ui.COR_TEXTO)
        self.tela.blit(rotulo, (MARGEM, 22))

        self.dropdown.desenhar(self.tela, self.fonte)
        self.botao_executar.desenhar(self.tela, self.fonte)
        self.botao_novo.desenhar(self.tela, self.fonte)

    def desenhar_rodape(self) -> None:
        y_stats = TOPO_BARRA_ALTURA + GRID_ALTURA + 6

        if self.erro:
            texto = f"⚠ {self.erro}"
            cor = (248, 113, 113)
        elif self.resultado is not None:
            tamanho_caminho = len(self.resultado.caminho)
            texto = (
                f"Caminho: {tamanho_caminho} | "
                f"Expandidos: {self.resultado.expandidos} | "
                f"Tempo: {self.resultado.tempo:.6f}s"
            )
            cor = ui.COR_TEXTO_FRACO
        else:
            texto = "Escolha um algoritmo e clique em Executar."
            cor = ui.COR_TEXTO_FRACO

        stats_surf = self.fonte_pequena.render(texto, True, cor)
        self.tela.blit(stats_surf, (MARGEM, y_stats))

        y_legenda = y_stats + STATS_ALTURA
        ui.desenhar_legenda(self.tela, (MARGEM, y_legenda), self.fonte_pequena)

    # -------------------------------------------------------------------
    def desenhar(self) -> None:
        self.tela.fill(ui.COR_FUNDO)
        self.desenhar_barra_superior()

        explorados_visiveis, caminho_visivel = self.celulas_visiveis()
        ui.desenhar_tabuleiro(
            self.tela,
            self.grid_origem,
            TAMANHO_CELULA,
            self.maze,
            explorados=explorados_visiveis,
            caminho=caminho_visivel,
        )

        self.desenhar_rodape()

        # A lista do dropdown precisa ser desenhada por cima de tudo,
        # então redesenhamos ela ao final, se estiver aberta.
        if self.dropdown.aberto:
            self.dropdown.desenhar(self.tela, self.fonte)

        pygame.display.flip()

    # -------------------------------------------------------------------
    def executar(self) -> None:
        rodando = True
        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                else:
                    self.dropdown.processar_evento(evento)
                    # Só processa clique nos botões se o dropdown não
                    # estiver aberto (evita clique "atravessar" a lista).
                    if not self.dropdown.aberto:
                        self.botao_executar.processar_evento(evento)
                        self.botao_novo.processar_evento(evento)

            self.atualizar_animacao()
            self.desenhar()
            self.relogio.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Aplicacao().executar()
