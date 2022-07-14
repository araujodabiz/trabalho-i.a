"""
Jogo da velha
"""

import math
import copy
import time

X = "X"
O = "O"
EMPTY = None


def estado_inicial():
    """
    Retorna o estado inicial.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def jogador(tabela):
    """
    Retorna jogador que tem a próxima volta em uma placa.
    """
    # Verifique o estado inicial
    if tabela == estado_inicial():
        return X
   #elif terminal(tabela): ## Falta chequear esto
   #     raise NotImplementedError
    else:
        # Count None: if there are an even number of "nones" -> ist turn of the "O" Player
        nones = [x.count(None) for x in tabela]
        if ((nones[0]+nones[1]+nones[2]) % 2) == 0:
            return O
        else:
            return X
        #raise NotImplementedError


def acoes(tabela):
    """
    Conjunto de devoluções de todas as ações possíveis (i, j) disponíveis no quadro.
    """
    opcoes = set()
    tabela2Test = copy.deepcopy(tabela)
    for x,y in enumerate(tabela2Test):
        for w,z in enumerate(y):
            if z == None:
                opcoes.add((x,w))
    
    return opcoes 



def result(tabela, acao):
    """
    Retorna a diretoria que resulta de fazer movimento (i, j) no tabuleiro.
    """

    # Verifique se a ação é uma ação possível
    if acao not in acoes(tabela):
        raise NameError('Action not correct')

    # Faça cópia profunda, chek player e substitua ação por jogadores
    tabela2 = copy.deepcopy(tabela)
    tabela2[acao[0]][acao[1]] = jogador(tabela)
    return tabela2
    


def vencedor(tabela):
    """
Retorna o vencedor do jogo, se houver um.
    """
    if (tabela[1][1]==tabela[0][0]) and (tabela[1][1]==tabela[2][2]) or (tabela[1][1]==tabela[0][2]) and (tabela[1][1]==tabela[2][0]) \
    or (tabela[1][1]==tabela[1][0]) and (tabela[1][1]==tabela[1][2]) or (tabela[1][1]==tabela[0][1]) and (tabela[1][1]==tabela[2][1]):
            win = tabela[1][1]
    elif (tabela[0][1]==tabela[0][0]) and (tabela[0][1]==tabela[0][2]):
        win = tabela[0][1]
    elif (tabela[2][1]==tabela[2][0]) and (tabela[2][1]==tabela[2][2]):
        win = tabela[2][1]
    elif (tabela[1][0]==tabela[0][0]) and (tabela[1][0]==tabela[2][0]):
        win = tabela	[1][0]
    elif (tabela[1][2]==tabela[0][2]) and (tabela[1][2]==tabela[2][2]):
        win = tabela[1][2]
    else:
        win = None
    return win

def terminal(tabela):
    """
    Retorna Verdadeiro se o jogo acabar, falso de outra forma.

    O jogo acabou se houver um vencedor ou se não houver opções
    """
    if (vencedor(tabela) != None) or len(acoes(tabela)) == 0:
        return True
    else:
        return False



def utilitario(tabela):
    """
    Retorna 1 se X ganhou o jogo, -1 se O ganhou, 0 caso contrário.
    """
    if vencedor(tabela)== X:
 
        return 1
        
    elif vencedor(tabela) == O:
        return -1
        
    else:
        return 0


def minimax(tabela):
    """
    Retorna a ação ideal para o jogador atual no tabuleiro.

    """
    if jogador(tabela) == X:
        # MAX PLAYER
        opcoes = acoes(tabela)
        opcoeslist= []
        valores = []
        for op in opcoes:
            valores.append(minValor(result(tabela,op)))
            opcoeslist.append(op)
        return opcoeslist[valores.index(max(valores))]
             

    elif jogador(tabela) == O:
        # MIN PLAYER
        opcoes = acoes(tabela)
        valores = []
        opcoeslist = []
        for op in opcoes:
            valores.append(maxValor(result(tabela,op)))
            opcoeslist.append(op)
        return opcoeslist[valores.index(min(valores))]



def minValor(tabela):
    if terminal(tabela):
        a = utilitario(tabela)
        return a
    else:
        v = 10
        for acao in acoes(tabela):
            v = min(v,maxValor(result(tabela,acao)))
        return  v    


def maxValor(tabela):
    if terminal(tabela):
        a = utilitario(tabela)
        return a
    else:
        v = -10
        for acao in acoes(tabela):
            v = max(v,minValor(result(tabela,acao)))
        return  v 
