import pygame
from dropdownClass import Dropdown

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

PILL_BG = (123, 217, 231)      # botão normal
PILL_HOVER = (120, 235, 255)   # botão hover
PILL_TEXT = (26, 127, 189)

def drawPill(surface, rect, text, font, hovered, bg_color, hover_color, text_color, border_radius):
    # sombra em camadas (parecida com Figma)
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

    # corpo do botão
    color = hover_color if hovered else bg_color
    pygame.draw.rect(surface, color, rect, border_radius=border_radius)

    # texto centralizado
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

# Características de font
fontNivel = pygame.font.SysFont("Comic Sans MS", 40, bold=True)

# Chamada do método com as características do dropdown
dropdown = Dropdown(x = 440, y = 80, w = 400, h = 90, options = ["NÍVEL 1", "NÍVEL 2", "NÍVEL 3", "NÍVEL 4"], fonte = fontNivel)

# botão Jogar
botaoJogar = PillButton(
    x= 490,
    y= 545,  # ajusta se quiser mais pra cima/baixo
    w=300,
    h=90,
    text="JOGAR",
    fonte= fontNivel,
)

telaAtual = "menu"

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if telaAtual == "menu":
            dropdown.handle_event(event)
            if botaoJogar.handle_event(event):
                tela_atual = "jogo"

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("#C7E2E4")
    
    #------ BONECO DE NEVE ------#
    icon_image = pygame.image.load('amazing_game/src/frontend/img/icon.png')
    scaled_image = icon_image.get_rect()
    scaled_image.center = (640, 360)
    screen.blit(icon_image, scaled_image)

    dropdown.draw(screen)
    botaoJogar.draw(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()