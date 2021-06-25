from random import random
import numpy as np
from collections import defaultdict
import pickle
import minesweeperheadless

# Learning Parameters
mines: int = 3
length: int = 5
width: int = 5
rewardAlive = 10
rewardKill = -10000
rewardWin = 10000
alpha = 0.02
gamma = 0.6

# Global Parameters
intervallsize: int = 10000
namespace = "Q420"
oldState = None
oldAction = (None, None)
oldParams = np.zeros(shape=(length, width), dtype=int)
Q = defaultdict(lambda: np.zeros(shape=(length, width), dtype=int))
wincounter: int = 0
gamecounter: int = 0
cords = []


def main():
    minesweeperheadless.main(shouldEmulateMove, onGameover, onWin, mines, length, width)



# Die save Methode wandelt das Defaultdict Q in ein normales dict um und speichert es binär in einer externen Datei.
# Zusätzlich werden die Daten, welche in der evaluate Methode erfasst werden, in einer weiteren Datei gespeichert.
def save():
    global namespace
    global gamecounter
    with open("F:\Q/" + namespace + "_" + str(gamecounter) + ".pickle", "wb") as file:
        pickle.dump(dict(Q), file)
    with open("Q_Evo/" + str(namespace) + "_evodata" + ".pickle", "wb") as fileevo:
        pickle.dump(cords, fileevo)



# Die load Methode ist zum Laden von gespeicherten Daten zuständig. Dazu muss der Methode ein Speicherstand
# mit Speicherpfad in Form eines Strings übergeben werden. Der Algorithmus lädt dann den Inhalt der Datei in
# das Defaultdict Q und lädt die passende Evodatei aus dem Q_Evo Ordner. Nun kann der Algorithmus wieder an
# dem geladenen Speicherstand weiterarbeiten.
def load(datei):
    global Q
    global cords
    with open(str(datei), "rb") as file:
        Q = defaultdict(lambda: np.zeros(shape=(length, width), dtype=int), pickle.load(file))
    with open("Q_Evo/" + str(namespace) + "_evodata.pickle", "rb") as file:
       cords = pickle.load(file)




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
                if not found: # Diese If-Abfrage dient dazu, das immer ein Wert gefunden wird.
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


# Bei dieser Methode handelt es sich um eine Variante der pick Methode, welche einen anderen Ansatz für das Auswählen
# der nächsten Aktion, also der pick Methode, vertritt. Sie verstößt zwar gegen das eigentliche Konzept des Q-Learning,
# jedoch sind die Ergebnisse nützlich, um zu prüfen wie viel Einfluss die Anzahl der erkundeten Zustände auf die
# Gewinnwahrscheinlichkeit hat. In dieser Variante werden alle möglichen Aktionen mit einer Wahrscheinlichkeit, welche
# von ihrer Bewertung abhängig ist, versehen. Danach wird anhand dieser Wahrscheinlichkeiten die nächste Aktion
# ausgewählt. Dadurch können schlechter bewertete Aktionen besser erkundet werden und eventuell eine höhere
# Gewinnwahrscheinlichkeit erzielt werden.
def picktest(reward, params):
    sum = 0
    rNum = random.random()
    for x in range(0, np.array(reward).shape[0]):
        for y in range(0, np.array(reward).shape[1]):
            if params[x][y] == 0:
                sum = sum+reward[x][y]+10000
    for x in range(0, np.array(reward).shape[0]):
        for y in range(0, np.array(reward).shape[1]):
            if params[x][y] == 0:
                if rNum < (reward[x][y]+10000)/sum:
                    return np.array([x, y])
                else:
                    rNum = rNum - (reward[x][y] + 10000) / sum


# Die onWin Methode wird aufgerufen, wenn ein Spiel gewonnen wurde. Das ist sehr wichtig, da die shouldEmulateMove
# Methode nur den Vorgängerstate aktualisiert, jedoch wird wenn das Spiel gewonnen ist, kein weiterer Zug für diese
# Epoche ausgeführt. Als erstes wird der der Counter um 1 erhöht, welcher die gewonnen Spiele zählt und anschließend
# wird die evaluate Methode aufgerufen. Nun werden die Gewichte des Vorgängerstates durch die  Q-Learning Formel
# aktualisiert. Hierbei kann jedoch die Formel gekürzt werden, weil der Agent in dieser Epoche keine weiteren States
# erreichen kann. Der Reward entspricht in diesem Fall dem Superparameter RewardWin Zusätzlich wird alles für ein neues
# Spiel vorbereitet.
def onWin():
    global oldState
    global oldAction
    global wincounter
    wincounter += 1
    evaluate()
    prevReward = Q[oldState]
    prevReward[oldAction[0]][oldAction[1]] = (1 - alpha) * prevReward[oldAction[0]][oldAction[1]] + \
                                             alpha * rewardWin
    oldState = None
    oldAction = (None, None)


# Wenn das Spiel verloren wurde, wird anstatt der onWin Methode die onGameover Methode aufgerufen. Jedoch wird der
# Wincounter nicht erhöht und die Gewichte des Vorgängerzustandes werden entsprechend der Niederlage aktualisiert.
def onGameover():
    global oldState
    global oldAction
    evaluate()
    prevReward = Q[oldState]
    prevReward[oldAction[0]][oldAction[1]] = (1 - alpha) * prevReward[oldAction[0]][oldAction[1]] + \
                                             alpha * rewardKill
    oldState = None
    oldAction = (None, None)



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
        cords.append([gamecounter, (wincounter / intervallsize)])
        save()
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



# Die shouldEmulateMove Methode dient dazu den Spieler zu simulieren. Sie ist also die Methode, die entscheidet,
# welcher Zug als nächstes ausgeführt wird. Dazu ermittelt sie über die paramsToState Methode den aktuellen State
# und referenziert die passenden Daten aus dem Defaultdict Q. Falls zu dem State noch keine Gewichte vorhanden sind,
# werden sie vom defaultdict mit Nullen initialisiert. Anhand der Gewichte des Vorgängerstates, der Aktion welche im
# letzten Zug gewählt wurde, den Superparametern, den Gewichten des aktuellen Zustandes und der Q-Learning Formel werden
# die Gewichte des Vorgängerstates aktualisiert. Nun wird durch die pick Methode die nächste Aktion bestimmt und zurück
# geliefert. Um die rekursiven Eigenschaften der Q-Learning Formel zu berechnen, speichert diese Methode immer den
# Aktuellen State, das Aktuelle Spielfeld und die gewählte Aktion für den Nächsten Zug. Diese Methode aktualisiert also
# immer den Vorgängerstate.
def shouldEmulateMove(params):
    global oldState
    global oldAction
    global oldParams
    state = paramsToState(params)
    estReward = Q[state]
    prevReward = Q[oldState] # prevReward referenziert jetzt auf Q[oldState]
    prevReward[oldAction[0]][oldAction[1]] = (1 - alpha) * np.array(prevReward[oldAction[0]][oldAction[1]]) + \
                                             alpha * (rewardAlive + gamma * estReward[pick(estReward, oldParams)[0]][
        pick(estReward, oldParams)[1]]) # Berechnung der Gewichte.
    oldState = state
    oldParams = params
    pos = pick(estReward, params)
    oldAction = pos
    return pos


if __name__ == "__main__":
    main()
