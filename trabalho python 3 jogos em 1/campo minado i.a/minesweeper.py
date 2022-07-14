import itertools
import random


class Minesweeper():
    """
    representacao do campo minado
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Inicialize um campo vazio sem minas
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Adicione minas de forma aleatoria
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # No início, o jogador não encontrou minas
        self.mines_found = set()

    def print(self):
        """
        Imprime uma representação baseada em texto
        de onde as minas estão localizadas.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Retorna o número de minas que são
        dentro de uma linha e coluna de uma determinada célula,
        não incluindo a célula em si.
        """

        # Mantenha a contagem de minas próximas
        count = 0

        # Loop sobre todas as células dentro de uma linha e coluna
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore a célula em si
                if (i, j) == cell:
                    continue

                # Contagem de atualizações se célula nos limites e é minha
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Declaração lógica sobre um jogo de campo minado
    Uma frase consiste em um conjunto de células de tabuleiro,
    e uma contagem do número dessas células que são minas.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Retorna o conjunto de todas as células em auto-células conhecidas como minas.
        """
        if len(self.cells) == self.count:
            return self.cells
        else:
            return set()
        

    def known_safes(self):
        """
        Retorna o conjunto de todas as células em células auto-conhecidas como seguras.
        """
        if self.count == 0:
            return self.cells
        else:
            return set()
        

    def mark_mine(self, cell):
        """
        Atualiza a representação do conhecimento interno dado o fato de que
        uma célula é conhecida por ser uma mina.
        """

        if cell in self.cells: # First check if cell in sentence
            self.cells.remove(cell) # Remove cell from sentence
            self.count -= 1 # There is one mine less in sentence 
            #print(cell)
        

    def mark_safe(self, cell):
        """
        Atualiza a representação do conhecimento interno dado o fato de que
        uma célula é conhecida por ser segura.
        """
        if cell in self.cells: # First check if cell in sentence
            self.cells.remove(cell) # Remove cell from sentence
            #print(cell)

        


class MinesweeperAI():
    """
    campo minado game player
    """

    def __init__(self, height=8, width=8):

        # Definir altura e largura iniciais
        self.height = height
        self.width = width

        # Mantenha o controle de quais células foram clicadas em
        self.moves_made = set()

        # Mantenha o controle de células conhecidas por serem seguras ou minas
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marca uma célula como uma mina, e atualiza todo o conhecimento
        para marcar essa célula como uma mina também.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marca uma célula como segura e atualiza todo o conhecimento
        para marcar essa célula como segura também.
        """
        self.safes.add(cell)
        for sentence in self.knowledge.copy():
            sentence.mark_safe(cell)
            if len(sentence.cells) == 0:
                self.knowledge.remove(sentence)

    def add_knowledge(self, cell, count):
        """
        Chamado quando o conselhocampo minado nos diz, para um dado
        célula segura, quantas células vizinhas têm minas nelas.

        Esta função deve:
            1) marcar a célula como um movimento que foi feito

            2) mark the cell as safe
            3) adicionar uma nova frase à base de conhecimento da IA
               com base no valor de 'célula' e 'contagem'
            4) marcar quaisquer células adicionais tão seguras ou como minas
               se ele pode ser concluído com base na base de conhecimento da IA
            5) adicionar quaisquer novas frases à base de conhecimento da IA
               se eles podem ser inferidos a partir do conhecimento existente
        """
        
        #1) marcar a célula como um movimento que foi feito
        self.moves_made.add(cell)
        #2) marcar a célula como segura
        # Atualize todas as frases em conhecimento, agora esta célula sabe ser segura
        self.mark_safe(cell)
        # 3) Nova frase: conjunto de células em torno de células atuais e contagem de minas
        fullSentence = self.agregarCeldas(cell)
        # Eu checo o número de células na declaração que já são conhecidas por serem minas
        minas = len(list(itertools.takewhile(lambda i:i in self.mines, fullSentence)))
        # Resto la(s) mina(s) ya conocida(s) en count
        count = count - minas
        # Eu removo do conjunto as células que eu já sei que são minas.
        cleanSentence = set(itertools.dropwhile(lambda i:i in self.mines, fullSentence))
        # Eu removo células que eu já sei que estão a salvo do conjunto
        cleanSentence = set(itertools.dropwhile(lambda i:i in self.safes, cleanSentence))
        # Eu adiciono a frase limpa ao conhecimento básico
        self.knowledge.append(Sentence(cleanSentence,count))

        '''
        Se, com base em qualquer uma das frases em autoconhecimento, 
        novas células podem ser marcadas como seguras ou como minas, então a função deve fazê-lo.
        Se, com base em qualquer uma das frases em autoconhecimento, 
        novas frases podem ser inferidas (usando o método de subconjunto descrito no Fundo),
        então essas frases devem ser adicionadas à base de conhecimento também.

        
        Para cada sentencia individual (ahora actualizadas)
        Verificar: 
        1)executar known_mines
        Dentro de known mines: si len(set) = count -> todas son minas
        Para cada célula faça a markMine, que re-modifica todos 
        os julgamentos no banco de dados
        2) executar known_safes
        Dentro de known_safes: si count == 0 -> todas a salvo
        Para cada celda hacer el markSafe, que modifica los registros


        Para cada una de las permutaciones (o combinaciones, ver que conviene) entre las sentencias
        de la base de datos, verificar si algún set está incluido en otro set. De ser así, generar 
        una nueva sentencia set2 - set1 = count2 - count1

        Si se generó una nueva secuencia, repetir 1 2 3 en loop.

        '''
        cambios = True
        while cambios:
            cambios = False
            for sentence in self.knowledge:
                nuevasMinas = sentence.known_mines()
                if len(nuevasMinas) != 0:
                    for mina in nuevasMinas.copy():
                        self.mark_mine(mina)
                        cambios = True
                else:
                    nuevasSalvo = sentence.known_safes()
                    if len(nuevasSalvo) != 0:
                        for safe in nuevasSalvo.copy():
                                self.mark_safe(safe)
                                cambios = True
             

            #   Anula a Sentença Limpa
            for i in self.knowledge.copy():
                if len(i.cells)== 0:
                    self.knowledge.remove(i)
                
            if len(self.knowledge)>1:               
                for i in list(itertools.permutations(self.knowledge.copy())):
                    if i[0].cells.issubset(i[1].cells):
                        #print(i[0].cells)
                       # print(i[1].cells)
                        self.knowledge.append(Sentence(i[1].cells.difference(i[0].cells),i[1].count-i[0].count))
                        #print(i[1].cells.difference(i[0].cells))
                        self.knowledge.remove(Sentence(i[1].cells, i[1].count))
                        cambios = True
                        break
                    #print(self.knowledge)
    def agregarCeldas(self,celda):
        
        celdas = set()
        if celda[0] == self.width-1:
            x = [celda[0]-1,celda[0]]
        elif celda[0] == 0:
            x = [celda[0],celda[0]+1]
        else:
            x = [celda[0]-1, celda[0],celda[0]+1]

        if celda[1] == self.height-1:
            y = [celda[1]-1,celda[1]]
        elif celda[1] == 0:
            y = [celda[1],celda[1]+1]
        else:
            y = [celda[1]-1, celda[1],celda[1]+1]

        for xx in x:
            for yy in y:
                a = (xx,yy)
                if a != celda:
                    celdas.add(a)
        
        return celdas

    def make_safe_move(self):
        """
        Retorna uma célula segura para escolher no quadro Minesweeper.
        A mudança deve ser conhecida por ser segura, e ainda não um movimento
        que foi feito.

Esta função pode usar o conhecimento em auto.mines, self.safes
        e self.moves_made, mas não devem modificar nenhum desses valores.

Retornarnar algun tupla que esté en safe y no esté en yausados
        Si no feno, Nenhum
        """
        if len(list(self.safes.difference(self.moves_made))) == 0:
            return None
        else:
            #print(list(self.safes.difference(self.moves_made))[0])
            #time.sleep(1)
            return list(self.safes.difference(self.moves_made))[0]

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        todo = set()
        for i in range(self.height):
            for j in range(self.width):
                todo.add((i,j))
        todo = todo.difference(self.mines)
        todo = todo.difference(self.moves_made)
        if len(todo) == 0:
            return None
        else:
            x = todo.pop()
            ##print(x)
            #time.sleep(1)
            return x

