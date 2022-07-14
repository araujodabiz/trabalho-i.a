import pygame
import sys
import time

import tictactoe as ttt

pygame.init()
size = width, height = 600, 400

# Colors
preto = (0, 0, 0)
branco = (255, 255, 255)

screen = pygame.display.set_mode(size)

mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
largeFont = pygame.font.Font("OpenSans-Regular.ttf", 40)
moveFont = pygame.font.Font("OpenSans-Regular.ttf", 60)

user = None
tabela = ttt.estado_inicial()
ai_turno = False

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(preto)

    # Let user choose a player.
    if user is None:

        # Draw title
        title = largeFont.render("Jogo da velha", True, branco)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Draw buttons
        playXButton = pygame.Rect((width / 8), (height / 2), width / 3, 50)
        playX = mediumFont.render("Jogue como X", True, preto)
        playXRect = playX.get_rect()
        playXRect.center = playXButton.center
        pygame.draw.rect(screen, branco, playXButton)
        screen.blit(playX, playXRect)

        playOButton = pygame.Rect(5 * (width / 8), (height / 2), width / 3, 50)
        playO = mediumFont.render("Jogue como O", True, preto)
        playORect = playO.get_rect()
        playORect.center = playOButton.center
        pygame.draw.rect(screen, branco, playOButton)
        screen.blit(playO, playORect)

        # Check if button is clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if playXButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ttt.X
            elif playOButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ttt.O

    else:

        # Draw game board
        tile_size = 80
        tile_origin = (width / 2 - (1.5 * tile_size),
                       height / 2 - (1.5 * tile_size))
        tiles = []
        for i in range(3):
            linha = []
            for j in range(3):
                rect = pygame.Rect(
                    tile_origin[0] + j * tile_size,
                    tile_origin[1] + i * tile_size,
                    tile_size, tile_size
                )
                pygame.draw.rect(screen, branco, rect, 3)

                if tabela[i][j] != ttt.EMPTY:
                    move = moveFont.render(tabela[i][j], True, branco)
                    moveRect = move.get_rect()
                    moveRect.center = rect.center
                    screen.blit(move, moveRect)
                linha.append(rect)
            tiles.append(linha)

        game_over = ttt.terminal(tabela)
        jogador = ttt.jogador(tabela)

        # Show title
        if game_over:
            vencedor = ttt.vencedor(tabela)
            if vencedor is None:
                title = f"Deu velha: Empate."
            else:
                title = f"Deu velha: {vencedor} venceu."
        elif user == jogador:
            title = f"Jogue como {user}"
        else:
            title = f"Vez da IA..."
        title = largeFont.render(title, True, branco)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 30)
        screen.blit(title, titleRect)

        # Check for AI move
        if user != jogador and not game_over:
            if ai_turno:
                time.sleep(0.5)
                move = ttt.minimax(tabela)
                tabela = ttt.result(tabela, move)
                ai_turno = False
            else:
                ai_turno = True

        # Check for a user move
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and user == jogador and not game_over:
            mouse = pygame.mouse.get_pos()
            for i in range(3):
                for j in range(3):
                    if (tabela[i][j] == ttt.EMPTY and tiles[i][j].collidepoint(mouse)):
                        tabela = ttt.result(tabela, (i, j))

        if game_over:
            againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
            again = mediumFont.render("Jogue de novo", True, preto)
            againRect = again.get_rect()
            againRect.center = againButton.center
            pygame.draw.rect(screen, branco, againButton)
            screen.blit(again, againRect)
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = None
                    tabela = ttt.estado_inicial()
                    ai_turno = False

    pygame.display.flip()
