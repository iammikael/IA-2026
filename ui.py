"""
Autor: Alexandre Augusto Angelo de Souza
Data: 18/07/2026
-----
Componentes visuais reutilizáveis (cores, botão, dropdown) e a rotina
que desenha o tabuleiro na tela.

Este módulo já está PRONTO — não mexa!!!
"""

from __future__ import annotations

from typing import Callable, List, Optional, Sequence, Tuple

import pygame

# ---------------------------------------------------------------------------
# Paleta de cores (mesmo estilo da interface de exemplo)
# ---------------------------------------------------------------------------
COR_FUNDO = (18, 22, 33)
COR_PAINEL = (26, 31, 46)
COR_TEXTO = (226, 232, 240)
COR_TEXTO_FRACO = (148, 163, 184)

COR_CELULA_LIVRE = (42, 49, 68)
COR_CELULA_PAREDE = (10, 10, 14)
COR_GRADE = (54, 61, 82)

COR_INICIO = (74, 222, 128)      # verde
COR_OBJETIVO = (236, 72, 153)    # vermelho/rosa
COR_EXPLORADO = (91, 141, 199)   # azul
COR_CAMINHO = (244, 210, 156)    # areia/laranja claro

COR_BOTAO = (37, 99, 235)
COR_BOTAO_HOVER = (59, 130, 246)
COR_BOTAO_DESTAQUE = (34, 197, 94)
COR_BOTAO_DESTAQUE_HOVER = (74, 222, 128)

COR_DROPDOWN = (30, 41, 59)
COR_DROPDOWN_BORDA = (71, 85, 105)


class Botao:
    """Botão clicável simples, com texto centralizado."""

    def __init__(
        self,
        rect: Tuple[int, int, int, int],
        texto: str,
        ao_clicar: Callable[[], None],
        cor: Tuple[int, int, int] = COR_BOTAO,
        cor_hover: Tuple[int, int, int] = COR_BOTAO_HOVER,
    ) -> None:
        self.rect = pygame.Rect(rect)
        self.texto = texto
        self.ao_clicar = ao_clicar
        self.cor = cor
        self.cor_hover = cor_hover

    def desenhar(self, tela: pygame.Surface, fonte: pygame.font.Font) -> None:
        mouse_pos = pygame.mouse.get_pos()
        sobre = self.rect.collidepoint(mouse_pos)
        cor = self.cor_hover if sobre else self.cor
        pygame.draw.rect(tela, cor, self.rect, border_radius=6)
        texto_surf = fonte.render(self.texto, True, (255, 255, 255))
        texto_rect = texto_surf.get_rect(center=self.rect.center)
        tela.blit(texto_surf, texto_rect)

    def processar_evento(self, evento: pygame.event.Event) -> None:
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.rect.collidepoint(evento.pos):
                self.ao_clicar()


class Dropdown:
    """Caixa de seleção simples (droplist) com uma lista de opções."""

    def __init__(
        self,
        rect: Tuple[int, int, int, int],
        opcoes: Sequence[str],
        selecionado: Optional[str] = None,
    ) -> None:
        self.rect = pygame.Rect(rect)
        self.opcoes = list(opcoes)
        self.selecionado = selecionado if selecionado in self.opcoes else self.opcoes[0]
        self.aberto = False

    def _rect_opcao(self, indice: int) -> pygame.Rect:
        return pygame.Rect(
            self.rect.x,
            self.rect.y + self.rect.height * (indice + 1),
            self.rect.width,
            self.rect.height,
        )

    def desenhar(self, tela: pygame.Surface, fonte: pygame.font.Font) -> None:
        # Caixa principal
        pygame.draw.rect(tela, COR_DROPDOWN, self.rect, border_radius=6)
        pygame.draw.rect(tela, COR_DROPDOWN_BORDA, self.rect, width=1, border_radius=6)

        texto_surf = fonte.render(self.selecionado, True, COR_TEXTO)
        texto_rect = texto_surf.get_rect(midleft=(self.rect.x + 10, self.rect.centery))
        tela.blit(texto_surf, texto_rect)

        # Seta indicando abrir/fechar
        seta_centro = (self.rect.right - 15, self.rect.centery)
        direcao = -1 if self.aberto else 1
        pygame.draw.polygon(
            tela,
            COR_TEXTO_FRACO,
            [
                (seta_centro[0] - 5, seta_centro[1] - 3 * direcao),
                (seta_centro[0] + 5, seta_centro[1] - 3 * direcao),
                (seta_centro[0], seta_centro[1] + 3 * direcao),
            ],
        )

        # Lista de opções (desenhada por cima de tudo, quando aberta)
        if self.aberto:
            for i, opcao in enumerate(self.opcoes):
                rect_opcao = self._rect_opcao(i)
                mouse_pos = pygame.mouse.get_pos()
                sobre = rect_opcao.collidepoint(mouse_pos)
                cor_fundo = COR_BOTAO_HOVER if sobre else COR_DROPDOWN
                pygame.draw.rect(tela, cor_fundo, rect_opcao)
                pygame.draw.rect(tela, COR_DROPDOWN_BORDA, rect_opcao, width=1)
                op_surf = fonte.render(opcao, True, COR_TEXTO)
                op_rect = op_surf.get_rect(midleft=(rect_opcao.x + 10, rect_opcao.centery))
                tela.blit(op_surf, op_rect)

    def processar_evento(self, evento: pygame.event.Event) -> None:
        if evento.type != pygame.MOUSEBUTTONDOWN or evento.button != 1:
            return

        if self.rect.collidepoint(evento.pos):
            self.aberto = not self.aberto
            return

        if self.aberto:
            for i, opcao in enumerate(self.opcoes):
                if self._rect_opcao(i).collidepoint(evento.pos):
                    self.selecionado = opcao
                    break
            self.aberto = False


def desenhar_tabuleiro(
    tela: pygame.Surface,
    origem: Tuple[int, int],
    tamanho_celula: int,
    maze,
    explorados: Optional[List[Tuple[int, int]]] = None,
    caminho: Optional[List[Tuple[int, int]]] = None,
) -> None:
    """
    Desenha o tabuleiro (labirinto) na tela a partir do ponto `origem`
    (canto superior esquerdo, em pixels), usando `tamanho_celula` pixels
    por célula.

    - Células livres: cinza escuro
    - Obstáculos: preto
    - Início: verde | Objetivo: vermelho/rosa
    - `explorados`: células visitadas pela busca (azul)
    - `caminho`: caminho final encontrado (areia/laranja)
    """
    ox, oy = origem
    explorados = explorados or []
    caminho = caminho or []
    conjunto_explorados = set(explorados)
    conjunto_caminho = set(caminho)

    for r in range(maze.linhas):
        for c in range(maze.colunas):
            celula = (r, c)
            rect = pygame.Rect(ox + c * tamanho_celula, oy + r * tamanho_celula, tamanho_celula, tamanho_celula)

            if maze.grade[r][c] == 1:
                cor = COR_CELULA_PAREDE
            elif celula in conjunto_caminho:
                cor = COR_CAMINHO
            elif celula in conjunto_explorados:
                cor = COR_EXPLORADO
            else:
                cor = COR_CELULA_LIVRE

            pygame.draw.rect(tela, cor, rect)
            pygame.draw.rect(tela, COR_GRADE, rect, width=1)

            if celula == maze.inicio:
                pygame.draw.rect(tela, COR_INICIO, rect)
                pygame.draw.rect(tela, COR_GRADE, rect, width=1)
            elif celula == maze.objetivo:
                pygame.draw.rect(tela, COR_OBJETIVO, rect)
                pygame.draw.rect(tela, COR_GRADE, rect, width=1)


def desenhar_legenda(
    tela: pygame.Surface,
    posicao: Tuple[int, int],
    fonte: pygame.font.Font,
) -> None:
    """Desenha a legenda de cores na parte inferior da janela."""
    x, y = posicao
    itens = [
        (COR_INICIO, "Início"),
        (COR_OBJETIVO, "Objetivo"),
        (COR_CELULA_PAREDE, "Parede"),
        (COR_EXPLORADO, "Explorado"),
        (COR_CAMINHO, "Caminho"),
    ]
    cursor_x = x
    for cor, rotulo in itens:
        pygame.draw.rect(tela, cor, (cursor_x, y, 16, 16), border_radius=3)
        texto_surf = fonte.render(rotulo, True, COR_TEXTO_FRACO)
        tela.blit(texto_surf, (cursor_x + 22, y - 1))
        cursor_x += 22 + texto_surf.get_width() + 22
