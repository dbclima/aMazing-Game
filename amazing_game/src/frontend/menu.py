import pygame
from .dropdownClass import Dropdown

PILL_BG = (123, 217, 231)      
PILL_HOVER = (120, 235, 255)   
PILL_TEXT = (26, 127, 189)


def drawPill(surface, rect, text, font, hovered, bg_color, hover_color, text_color, border_radius):
    shadow_layers = [
        (2, 2, 20),
        (3, 3, 15),
        (4, 4, 10),
    ]

    for dx, dy, alpha in shadow_layers:
        shadow_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(
            shadow_surf,
            (0, 0, 0, alpha),
            shadow_surf.get_rect(),
            border_radius=border_radius
        )
        surface.blit(shadow_surf, (rect.x + dx, rect.y + dy))

    color = hover_color if hovered else bg_color
    pygame.draw.rect(surface, color, rect, border_radius=border_radius)

    if text:
        txt_surf = font.render(text, True, text_color)
        txt_rect = txt_surf.get_rect(center=rect.center)
        surface.blit(txt_surf, txt_rect)


class PillButton:
    def __init__(self, x, y, w, h, text, fonte):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = fonte
        self.bg_color = PILL_BG
        self.hover_color = PILL_HOVER
        self.text_color = PILL_TEXT
        self.border_radius = h // 2

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def draw(self, surface):
        mx, my = pygame.mouse.get_pos()
        hovered = self.rect.collidepoint(mx, my)
        drawPill(
            surface,
            self.rect,
            self.text,
            self.font,
            hovered,
            self.bg_color,
            self.hover_color,
            self.text_color,
            self.border_radius,
        )


def telaMenu(screen):
    """Tela de menu. Retorna ('jogar', nivel_escolhido) quando clicar no botão JOGAR."""
    clock = pygame.time.Clock()

    # Fonte
    fontNivel = pygame.font.SysFont("Comic Sans MS", 40, bold=True)

    # Dropdown
    dropdown = Dropdown(
        x=440,
        y=80,
        w=400,
        h=90,
        options=["NÍVEL 1", "NÍVEL 2", "NÍVEL 3", "NÍVEL 4"],
        fonte=fontNivel,
    )

    # Botão Jogar
    botaoJogar = PillButton(
        x=490,
        y=545,  
        w=300,
        h=90,
        text="JOGAR",
        fonte=fontNivel,
    )

    # Boneco de neve
    icon_image = pygame.image.load("amazing_game/src/frontend/img/icon.png").convert_alpha()
    icon_rect = icon_image.get_rect()
    icon_rect.center = (640, 360)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            dropdown.handle_event(event)

            if botaoJogar.handle_event(event):
                try:
                    nivel_escolhido = dropdown.options[dropdown.selected_index]
                except AttributeError:
                    nivel_escolhido = "NÍVEL 1"
                return "jogar", nivel_escolhido

        # fundo
        screen.fill("#C7E2E4")

        # boneco de neve
        screen.blit(icon_image, icon_rect)

        # UI
        dropdown.draw(screen)
        botaoJogar.draw(screen)

        pygame.display.flip()
        clock.tick(60)
