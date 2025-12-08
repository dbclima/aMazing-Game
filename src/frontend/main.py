import pygame
import string

ALLOWED_CHARS = string.ascii_letters + string.digits + " "

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

# Estado do input 
active = False
textPlayer = ""
visibilidadeCursor = True
last_switch = 0
CURSOR_PERIOD = 400  # ms

def drawShadow(screen, rect, border_radius=40, offset=(5, 5), shadow_color=(0, 0, 0, 90)):
    """Desenha uma sombra arredondada atrás de um rect."""
    sombra = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(
        sombra,
        shadow_color,
        (0, 0, rect.width, rect.height),
        border_radius=border_radius,
    )
    dest = rect.move(*offset)
    screen.blit(sombra, dest.topleft)


# Dimensões do retângulo da base
baseDimensions = pygame.Rect(0, 0, 480, 189)

# Dimensões da caixa de input
inputDimensions = pygame.Rect(0, 0, 360, 45)

# Características de font
fontTitulo = pygame.font.SysFont("Comic Sans MS", 40, bold=True)
fontInput = pygame.font.SysFont("Arial", 32)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # ativa/desativa input quando clica na caixinha
            active = inputDimensions.collidepoint(event.pos)

        elif event.type == pygame.KEYDOWN:
            # só processa teclas se o input estiver ativo
            if not active:
                continue

            if event.key == pygame.K_BACKSPACE:
                textPlayer = textPlayer[:-1]

            elif event.key == pygame.K_RETURN:
                print("Nome digitado:", textPlayer)

            else:
                ch = event.unicode
                # evita None / vazio e filtra caracteres estranhos
                if ch in ALLOWED_CHARS and len(textPlayer) < 16:
                    textPlayer += ch


    # fill the screen with a color to wipe away anything from last frame
    screen.fill("#C7E2E4")


    #------ CONFIGURAÇÕES DA BASE ------#

    drawShadow(screen, baseDimensions, offset=(-3, 3))
    pygame.draw.rect(screen, "#7BD9E7", baseDimensions, border_radius=40)
    baseDimensions.center = screen.get_rect().center

    #------ CONFIGURAÇÕES DE INPUT  ------#

    # Estilização do campo de input
    inputDimensions.centerx = baseDimensions.centerx
    inputDimensions.y = baseDimensions.y + 120
    pygame.draw.rect(screen, "#C7E2E4", inputDimensions, border_radius=20)


    # Estilização do input
    text = fontInput.render(textPlayer, True, (50, 50, 50))
    textRect = text.get_rect(midleft=(inputDimensions.x + 12, inputDimensions.centery))
    screen.blit(text, textRect)

    # Cursor
    if active and visibilidadeCursor:
        cursor_x = textRect.right + 3
        pygame.draw.line(screen, (50, 50, 50), (cursor_x, inputDimensions.y + 10), (cursor_x, inputDimensions.bottom - 10), 2)

    #------ CONFIGURAÇÕES DO TÍTULO  ------#
    titulo = fontTitulo.render("ESCREVA SEU NOME", True, (26, 127,189))
    tituloRect = titulo.get_rect(center = (baseDimensions.centerx, baseDimensions.y + 60))
    screen.blit(titulo, tituloRect)


    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()

# FALTA INTEGRAR COM O BACK E MANDAR PARA PÁGINA INICIAL