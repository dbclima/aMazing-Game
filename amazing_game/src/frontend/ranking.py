import pygame
import sys

pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 600, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ranking")

# Cores
BACKGROUND_COLOR = (0xC7, 0xE2, 0xE4)   # C7E2E4
RANKING_BG = (0x7B, 0xD9, 0xE7)         # 7BD9E7
TEXT_COLOR       = (0x1A, 0x7F, 0xBD)

# Fonte
font = pygame.font.SysFont("arial", 24)
title_font = pygame.font.SysFont("arial", 32, bold=True)

# Ranking (máx. 10)
ranking = [
    ("Alice", 1200, "02:13"),
    ("Bob", 1100, "02:50"),
    ("Carol", 1050, "03:10"),
    ("Daniel", 990, "03:40"),
    ("Eve", 970, "03:55"),
]

# Botão Menu
button_rect = pygame.Rect(WIDTH//2 - 80, HEIGHT - 80, 160, 50)

def draw_ranking():
    # Fundo geral
    screen.fill(BACKGROUND_COLOR)

    # Área do ranking
    pygame.draw.rect(screen, RANKING_BG, (40, 40, WIDTH - 80, HEIGHT - 140), border_radius=12)

    # Título
    title = title_font.render("Ranking", True, TEXT_COLOR)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 55))

    # Cabeçalho
    screen.blit(font.render("Pos", True, TEXT_COLOR), (70, 100))
    screen.blit(font.render("Nome", True, TEXT_COLOR), (130, 100))
    screen.blit(font.render("XP", True, TEXT_COLOR), (330, 100))
    screen.blit(font.render("Tempo", True, TEXT_COLOR), (420, 100))

    # Linhas do ranking
    y = 140
    for i, (nome, xp, tempo) in enumerate(ranking[:10], start=1):
        screen.blit(font.render(str(i), True, (0, 0, 0)), (70, y))
        screen.blit(font.render(nome, True, (0, 0, 0)), (130, y))
        screen.blit(font.render(str(xp), True, (0, 0, 0)), (330, y))
        screen.blit(font.render(tempo, True, (0, 0, 0)), (420, y))
        y += 35

    # Botão Menu
    pygame.draw.rect(screen, (255, 255, 255), button_rect, border_radius=10)
    pygame.draw.rect(screen, (0, 0, 0), button_rect, 2, border_radius=10)

    text = font.render("Menu", True, (0, 0, 0))
    screen.blit(text, (button_rect.x + 45, button_rect.y + 10))

    pygame.display.update()


def ranking_screen():
    while True:
        draw_ranking()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    print("Voltando para o menu...")
                    return


ranking_screen()
