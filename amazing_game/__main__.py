from .src.frontend import telaNome
from .src.frontend import menu
from .src.frontend import labirinto
from .src.frontend import ranking
import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Amazing Game")

while True:
    nomeJogador = telaNome.Nome(screen)
    acao, nivel = menu.telaMenu(screen)
    if acao == "jogar":
        sucesso, XPfinal, tempoFinal = labirinto.telaLabirinto(screen, nivel, nomeJogador)
        ranking.ranking()


#nomeJogador = telaNome.Nome(screen)
#print("Jogador:", nomeJogador)