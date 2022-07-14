from pygame import display, time, draw, QUIT, init, KEYDOWN, K_a, K_s, K_d, K_w
from random import randint
import pygame
from numpy import sqrt
init()

done = False
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)

colunas = 25
linhas = 25

largura = 600
altura = 600
wr = largura/colunas
hr = altura/linhas
direcao = 1

tela = display.set_mode([largura, altura])
display.set_caption("snake_self")
relogio = time.Clock()


def getpath(comida1, cobrinha1):
    comida1.camefrom = []
    for s in cobrinha1:
        s.camefrom = []
    openset = [cobrinha1[-1]]
    closedset = []
    dir_array1 = []
    while 1:
        atual1 = min(openset, key=lambda x: x.f)
        openset = [openset[i] for i in range(len(openset)) if not openset[i] == atual1]
        closedset.append(atual1)
        for neighbor in atual1.neighbors:
            if neighbor not in closedset and not neighbor.obstrucle and neighbor not in cobrinha1:
                tempg = neighbor.g + 1
                if neighbor in openset:
                    if tempg < neighbor.g:
                        neighbor.g = tempg
                else:
                    neighbor.g = tempg
                    openset.append(neighbor)
                neighbor.h = sqrt((neighbor.x - comida1.x) ** 2 + (neighbor.y - comida1.y) ** 2)
                neighbor.f = neighbor.g + neighbor.h
                neighbor.camefrom = atual1
        if atual1 == comida1:
            break
    while atual1.camefrom:
        if atual1.x == atual1.camefrom.x and atual1.y < atual1.camefrom.y:
            dir_array1.append(2)
        elif atual1.x == atual1.camefrom.x and atual1.y > atual1.camefrom.y:
            dir_array1.append(0)
        elif atual1.x < atual1.camefrom.x and atual1.y == atual1.camefrom.y:
            dir_array1.append(3)
        elif atual1.x > atual1.camefrom.x and atual1.y == atual1.camefrom.y:
            dir_array1.append(1)
        atual1 = atual1.camefrom
    #print(dir_array1)
    for i in range(linhas):
        for j in range(colunas):
            grid[i][j].camefrom = []
            grid[i][j].f = 0
            grid[i][j].h = 0
            grid[i][j].g = 0
    return dir_array1


class Spot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbors = []
        self.camefrom = []
        self.obstrucle = False
        if randint(1, 101) < 3:
            self.obstrucle = True

    def show(self, color):
        draw.rect(tela, color, [self.x*hr+2, self.y*wr+2, hr-4, wr-4])

    def add_neighbors(self):
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])
        if self.x < linhas - 1:
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.y < colunas - 1:
            self.neighbors.append(grid[self.x][self.y + 1])


grid = [[Spot(i, j) for j in range(colunas)] for i in range(linhas)]

for i in range(linhas):
    for j in range(colunas):
        grid[i][j].add_neighbors()

cobrinha = [grid[round(linhas/2)][round(colunas/2)]]
comida = grid[randint(0, linhas-1)][randint(0, colunas-1)]
atual = cobrinha[-1]
dir_array = getpath(comida, cobrinha)
comida_array = [comida]

while not done:
    relogio.tick(12)
    tela.fill(PRETO)
    direcao = dir_array.pop(-1)
    if direcao == 0:    # down
        cobrinha.append(grid[atual.x][atual.y + 1])
    elif direcao == 1:  # right
        cobrinha.append(grid[atual.x + 1][atual.y])
    elif direcao == 2:  # up
        cobrinha.append(grid[atual.x][atual.y - 1])
    elif direcao == 3:  # left
        cobrinha.append(grid[atual.x - 1][atual.y])
    atual = cobrinha[-1]

    if atual.x == comida.x and atual.y == comida.y:
        while 1:
            comida = grid[randint(0, linhas - 1)][randint(0, colunas - 1)]
            if not (comida.obstrucle or comida in cobrinha):
                break
        comida_array.append(comida)
        dir_array = getpath(comida, cobrinha)
    else:
        cobrinha.pop(0)

    for spot in cobrinha:
        spot.show(BRANCO)
    for i in range(linhas):
        for j in range(colunas):
            if grid[i][j].obstrucle:
                grid[i][j].show(VERMELHO)

    comida.show(VERDE)
    cobrinha[-1].show(AZUL)
    display.flip()
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
        elif event.type == KEYDOWN:
            if event.key == K_w and not direcao == 0:
                direcao = 2
            elif event.key == K_a and not direcao == 1:
                direcao = 3
            elif event.key == K_s and not direcao == 2:
                direcao = 0
            elif event.key == K_d and not direcao == 3:
                direcao = 1
