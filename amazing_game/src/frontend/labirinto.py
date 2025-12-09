import pygame
from pathlib import Path
import time
from ..backend import criar_labirinto, Dificuldade, transforma_labirinto_para_json_front


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


def telaLabirinto(labirinto,screen):

    clock = pygame.time.Clock()

    #------ Configurações de Tempo e Vida ------#
    XPDimensions = pygame.Rect(300, 70, 200, 50)
    timeDimensions = pygame.Rect(780, 70, 200, 50)
    fontSettings = pygame.font.SysFont("Bangers", 25, bold=True)

    #------ Criação do labirinto com backend ------
    dados = transforma_labirinto_para_json_front(labirinto)

    #------ Configurações do Labirinto ------#
    dadosLabirinto = dados

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

    tamCEL = 80

    larguraLAB = colunasLabirinto * tamCEL
    alturaLAB = linhasLabirinto * tamCEL

    labRECT = pygame.Rect(
        (screen.get_width() - larguraLAB) // 2,
        (screen.get_height() - alturaLAB) // 2 + 40,
        larguraLAB,
        alturaLAB,
    )

    #------ Carrega imagens ------#
    boneco_img = pygame.image.load(r"amazing_game/src/frontend/img/icon.png").convert_alpha()
    boneco_img = pygame.transform.scale(boneco_img, (tamCEL, tamCEL))

    iglu_img = pygame.image.load(r"amazing_game/src/frontend/img/igluicon.png").convert_alpha()
    iglu_img = pygame.transform.scale(iglu_img, (tamCEL, tamCEL))

    sorvete_img = pygame.image.load(r"amazing_game/src/frontend/img/iconSorvete.png").convert_alpha()
    sorvete_img = pygame.transform.scale(sorvete_img, (tamCEL, tamCEL))

    #------ Funções internas ------#
    def desenhaBoneco(px, py):
        screen.blit(boneco_img, (px - tamCEL // 2, py - tamCEL // 2))

    print(posChegada)
    def desenhaIglu():
        x = labRECT.x + (posChegada[1]) * tamCEL
        y = labRECT.y + (posChegada[0]) * tamCEL
        screen.blit(iglu_img, (x, y))

    def desenhaSorvete(x, y, valor):
        checkpointFont = pygame.font.SysFont("arial", 22, bold=True)
        # Desenha o sorvete
        screen.blit(sorvete_img, (x, y))

        # Texto do valor
        texto = f"{valor:+d}"   # ex: +5, -3
        label = checkpointFont.render(texto, True, (255, 255, 255))

        rect = label.get_rect(center=(x + tamCEL // 2, y + tamCEL // 2))
        screen.blit(label, rect)

    def temAresta(a, b):
        return (a, b) in arestas

    def desenharLabirinto():
        for r in range(linhasLabirinto):
            for c in range(colunasLabirinto):
                x = labRECT.x + c * tamCEL
                y = labRECT.y + r * tamCEL
                rectCEL = pygame.Rect(x, y, tamCEL, tamCEL)

                # piso
                pygame.draw.rect(screen, (199, 226, 228), rectCEL)

                pos = (r, c)

                if pos in CHECKPOINTS:
                    valor = CHECKPOINTS[pos]
                    desenhaSorvete(x, y, valor)

                # paredes
                if r == 0 or not temAresta(pos, (r - 1, c)):
                    pygame.draw.line(screen, (0, 184, 197), (x, y), (x + tamCEL, y), 3)
                if r == linhasLabirinto - 1 or not temAresta(pos, (r + 1, c)):
                    pygame.draw.line(
                        screen, (0, 184, 197), (x, y + tamCEL), (x + tamCEL, y + tamCEL), 3
                    )
                if c == 0 or not temAresta(pos, (r, c - 1)):
                    pygame.draw.line(screen, (0, 184, 197), (x, y), (x, y + tamCEL), 3)
                if c == colunasLabirinto - 1 or not temAresta(pos, (r, c + 1)):
                    pygame.draw.line(
                        screen, (0, 184, 197), (x + tamCEL, y), (x + tamCEL, y + tamCEL), 3
                    )

    #------ Estado inicial de jogo ------#
    playerPos = [linhaOrigem, colunaOrigem]
    checkpointsVisitados = set()
    tempoInicial = time.time()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

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

                    if (
                        0 <= novo[0] < linhasLabirinto
                        and 0 <= novo[1] < colunasLabirinto
                        and (antigo, novo) in arestas
                    ):
                        
                        w = arestas[(antigo, novo)]
                        print(arestas)
                        playerPos[:] = list(novo)

                        nonlocal_currentXP = True  
                        currentXP += w
                        print(currentXP, w)
                        if currentXP < 0:
                            currentXP = 0
                            tempoFinal = time.time() - tempoInicial
                            print("Não conseguiu terminar")
                            print("Tempo:", round(tempoFinal, 2), "s")
                            return False, currentXP, round(tempoFinal, 2)

                        if novo in CHECKPOINTS and novo not in checkpointsVisitados:
                            # currentXP += CHECKPOINTS[novo]
                            # checkpointsVisitados.add(novo)
                            arestas[(antigo, novo)] = -1

                            print(CHECKPOINTS[novo])

                        if novo == posChegada:
                            tempoFinal = time.time() - tempoInicial
                            print("Fim do nível!")
                            print("Vida final:", currentXP)
                            print("Tempo:", round(tempoFinal, 2), "s")
                            return True, currentXP, round(tempoFinal, 2)

        # fundo
        screen.fill("#C7E2E4")

        # desenhar labirinto
        desenharLabirinto()

        # jogador
        px = labRECT.x + playerPos[1] * tamCEL + tamCEL // 2
        py = labRECT.y + playerPos[0] * tamCEL + tamCEL // 2
        pygame.draw.circle(screen, (255, 100, 100), (px, py), tamCEL // 3)
        desenhaBoneco(px, py)
        desenhaIglu()

        # HUD XP
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

        # HUD Tempo
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

        pygame.display.flip()
        clock.tick(60)
