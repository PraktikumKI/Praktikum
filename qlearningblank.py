import numpy as np
from collections import defaultdict
import pickle
import minesweeperheadless

# Learning Parameters
rewardAlive = 0 #Belohung im fall das der Agent keine Mine getroffen hat
rewardKill = 0 #Belohung im fall das der Agent eine Mine getroffen hat
rewardWin = 0 #Belohung im fall das der Agent ein Spiel gewonnen hat
alpha = 0
gamma = 0

# Global Parameters
mines: int = 3
length: int = 5
width: int = 5
namespace = ""  # Wird mit "Q" + eine Nummer angegeben bsp: "Q1"
Q = defaultdict(lambda: np.zeros(shape=(length, width), dtype=int))
cords = []


# TODO ADD MISSING PARAMETERS

def main():
    minesweeperheadless.main(shouldEmulateMove, onGameover, onWin, mines, length, width)


def save():
    global namespace
    with open("Q_Evo/" + str(namespace) + "_evodata" + ".pickle", "wb") as fileevo:
        pickle.dump(cords, fileevo)
    # TODO FINISH THIS METHOD
    #  Speichern der Q-Daten


def load():
    global cords
    with open("Q_Evo/" + str(namespace) + "_evodata.pickle", "rb") as file:
        cords = pickle.load(file)
    # TODO FINISH THIS METHOD
    #  Laden der Q-Daten


def pick(reward, params):
    # TODO IMPLEMENT THIS METHODE
    #  Die pick Methode ermittelt die am Besten bewertete Aktion anhand der gewichte
    #  des übergebenden Zustandes heraus. Dazu werden nur die Gewichte aus dem
    #  aktuellen State in Betracht gezogen.
    pass


def onWin():
    # TODO IMPLEMENT THIS METHODE
    #  Die onWin Methode wird aufgerufen wenn ein Spiel gewonnen wurde. Das ist sehr
    #  wichtig da die shouldEmulateMove Methode nur den Vorgängerstate aktualisiert
    #  jedoch wird wenn das Spiel gewonnen ist kein weiterer Zug, für diese Epoche,
    #  ausgeführt. Zusätzlich ruft diese methode noch die evaluate methode auf.
    pass


def evaluate():
    # TODO IMPLEMENT THIS METHODE
    #  Die evaluate Methode dient zur Erfassung von der Gewinnrate und ruft die
    #  save Methode nach einer gewissen Anzahl von Spielen auf. In dieser Methode
    #  werden die Evaluationsdaten in cords aufgenommen.
    cords.append(["""Spieleanzahl, Gewinnwahrscheinlichkeit"""])

    pass


def onGameover():
    # TODO IMPLEMENT THIS METHODE
    #  Wie die onWin Methode jedoch wird diese Methode aufgerufen wenn ein Spiel
    #  verloren ist.
    pass


def paramsToState(params):
    # TODO IMPLEMENT THIS METHODE
    #  Der paramsToState Methode wandelt den aktuellen Zustand des Spielfeldes
    #  in einen einheitlichen State um. Dazu wird ihr das numbers Array der
    #  Minesweeper klasse von der souldEmulateMove Methode übergeben. Dieses
    #  Array wird durch Iteriert und die Inhalte werden mit einem _ getrennt
    #  in einen String geschrieben. Dieser wird dann zurück gegeben.
    pass



def shouldEmulateMove(params):
    # TODO IMPLEMENT THIS METHODE
    #  Die shouldEmulateMove Methode dient dazu den Spieler zu simulieren.
    #  Sie ist also die Methode die entscheidet welcher Zug als nächstes
    #  ausgeführt wird. Dazu ermittelt sie über die paramsToState Methode
    #  den aktuellen State und referenziert die passenden Daten aus dem
    #  Defaultdict Q. Falls zu dem State noch keine Gewichte vorhanden
    #  sind werden sie vom defaultdict mit Nullen initialisiert. An Hand
    #  der Gewichte des Vorgängerstates, der Aktion welche im letzten Zug
    #  gewählt wurde, den Superparametern, den Gewichten des Aktuellen
    #  Zustandes und der Q-Learning Formel (siehe Übungsblatt) werden die Gewichte des
    #  Vorgängerstates aktualisiert. Nun wird durch die pick Methode die
    #  nächste Aktion bestimmt und zurück geliefert. Um die rekursiven
    #  Eigenschaften der Q-Learning Formel zu berechnen speichert diese
    #  Methode immer den Aktuellen State, das Aktuelle Spielfeld und die
    #  gewählte Aktion für den Nächsten Zug. Diese Methode Aktualisiert
    #  also immer den Vorgängerstate.

    pos = np.empty(dtype=int, shape=2)  # steht symbolisch für die Position die eigentlich übergeben wird

    return pos


if __name__ == "__main__":
    main()
