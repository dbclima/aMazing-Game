import pygame
import sys

def draw_pill(surface, rect, text, font, hovered,
              bg_color=(123, 217, 231),
              hover_color=(140, 240, 255),
              text_color=(26, 127, 189)):
    border_radius = rect.height // 2

    # sombra estilo Figma (camadas suaves)
    shadow_layers = [
        (2, 2, 20),
        (3, 3, 15),
        (4, 4, 10),
    ]

    for dx, dy, alpha in shadow_layers:
        shadow = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(
            shadow,
            (0, 0, 0, alpha),
            shadow.get_rect(),
            border_radius=border_radius
        )
        surface.blit(shadow, (rect.x + dx, rect.y + dy))

    # corpo do botão
    color = hover_color if hovered else bg_color
    pygame.draw.rect(surface, color, rect, border_radius=border_radius)

    # texto centralizado
    txt = font.render(text, True, text_color)
    surface.blit(txt, txt.get_rect(center=rect.center))


def ranking():
# Configurações da tela
  WIDTH, HEIGHT = 1280, 720
  screen = pygame.display.set_mode((WIDTH, HEIGHT))

  pygame.display.set_caption("Ranking")

  # Cores
  BACKGROUND_COLOR = (0xC7, 0xE2, 0xE4)   # C7E2E4
  RANKING_BG = (0x7B, 0xD9, 0xE7)         # 7BD9E7
  TEXT_COLOR       = (0x1A, 0x7F, 0xBD)

  # Fonte
  font = pygame.font.SysFont("arial", 24)
  title_font = pygame.font.SysFont("Comic Sans MS", 32, bold=True)

  # Ranking (máx. 10)
  ranking = [
      ("Alice", 1200, "02:13"),
      ("Bob", 1100, "02:50"),
      ("Carol", 1050, "03:10"),
      ("Daniel", 990, "03:40"),
      ("Eve", 970, "03:55"),
  ]

  # Botão Menu
  button_rect = pygame.Rect(WIDTH//2 - 200, HEIGHT - 90, 400, 70)

  def draw_ranking():
    # Fundo geral
    screen.fill(BACKGROUND_COLOR)

    # --- Retângulo do ranking (menor e centralizado) ---
    ranking_rect = pygame.Rect(0, 0, int(WIDTH * 0.8), int(HEIGHT * 0.65))
    ranking_rect.centerx = WIDTH // 2
    ranking_rect.top = 120  # distância do topo (abaixo do título)

    pygame.draw.rect(screen, RANKING_BG, ranking_rect, border_radius=25)

    # --- Título ---
    title = title_font.render("RANKING", True, TEXT_COLOR)
    screen.blit(title, title.get_rect(midtop=(WIDTH // 2, 40)))

    # --- Colunas: Pos | Nome | XP | Tempo ---
    col_count = 4
    col_width = ranking_rect.width / col_count
    col_centers = [
        ranking_rect.left + col_width * (i + 0.5) for i in range(col_count)
    ]

    header_y = ranking_rect.top + 30

    headers = ["Pos", "Nome", "XP", "Tempo"]
    for i, label in enumerate(headers):
        surf = font.render(label, True, TEXT_COLOR)
        rect = surf.get_rect(center=(col_centers[i], header_y))
        screen.blit(surf, rect)

    # --- Linhas do ranking ---
    row_y = header_y + 40   # primeira linha depois do cabeçalho
    row_step = 35           # distância vertical entre linhas

    for idx, (nome, xp, tempo) in enumerate(ranking[:10], start=1):
        valores = [str(idx), nome, str(xp), tempo]

        for i, valor in enumerate(valores):
            surf = font.render(valor, True, (0, 0, 0))
            rect = surf.get_rect(center=(col_centers[i], row_y))
            screen.blit(surf, rect)

        row_y += row_step

    # --- Botão MENU (mantém como estava, só desenha depois do ranking) ---
    mx, my = pygame.mouse.get_pos()
    hovered = button_rect.collidepoint((mx, my))

    draw_pill(
        screen,
        button_rect,
        "VOLTAR",
        title_font,
        hovered
    )

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
                      return


  ranking_screen()
