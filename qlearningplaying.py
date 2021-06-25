import numpy as np
from collections import defaultdict
import pickle
import minesweeperQ

# Learning Parameters
mines: int = 3
length: int = 5
width: int = 5
pfad =" "
# Global Parameters
intervallsize: int = 100
Q = defaultdict(lambda: np.zeros(shape=(length, width), dtype=int))
wincounter: int = 0
gamecounter: int = 0


def main():
    load(pfad)
    minesweeperQ.main(shouldEmulateMove, onGameover, onWin, mines, length, width)



# Die load Methode ist zum Laden von gespeicherten Daten zuständig. Dazu muss der Methode ein Speicherstand
# mit Speicherpfad in Form eines Strings übergeben werden. Der Algorithmus lädt dann den Inhalt der Datei in
# das Defaultdict Q.
def load(datei):
    global Q
    with open(str(datei), "rb") as file:
        Q = defaultdict(lambda: np.zeros(shape=(length, width), dtype=int), pickle.load(file))




# Die pick Methode ermittelt die am besten bewertete Aktion anhand der Gewichte des übergebenden Zustandes.
# Dazu werden nur die Gewichte aus dem aktuellen State in Betracht gezogen, welche zu noch möglichen Zügen
# gehören. Die möglichen Züge werden anhand des numbers Array ermittelt. Dazu wird eine verschachtelte For-Schleife
# durchlaufen, welche überprüft, ob im numbers Feld eine 0 steht. Die 0 bedeutet, dass dieses Feld noch nicht
# aufgedeckt ist und die Aktion noch zur Wahl steht. Nachdem die For-Schleife beendet ist, steht in der Index-Variable
# die Koordinate der ausgewählten Aktion. Diese Koordinate wird dann zurückgegeben.
def pick(reward, params):
    found = False
    index = np.empty(dtype=int, shape=2)
    for x in range(0, np.array(reward).shape[0]):
        for y in range(0, np.array(reward).shape[1]):
            if params[x][y] == 0:
                if not found:
                    found = True
                    maximum = reward[x][y]
                    index[0] = x
                    index[1] = y
                if maximum <= reward[x][y]:
                    maximum = reward[x][y]
                    index = np.array([x, y])

    if not found:
        print("Fail: Found = false")
    return index



# Diese Methode dient der Dokumentierung der gewonnenen spiele. Zusätzlich ruft sie noch die Evaluate-Methode auf.
def onWin():
    global wincounter
    wincounter += 1
    evaluate()



# Diese methode ruft nurnoch die Evaluete methode auf.
def onGameover():
    evaluate()




# Die evaluate Methode dient zur Erfassung von der Gewinnrate und ruft die save Methode nach einer gewissen Anzahl
# von Spielen auf. Dabei werden der cords Variable die Gewinnrate und die Anzahl der bis jetzt gespielten Spiele
# angehangen. Diese Variable wird später vom Analysetool zur Auswertung benötigt. Zusätzlich wird der Wincouter für
# das kommende Intervall wieder auf null gesetzt.
def evaluate():
    global wincounter
    global gamecounter
    gamecounter += 1
    if gamecounter % intervallsize == 0: # Diese If-Abfrage sorgt dafür das nur alle x Runden gespeichert und evaluiert wird.
        print(str(gamecounter) + ": " + str(wincounter / intervallsize))
        wincounter = 0



# Die paramsToState Methode wandelt den aktuellen Zustand des Spielfeldes in einen einheitlichen State um.
# Dazu wird ihr das numbers Array der Minesweeper Klasse von der shouldEmulateMove Methode übergeben. Dieses
# Array wird durchiteriert und die Inhalte werden mit einem "_" getrennt in einen String geschrieben. Dieser wird dann
# zurück gegeben. Er wird als Schlüssel für das Defaultdict genommen.
def paramsToState(params):
    state = ""
    for j in range(0, np.array(params).shape[0]):
        for i in range(0, np.array(params).shape[1]):
            state = state + str(params[j][i]) + "_"
    state = state[:-1] #Listslicing: Letzer Buchstabe wird abgeschnitten da dieser ein _ ist und nicht benötigt wird.
    return state



#Bei der souldEmulateMove Methode wurden ebenfalls alle zur Berechnung dienenden Zeilen entfernt.
# Sie sucht nun noch anhand des Aktuellen States die nächste Aktion aus.
def shouldEmulateMove(params):
    pos = pick(Q[paramsToState(params)], params)
    return pos



if __name__ == "__main__":
    main()
