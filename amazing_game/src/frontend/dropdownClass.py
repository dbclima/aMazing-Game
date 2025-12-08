import pygame 

import pygame

class Dropdown:
    def __init__(self, x, y, w, h, options, fonte):
        self.rect = pygame.Rect(x, y, w, h)
        self.options = options
        self.font = fonte

        self.selected_index = 0
        self.open = False

        # cores de estilo (ajuste como quiser)
        self.bg_color = (123, 217, 231)   # azul do botão
        self.text_color = (26, 127, 189)    # azul do texto
        self.shadow_color = (0, 0, 0, 40) # sombra
        self.hover_color = (120, 235, 255)

        # altura de cada item da lista
        self.item_height = h
        self.border_radius = h // 2   # pílula

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos

            # clique no botão principal
            if self.rect.collidepoint(mx, my):
                self.open = not self.open
                return

            # se aberto, verificar clique nas opções
            if self.open:
                for i, _ in enumerate(self.options):
                    item_rect = pygame.Rect(
                        self.rect.x,
                        self.rect.y + self.rect.height * (i + 1),
                        self.rect.width,
                        self.rect.height
                    )
                    if item_rect.collidepoint(mx, my):
                        self.selected_index = i
                        self.open = False
                        return

        # se clicar em qualquer outro lugar, fecha
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.open:
                mx, my = event.pos
                area_total = pygame.Rect(
                    self.rect.x,
                    self.rect.y,
                    self.rect.width,
                    self.rect.height * (len(self.options) + 1)
                )
                if not area_total.collidepoint(mx, my):
                    self.open = False

    def draw_pill(self, surface, rect, text, hovered=False):
        # ===== SOMBRA SUAVE MULTI-CAMADAS =====
        shadow_layers = [
            (2, 2, 20),
            (3, 3, 15),
            (4, 4, 10),
        ]

        for dx, dy, alpha in shadow_layers:
            shadow_surf = pygame.Surface(
                (rect.width, rect.height),
                pygame.SRCALPHA
            )
            pygame.draw.rect(
                shadow_surf,
                (0, 0, 0, alpha),
                shadow_surf.get_rect(),
                border_radius=self.border_radius
            )
            surface.blit(shadow_surf, (rect.x + dx, rect.y + dy))

        # ===== CORPO DO BOTÃO =====
        color = self.hover_color if hovered else self.bg_color
        pygame.draw.rect(surface, color, rect, border_radius=self.border_radius)

        # ===== TEXTO =====
        txt_surf = self.font.render(text, True, self.text_color)
        txt_rect = txt_surf.get_rect(center=rect.center)
        surface.blit(txt_surf, txt_rect)


    def draw_arrow(self, surface):
        cx = self.rect.right - 50     # distância da borda direita
        cy = self.rect.centery
        size = 11                     # 🔽 tamanho da seta (AJUSTE AQUI)

        if self.open:
            points = [
                (cx - size, cy + size),
                (cx + size, cy + size),
                (cx, cy - size)
            ]
        else:
            points = [
                (cx - size, cy - size),
                (cx + size, cy - size),
                (cx, cy + size)
            ]

        pygame.draw.polygon(surface, self.text_color, points)

    def draw(self, surface):
        mx, my = pygame.mouse.get_pos()

        # botão principal
        hovered_main = self.rect.collidepoint(mx, my)
        self.draw_pill(surface, self.rect, self.options[self.selected_index], hovered_main)
        self.draw_arrow(surface)

        # lista aberta
        if self.open:
            for i, opt in enumerate(self.options):
                item_rect = pygame.Rect(
                    self.rect.x,
                    self.rect.y + self.rect.height * (i + 1),
                    self.rect.width,
                    self.rect.height
                )
                hovered = item_rect.collidepoint(mx, my)
                self.draw_pill(surface, item_rect, opt, hovered)
