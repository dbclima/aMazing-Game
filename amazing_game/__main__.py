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

        print(type(tempoFinal))

        if sucesso:
            crud.saveStats(nivel, nomeJogador, XPfinal, tempoFinal)

        rank = crud.getStats(nivel)
        rank_lista = [(chave, valor["score"], str(valor["time"])) for chave, valor in rank]

        ranking.ranking(rank_lista)


#nomeJogador = telaNome.Nome(screen)
#print("Jogador:", nomeJogador)