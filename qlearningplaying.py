import numpy as np
from collections import defaultdict
import pickle
import minesweeperQ

# Learning Parameters
mines: int = 3
length: int = 5
width: int = 5
pfad ="Q\Q0_100000000.pickle"
# Global Parameters
intervallsize: int = 100
Q = defaultdict(lambda: np.zeros(shape=(length, width), dtype=int))
wincounter: int = 0
gamecounter: int = 0


def main():
    load(pfad)
    minesweeperQ.main(shouldEmulateMove, onGameover, onWin, mines, length, width)

def load(datei):
    global Q
    with open(str(datei), "rb") as file:
        Q = defaultdict(lambda: np.zeros(shape=(length, width), dtype=int), pickle.load(file))

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

def onWin():
    global wincounter
    wincounter += 1
    evaluate()


def onGameover():
    evaluate()


def evaluate():
    global wincounter
    global gamecounter
    gamecounter += 1
    if gamecounter % intervallsize == 0:
        print(str(gamecounter) + ": " + str(wincounter / intervallsize))
        wincounter = 0


def paramsToState(params):
    state = ""
    for j in range(0, np.array(params).shape[0]):
        for i in range(0, np.array(params).shape[1]):
            state = state + str(params[j][i]) + "_"
    state = state[:-1]
    return state

def shouldEmulateMove(params):
    pos = pick(Q[paramsToState(params)], params)
    return pos

if __name__ == "__main__":
    main()
