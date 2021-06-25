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

    # In der __init__-Methode werden alle relevanten Variabelen vordefiniert.
    def __init__(self, mines, length, width):
        self.mines = mines
        self.length = length
        self.width = width
        self.first = True
        self.numbers = np.zeros(shape=(self.length, self.width), dtype=int)
        self.minefield = np.zeros(shape=(self.length, self.width), dtype=bool)

    # Die generate Methode ist für die Zufallsgenerierung des Minenfelds zuständig
    # und macht den ersten Zug anhand der Eingabeparameter. Für die
    # Zufallsgenerierung wird das Package Random genutzt. Da beim ersten Zug keine
    # Mine getroffen werden darf, wird bei der Generierung eine neue Position für
    # Minen bestimmt, wenn diese die gleichen Koordinaten haben wie die Koordinaten
    # des ersten Zuges oder einer bereits platzierten Mine. Nachdem die Generierung
    # abgeschlossen ist, wird die reveal Methode mit den passenden Parametern
    # aufgerufen und das Ergebnis als Rückgabewert übergeben.
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

    # Die printNumbers-Methode iteriert mithilfe einer verschachtelten For-Schleife das
    # numbers Array und gibt das aktuelle aufgedeckte Spielfeld auf der Konsole aus.

    def printNumbers(self):
        for j in range(0, self.length):
            for i in range(0, self.width):
                if self.numbers[j][i] == -1:
                    print("[-]\t", end="")  # \t ist der Abstand zum nächsten Feld
                elif self.numbers[j][i] == 0:
                    print("[ ]\t", end="")
                else:
                    print("[" + str(int(self.numbers[j][i])) + "]\t", end="")
            print()

    # Die printMinefield-Methode geht wie die printNumbers Methode for jedoch gibt es das Spielfeld mit den
    # Minen, welche durch ein Rotes X Symbolisiert werden, auf der Konsole aus.

    def printMinefield(self):
        for j in range(0, self.length):
            for i in range(0, self.width):
                if self.minefield[j][i]:
                    print("[" + colored('X', 'red') + "]\t", end="")
                else:
                    print("[ ]\t", end="")
            print()

    # Diese Methode ist eine Kombination aus den Methoden printMinefield und printNumbers. Sie wird
    # in der Version von Minesweeper mit visueller Ausgabe benutzt, wenn keine Züge mehr möglich sind.
    def printNumbersAndMines(self):
        for j in range(0, self.length):
            for i in range(0, self.width):
                if self.minefield[j][i]:
                    print("[" + colored('X', 'red') + "]\t", end="")
                elif self.numbers[j][i] == -1:
                    print("[-]\t", end="")
                elif self.numbers[j][i] == 0:
                    print("[ ]\t", end="")
                else:
                    print("[" + str(int(self.numbers[j][i])) + "]\t", end="")
            print()

    # Die Methode revealMinefield führt auf jedem Feld die setNumber Methode aus.
    # Dadurch wird das ganze Feld aufgedeckt.
    def revealMinefield(self):
        for j in range(0, self.length):
            for i in range(0, self.width):
                self.setNumber(j, i)

    # Die setNumber Methode zählt die Anzahl der Bomben, welche in der direkten Nachbarschaft eines,
    # anhand von Koordinaten übergebenen, Feldes versteckt sind. Sie trägt diese Anzahl in das Numbers
    # Array ein und gibt die Anzahl als Rückgabewert zurück. Falls keine Minen in der direkten Nachbarschaft
    # gefunden werden, wird anstelle der Anzahl -1 in das Array geschrieben. Dies muss gemacht werden, da
    # die 0 symbolisch für nicht aufgedeckte Felder steht.
    def setNumber(self, a, b):
        if self.minefield[a][b]:
            return -1
        count: int = 0
        # Die folgende verschachtelte For-Forschleife durchläuft alle 8 umliegenden Nachbarfelder
        for x in range(a - 1, a + 2):
            for q in range(b - 1, b + 2):
                # Diese If abfrage überspringt Koordinaten, welche nicht auf dem Spielfeld liegen würden
                if x < 0 or q < 0 or x >= self.length or q >= self.width:
                    continue
                if self.minefield[x][q]:
                    count = count + 1
        # Der folgende Block übersetzt die count-Variable in die richtige Ausgabe
        if count != 0:
            self.numbers[a][b] = count
        else:
            self.numbers[a][b] = -1
        return count

    # Die reveal Methode ist eine rekursive Methode, welche aufgerufen wird, wenn ein Spieler ein Feld aufdeckt.
    # Ihr wird dazu die Koordinaten des vom Spieler gewählten Feldes übergeben. Mit diesen Koordinaten wird
    # dann die setNumber Methode ausgeführt und anhand der Rückgabe das weitere Vorgehen entschieden. Liefert
    # die setNumber Methode eine 0, wird die reveal Methode auf alle nicht aufgedeckten Nachbarfelder ausgeführt.
    # Wenn die setNumber Methode eine -1 zurück liefert, liefert die reveal Methode ebenfalls eine -1 zurück.
    # Dies wird gemacht, da die -1 der setNumber Methode bedeutet, dass das gewählte Feld eine Mine verborgen
    # hat. Die Rückgabe der reveal Methode steht jedoch für den aktuellen Spielstatus, welcher wenn eine Mine
    # aufgedeckt wurde "Game Over" bedeutet. Um heraus zu finden, ob das das Spiel nach dem Aufdecken
    # gewonnen wurde, wird am Ende der Methode das Array durchlaufen und geprüft, ob auf dem Spielfeld noch
    # nicht aufgedeckte Felder existieren, welche keine Bombe verstecken. Ist dies der Fall, wird 0
    # zurückgegeben, da der Spieler noch nicht gewonnen hat. Falls der Spieler jedoch alle richtigen Felder
    # aufgedeckt hat, wird eine 1 zurück gegeben.

    def reveal(self, a, b):
        v = self.setNumber(a, b)
        # Diese If-Abfrage prüft ob eine Mine getroffen wurde.
        if v == -1:
            return -1
        # Diese If-Abfrage wird ausgeführt wenn keine Mine in der Nachbarschaft liegt.
        if v == 0:
            # Die folgende verschachtelte For-Forschleife durchläuft alle 8 umliegenden Nachbarfelder
            for x in range(a - 1, a + 2):
                for q in range(b - 1, b + 2):
                    # Diese If abfrage überspringt Koordinaten, welche nicht auf dem Spielfeld liegen würden
                    if x < 0 or q < 0 or x >= self.length or q >= self.width:
                        continue
                    # Diese If abfrage überspringt Koordinaten, welche bereits aufgedeckt wurden, um eine
                    # Endlosschleife zu vermeiden
                    if x == a and q == b:
                        continue
                    if self.numbers[x][q] == 0:
                        self.reveal(x, q)
        # Der folgende Block überprüft ob auf dem Spielfeld noch nicht aufgedeckte Felder existieren, welche
        # keine Bombe verstecken. Falls ein solches Feld existiert wird 0 zurückgegeben, falls nicht wird 1 zurückgegeben.
        win = True
        for j in range(0, self.length):
            for i in range(0, self.width):
                if self.numbers[j][i] == 0 and not self.minefield[j][i]:
                    win = False
        if win:
            return 1
        return 0

    # Wird die reset Methode aufgerufen, wird das Spiel automatisch in den Zustand zurück gebracht, den das Spiel hatte,
    # nachdem es gestartet wurde. Dazu werden die Felder numbers und minefield zurückgesetzt und die first variable,
    # welche für die move Methode wichtig ist, auf True gesetzt. Diese Methode wird am ende einer Epoche, also wenn das
    # Spiel entweder gewonnen oder verloren wurde, ausgeführt.
    def reset(self):
        self.first = True
        self.numbers = np.zeros(shape=(self.length, self.width), dtype=int)
        self.minefield = np.zeros(shape=(self.length, self.width), dtype=bool)

    # Diese Methode wird aufgerufen, wenn der Spieler einen Zug macht. Je nachdem, ob es der erste Zug des Spieles bzw.
    # der Epoche ist oder nicht, wird die passende Methode aufgerufen. Wenn es sich um den ersten Zug handelt, wird die
    # generate Methode aufgerufen. Falls dies nicht der Fall ist, wird die reveal Methode aufgerufen. In beiden Fällen
    # werden die Eingabeparameter der move Methode an die entsprechende Methode übergeben.
    def move(self, a, b):
        if self.first:
            return self.generate(a, b)
        else:
            return self.reveal(a, b)

    # In dieser Version der Gameloop Methode wurden alle Konsolenoutputs entfernt, da diese für den Q-Learning
    # Algorithmus nur Laufzeit bedeuten und nicht von Nutzen sind. Zusätzlich wurden die Konsoleninputs durch die
    # Methode shouldEmulateMove ersetzt, da die Wahl des Zuges nun vom Q-Learning Agenten bestimmt werden.
    # Um den Q-Learning Algorithmus noch informationen über Sieg oder Niederlage eines Spiel zu informieren,
    # wurden die onWin und onGameover Methoden hinzugefügt.
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
