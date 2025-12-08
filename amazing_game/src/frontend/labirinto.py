import pygame
from pathlib import Path
import time
from ..backend import criar_labirinto, Dificuldade, transforma_labirinto_para_json_front


# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

#------ Configurações de Tempo e Vida ------#

XPDimensions = pygame.Rect(300, 70, 200, 50)
timeDimensions = pygame.Rect(780, 70, 200, 50)

fontSettings = pygame.font.SysFont("Bangers", 25, bold=True)


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



labirinto = criar_labirinto(0, 3, 3, maximo_checkpoints=8, dificuldade=Dificuldade.DIFICIL)
dados = transforma_labirinto_para_json_front(labirinto)


#------ Dados aleatórios (mock do backend) ------#
# dados = {
#     "nivel": 1,
#     "linhas": 5,
#     "colunas": 4,  
#     "origem": [0, 0],
#     "chegada": [4, 3],
#     "vidaInicial": 30,
#     "checkpoints": [
#         {"pos": (0, 2), "bonus": 2},
#         {"pos": (1, 0), "bonus": 7},
#         {"pos": (2, 3), "bonus": 8},
#         {"pos": (3, 1), "bonus": 5},
#     ],
#     "arestas": [
#         {"de": [0, 0], "para": [0, 1], "peso": -1},
#         {"de": [0, 1], "para": [0, 2], "peso": -1},
#         {"de": [0, 1], "para": [1, 1], "peso": -1},
#         {"de": [0, 2], "para": [1, 2], "peso": -1},
#         {"de": [1, 1], "para": [2, 1], "peso": -1},
#         {"de": [1, 1], "para": [1, 0], "peso": -1},
#         {"de": [1, 0], "para": [2, 0], "peso": -1},
#         {"de": [1, 0], "para": [1, 1], "peso": -1},
#         {"de": [2, 0], "para": [3, 0], "peso": -1},
#         {"de": [2, 1], "para": [2, 2], "peso": -1},
#         {"de": [2, 2], "para": [3, 2], "peso": -1},
#         {"de": [2, 2], "para": [2, 3], "peso": -1},
#         {"de": [3, 0], "para": [4, 0], "peso": -1},
#         {"de": [3, 1], "para": [4, 1], "peso": -1},
#         {"de": [3, 1], "para": [3, 0], "peso": -1},
#         {"de": [3, 2], "para": [4, 2], "peso": -1},
#         {"de": [4, 1], "para": [4, 2], "peso": -1},
#         {"de": [4, 2], "para": [4, 3], "peso": -1},
#     ],
# }

#------ Configurações do Labirinto ------#

dadosLabirinto = dados  # futuramente: nivelLabirinto(nivel)

linhasLabirinto = dadosLabirinto["linhas"]
colunasLabirinto = dadosLabirinto["colunas"]

linhaOrigem, colunaOrigem = dadosLabirinto["origem"]
posChegada = tuple(dadosLabirinto["chegada"])

XP_inicial = dadosLabirinto["vidaInicial"]
currentXP = XP_inicial

CHECKPOINTS = {tuple(item["pos"]): item["bonus"] for item in dadosLabirinto["checkpoints"]}

# monta a estrutura de arestas para acesso fácil
arestas = {}
for e in dadosLabirinto["arestas"]:
    u = tuple(e["de"])
    v = tuple(e["para"])
    w = e["peso"]
    arestas[(u, v)] = w
    arestas[(v, u)] = w  # movimento nos dois sentidos


tamCEL = 80

larguraLAB = colunasLabirinto * tamCEL
alturaLAB = linhasLabirinto * tamCEL

labRECT = pygame.Rect((screen.get_width()  - larguraLAB)  // 2, (screen.get_height() - alturaLAB) // 2 + 40, larguraLAB, alturaLAB)


def desenhaBoneco():
    icon_image = pygame.image.load(r'amazing_game\src\frontend\img\icon.png')
    scaled_image = pygame.transform.scale(icon_image, (tamCEL, tamCEL))
    screen.blit(scaled_image, (px - tamCEL//2, py - tamCEL//2))

def desenhaIglu():
    icon_image = pygame.image.load(r'amazing_game\src\frontend\img\igluicon.png')
    scaled_image = pygame.transform.scale(icon_image, (tamCEL, tamCEL))
    x = labRECT.x + (colunasLabirinto - 1) * tamCEL
    y = labRECT.y + (linhasLabirinto - 1) * tamCEL
    screen.blit(scaled_image, (x , y))

def desenhaSorvete(x,y):
    print(Path(".").cwd())
    icon_image = pygame.image.load(r'amazing_game\src\frontend\img\iconSorvete.png')
    scaled_image = pygame.transform.scale(icon_image, (tamCEL, tamCEL))
    screen.blit(scaled_image, (x , y))


def temAresta(a, b):
    return (a, b) in arestas


def desenharLabirinto(screen):
    for r in range(linhasLabirinto):
        for c in range(colunasLabirinto):
            x = labRECT.x + c * tamCEL
            y = labRECT.y + r * tamCEL
            rectCEL = pygame.Rect(x, y, tamCEL, tamCEL)

            # piso
            pygame.draw.rect(screen, (199, 226, 228), rectCEL)

            pos = (r, c)

            # cores especiais
            # if pos == (linhaOrigem, colunaOrigem):
                # pygame.draw.rect(screen, (0, 204, 219), rectCEL)  # início
            # if pos == posChegada:
            #     pygame.draw.rect(screen, (255, 215, 0), rectCEL)  # chegada
            if pos in CHECKPOINTS:
                desenhaSorvete(x,y)
                # pygame.draw.rect(screen, (0, 200, 0), rectCEL)  # checkpoint

            # paredes
            # top
            if r == 0 or not temAresta(pos, (r - 1, c)):
                pygame.draw.line(screen, (0, 184, 197), (x, y), (x + tamCEL, y), 3)
            # bottom
            if r == linhasLabirinto - 1 or not temAresta(pos, (r + 1, c)):
                pygame.draw.line(
                    screen, (0, 184, 197), (x, y + tamCEL), (x + tamCEL, y + tamCEL), 3
                )
            # left
            if c == 0 or not temAresta(pos, (r, c - 1)):
                pygame.draw.line(screen, (0, 184, 197), (x, y), (x, y + tamCEL), 3)
            # right
            if c == colunasLabirinto - 1 or not temAresta(pos, (r, c + 1)):
                pygame.draw.line(
                    screen, (0, 184, 197), (x + tamCEL, y), (x + tamCEL, y + tamCEL), 3
                )


#------ Estado inicial de jogo ------#

playerPos = [linhaOrigem, colunaOrigem]
checkpointsVisitados = set()
tempoInicial = time.time()

#----------------- LOOP PRINCIPAL -----------------#
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            dr, dc = 0, 0

            if keys[pygame.K_UP]:
                dr = -1
            elif keys[pygame.K_DOWN]:
                dr = 1
            elif keys[pygame.K_LEFT]:
                dc = -1
            elif keys[pygame.K_RIGHT]:
                dc = 1

            if dr != 0 or dc != 0:
                antigo = tuple(playerPos)
                novo = (playerPos[0] + dr, playerPos[1] + dc)

                # verifica se está dentro da grid E se há aresta
                if (
                    0 <= novo[0] < linhasLabirinto
                    and 0 <= novo[1] < colunasLabirinto
                    and (antigo, novo) in arestas
                ):
                    w = arestas[(antigo, novo)]  # peso da aresta = delta de vida
                    playerPos[:] = list(novo)

                    currentXP += w
                    # se quiser, pode travar em 0 pra não ficar negativo:
                    if currentXP < 0:
                        currentXP = 0
                        tempoFinal = time.time() - tempoInicial
                        print("Não conseguiu terminar")
                        print("Tempo:", round(tempoFinal, 2), "s")
                        running = False

                    # checkpoint (só conta uma vez)
                    if novo in CHECKPOINTS and novo not in checkpointsVisitados:
                        currentXP += CHECKPOINTS[novo]
                        checkpointsVisitados.add(novo)

                    # chegou ao fim?
                    if novo == posChegada:
                        tempoFinal = time.time() - tempoInicial
                        print("Fim do nível!")
                        print("Vida final:", currentXP)
                        print("Tempo:", round(tempoFinal, 2), "s")
                        running = False

    # fundo
    screen.fill("#C7E2E4")

    # --- MOVIMENTO DO JOGADOR ---

    # --- DESENHAR LABIRINTO ---
    desenharLabirinto(screen)

    # --- DESENHAR JOGADOR ---
    px = labRECT.x + playerPos[1] * tamCEL + tamCEL // 2
    py = labRECT.y + playerPos[0] * tamCEL + tamCEL // 2
    pygame.draw.circle(screen, (255, 100, 100), (px, py), tamCEL // 3)
    desenhaBoneco()
    desenhaIglu()


    #--------- HUD DE VIDA (XP) ---------#
    drawShadow(screen, XPDimensions, offset=(-3, 3))
    pygame.draw.rect(screen, "#7BD9E7", XPDimensions, border_radius=40)

    XP_Text = fontSettings.render("XP:", True, (26, 123, 253))
    XP_Text_rect = XP_Text.get_rect()
    XP_Text_rect.centery = XPDimensions.centery

    XP_valueText = fontSettings.render(f"{currentXP}", True, (221, 110, 106))
    XP_valueText_rect = XP_valueText.get_rect()
    XP_valueText_rect.centery = XPDimensions.centery

    total_width = XP_Text_rect.width + 10 + XP_valueText_rect.width
    start_x = XPDimensions.centerx - total_width // 2
    XP_Text_rect.x = start_x
    XP_valueText_rect.x = XP_Text_rect.right + 10

    screen.blit(XP_Text, XP_Text_rect)
    screen.blit(XP_valueText, XP_valueText_rect)

    #--------- HUD DE TEMPO ---------#
    drawShadow(screen, timeDimensions, offset=(-3, 3))
    pygame.draw.rect(screen, "#7BD9E7", timeDimensions, border_radius=40)

    tempoDecorrido = int(time.time() - tempoInicial)
    TIME_Text = fontSettings.render("TIME:", True, (26, 123, 253))
    TIME_Text_rect = TIME_Text.get_rect()
    TIME_Text_rect.centery = timeDimensions.centery

    TIME_valueText = fontSettings.render(f"{tempoDecorrido}s", True, (221, 110, 106))
    TIME_valueText_rect = TIME_valueText.get_rect()
    TIME_valueText_rect.centery = timeDimensions.centery

    total_width_time = TIME_Text_rect.width + 10 + TIME_valueText_rect.width
    start_x_time = timeDimensions.centerx - total_width_time // 2
    TIME_Text_rect.x = start_x_time
    TIME_valueText_rect.x = TIME_Text_rect.right + 10

    screen.blit(TIME_Text, TIME_Text_rect)
    screen.blit(TIME_valueText, TIME_valueText_rect)

    # atualizar tela
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
