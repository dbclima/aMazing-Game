import pygame
import string

ALLOWED_CHARS = string.ascii_letters + string.digits + " "

def drawShadow(screen, rect, border_radius=40, offset=(5, 5), shadow_color=(0, 0, 0, 90)):
    sombra = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(
        sombra,
        shadow_color,
        (0, 0, rect.width, rect.height),
        border_radius=border_radius,
    )
    dest = rect.move(*offset)
    screen.blit(sombra, dest.topleft)


def Nome(screen):
    clock = pygame.time.Clock()

    # Estado do input
    active = False
    textPlayer = ""

    visibilidadeCursor = True
    last_switch = 0
    CURSOR_PERIOD = 400  # ms

    # Dimensões
    baseDimensions = pygame.Rect(0, 0, 480, 189)
    inputDimensions = pygame.Rect(0, 0, 360, 45)

    # Fonts
    fontTitulo = pygame.font.SysFont("Comic Sans MS", 40, bold=True)
    fontInput = pygame.font.SysFont("Arial", 32)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            elif event.type == pygame.MOUSEBUTTONDOWN:
                active = inputDimensions.collidepoint(event.pos)

            elif event.type == pygame.KEYDOWN:
                if not active:
                    continue

                if event.key == pygame.K_BACKSPACE:
                    textPlayer = textPlayer[:-1]

                elif event.key == pygame.K_RETURN:
                    if textPlayer.strip() != "":
                        return textPlayer  # ✅ AQUI MUDA DE TELA

                else:
                    ch = event.unicode
                    if ch in ALLOWED_CHARS and len(textPlayer) < 16:
                        textPlayer += ch

        # Cursor piscante
        now = pygame.time.get_ticks()
        if now - last_switch > CURSOR_PERIOD:
            visibilidadeCursor = not visibilidadeCursor
            last_switch = now

        # Fundo
        screen.fill("#C7E2E4")

        # Base
        baseDimensions.center = screen.get_rect().center
        drawShadow(screen, baseDimensions, offset=(-3, 3))
        pygame.draw.rect(screen, "#7BD9E7", baseDimensions, border_radius=40)

        # Input
        inputDimensions.centerx = baseDimensions.centerx
        inputDimensions.y = baseDimensions.y + 120
        pygame.draw.rect(screen, "#C7E2E4", inputDimensions, border_radius=20)

        text = fontInput.render(textPlayer, True, (50, 50, 50))
        textRect = text.get_rect(midleft=(inputDimensions.x + 12, inputDimensions.centery))
        screen.blit(text, textRect)

        if active and visibilidadeCursor:
            cursor_x = textRect.right + 3
            pygame.draw.line(
                screen,
                (50, 50, 50),
                (cursor_x, inputDimensions.y + 10),
                (cursor_x, inputDimensions.bottom - 10),
                2
            )

        # Título
        titulo = fontTitulo.render("ESCREVA SEU NOME", True, (26, 127, 189))
        tituloRect = titulo.get_rect(center=(baseDimensions.centerx, baseDimensions.y + 60))
        screen.blit(titulo, tituloRect)

        pygame.display.flip()
        clock.tick(60)
