import numpy as np
import matplotlib.pyplot as plt
import pickle
import sys

allcords =[]


# Die Main-Methode dient der Steuerung des Analyse Tools. Sie dient zur Steuerung der
# einzelnen Analysefunktionen. Dazu nimmt sie Anweisungen durch die Konsole entgegen.
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



# Die Load-Methode lädt die verschiedenen Evo-daten, welche von dem Q-Learning Durchläufen
# gespeichert worden und fügt sie in einem Array zusammen. Sie ist in der Lage, mehrere
# Evodateien nacheinander einzulesen.
def load( *x):
    allcords.clear()
    for number in x:
        with open(str("Q_Evo/" + "Q" + str(number) + "_e"
                                                     "vodata" + ".pickle"), "rb") as file:
            cords = pickle.load(file)
            allcords.append(["Q" + str(number), cords])





# Die Analyse-Methode nutzt das Pyplot Package, um die vorher in den verschiedenen Evo-daten
# gespeicherten Ergebnisse in Graphenform visuell darzustellen. Dazu werden die Daten
# in ein Numpyarray konvertiert und mittels Listslicing der Pyplot Funktion übergeben.
# Diese öffnet ein Fenster, in welchem die jeweiligen Graphen der verschiedenen Tests
# zu sehen sind.  Zusätzlich zu dem Graphen wird auf der Konsole der Durchschnitt und
# das Maximum der einzelnen Tests, welche mittels Listsliceing errechnet wird, ausgegeben.
def analyse(limit =-1):
    title = ""
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



#Die Statecount-Methode gibt die Anzahl der erkundeten Zustände in einem Speicherstand an. Dazu wird einfach
# der len() befehl auf dem Dictionery ausgeführt.
def statecount(dateiname):
    with open(dateiname, "rb") as file:
        Q = pickle.load(file)
    print(len(Q))


if __name__ == "__main__":
    main()
