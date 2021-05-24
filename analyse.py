import numpy as np
import matplotlib.pyplot as plt
import pickle
import sys

allcords =[]
def main():
    while(True):
        if(int(input("Wollen sie \n 1: die Lernkurve von einen oder mehreren Tests anzeigen \n 2: die Zustände eines Speicherstand anzeigen:"))==1):
            x = list(map(int, input("Welche Tests?:").split()))
            y = int(input("Die ersten wieviel Punkte willst du analysieren?:"))
            load(*x)
            analyse(y)
        else:
            statecount(input("Pfad des Speicherstandes angeben:"))
        if (int(input("Wollen sie \n 1: erneut eine Aktion ausführen \n 2: Das Programm beenden :")) == 2):
            sys.exit("Programm beendet")


def load( *x):
    allcords.clear()
    for number in x:
        with open(str("Q_Evo/" + "Q" + str(number) + "_e"
                                                     "vodata" + ".pickle"), "rb") as file:
            cords = pickle.load(file)
            allcords.append(["Q" + str(number), cords])

def analyse(limit =-1):
    title = ""
    #print(allcords)
    for cords in allcords:
        tag = cords[0]
        title += str(tag) + ", "
        cords = np.array(cords[1])
        print("Maximum von " + str(tag[:]) + " auf den ersten " + str(limit) + " Punkten:" + str(max(cords[: int(limit), 1])))
        print("Durchschnitt von " + str(tag[:]) + " auf den ersten " + str(limit) + " Punkten:" + str(np.mean(cords[: int(limit), 1])))
        if limit == 1:
            plt.scatter(cords[: int(limit), 0], cords[: int(limit), 1], label=tag)
        else:
            plt.plot(cords[: int(limit), 0], cords[: int(limit), 1], label=tag)
    plt.legend(loc=0)
    plt.ylabel("Winrate")
    plt.xlabel("Games Played")
    plt.title("Results of: " + str(title[:-2]))
    plt.grid(True)
    plt.show()

def statecount(dateiname):
    with open(dateiname, "rb") as file:
        Q = pickle.load(file)
    print(len(Q))


if __name__ == "__main__":
    main()
