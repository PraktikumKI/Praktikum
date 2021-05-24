import numpy as np
import random
from termcolor import colored



class Minesweeper:
    mines: int #anzahl der Minen
    numbers: np.empty_like #Array welches in welchem die aufgedeckten felder gespeichert werden.
    minefield: np.empty_like # Array welches die Position der minen enthält
    length: int #länge des Spielfeldes
    width: int #breite des Spielfeldes
    first: bool #Zustandsvariable welche angibt ob es sich um den ersten zug des Spieles handelt

    def __init__(self, mines, length, width):
        self.mines = mines
        self.length = length
        self.width = width
        self.first = True
        self.numbers = np.zeros(shape=(self.length, self.width), dtype=int)
        self.minefield = np.zeros(shape=(self.length, self.width), dtype=bool)

    def generate(self, z, y):
        self.first = False
        random.seed()
        a: int
        b: int
        x: int = 0
        while x < self.mines:
            a = random.randrange(0, self.length)
            b = random.randrange(0, self.width)
            if a == z and b == y:
                continue
            elif self.minefield[a][b]:
                continue
            else:
                self.minefield[a][b] = True
                x = x + 1
        return self.reveal(z, y)

    def printMinefield(self):
        for j in range(0, self.length):
            for i in range(0, self.width):
                if self.minefield[j][i]:
                    print("[" + colored('X', 'red') + "]\u0009", end="")
                else:
                    print("[ ]\u0009", end="")
            print()

    def printNumbersAndMines(self):
        for j in range(0, self.length):
            for i in range(0, self.width):
                if self.minefield[j][i]:
                    print("[" + colored('X', 'red') + "]\u0009", end="")
                elif self.numbers[j][i] == -1:
                    print("[-]\u0009", end="")
                elif self.numbers[j][i] == 0:
                    print("[ ]\u0009", end="")
                else:
                    print("[" + str(int(self.numbers[j][i])) + "]\u0009", end="")
            print()

    def printNumbers(self):
        for j in range(0, self.length):
            for i in range(0, self.width):
                if self.numbers[j][i] == -1:
                    print("[-]\u0009", end="")
                elif self.numbers[j][i] == 0:
                    print("[ ]\u0009", end="")
                else:
                    print("[" + str(int(self.numbers[j][i])) + "]\u0009", end="")
            print()

    def revealMinefield(self):
        for j in range(0, self.length):
            for i in range(0, self.width):
                self.setNumber(j, i)

    def setNumber(self, a, b):
        if self.minefield[a][b]:
            return -1
        count: int = 0
        for x in range(a - 1, a + 2):
            for q in range(b - 1, b + 2):
                if x < 0 or q < 0 or x >= self.length or q >= self.width:
                    continue
                if self.minefield[x][q]:
                    count = count + 1
        if count != 0:
            self.numbers[a][b] = count
        else:
            self.numbers[a][b] = -1
        return count

    def reveal(self, a, b):
        v = self.setNumber(a, b)
        if v == -1:
            return -1
        if v == 0:
            for x in range(a - 1, a + 2):
                for q in range(b - 1, b + 2):
                    if x < 0 or q < 0 or x >= self.length or q >= self.width:
                        continue
                    if x == a and q == b:
                        continue
                    if self.numbers[x][q] == 0:
                        self.reveal(x, q)
        win = True
        for j in range(0, self.length):
            for i in range(0, self.width):
                if self.numbers[j][i] == 0 and not self.minefield[j][i]:
                    win = False
        if win:
            return 1
        return 0

    def reset(self):
        self.first = True
        self.numbers = np.zeros(shape=(self.length, self.width), dtype=int)
        self.minefield = np.zeros(shape=(self.length, self.width), dtype=bool)

    def move(self, a, b):
        if self.first:
            return self.generate(a, b)
        else:
            return self.reveal(a, b)

    def gameloop(self, shouldEmulateMove, onGameover, onWin):
        while True:
            t = shouldEmulateMove(self.numbers)
            result = self.move(int(t[0]), int(t[1]))
            if 0 != result:
                if result == 1:
                    self.reset()
                    onWin()
                elif result == -1:
                    self.reset()
                    onGameover()




def main(shouldEmulateAction, onGameover, onWin, mines, length, width):
    minesweeper = Minesweeper(mines, length, width)
    minesweeper.gameloop(shouldEmulateAction, onGameover, onWin)


if __name__ == '__main__':
    main(lambda x: 0, lambda x: 0, lambda x: 0, lambda x: 0, lambda x: 0, lambda x: 0)
