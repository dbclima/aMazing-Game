from .src.frontend import telaNome
from .src.frontend import menu
from .src.frontend import labirinto
from .src.frontend import ranking
from .src.database import crud
import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 740))
pygame.display.set_caption("Amazing Game")

while True:
    nomeJogador = telaNome.Nome(screen)
    acao, nivel = menu.telaMenu(screen)
    if acao == "jogar":

        lab = crud.loadLab(nivel)

        sucesso, XPfinal, tempoFinal = labirinto.telaLabirinto(lab,screen)

        ranking.ranking()


#nomeJogador = telaNome.Nome(screen)
#print("Jogador:", nomeJogador)