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
intervallsize: int = 1000
namespace = "Q121231"
oldState = None
oldAction = (None, None)
oldParams = np.zeros(shape=(length, width), dtype=int)
Q = defaultdict(lambda: np.zeros(shape=(length, width), dtype=int))
wincounter: int = 0
gamecounter: int = 0
cords = []


def main():
    minesweeperheadless.main(shouldEmulateMove, onGameover, onWin, mines, length, width)


def save():
    global namespace
    global gamecounter
    with open("F:\Q/" + namespace + "_" + str(gamecounter) + ".pickle", "wb") as file:
        pickle.dump(dict(Q), file)
    with open("Q_Evo/" + str(namespace) + "_evodata" + ".pickle", "wb") as fileevo:
        pickle.dump(cords, fileevo)


def load(datei):
    global Q
    global cords
    with open(str(datei), "rb") as file:
        Q = defaultdict(lambda: np.zeros(shape=(length, width), dtype=int), pickle.load(file))
    with open("Q_Evo/" + str(namespace) + "_evodata.pickle", "rb") as file:
       cords = pickle.load(file)

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
    global oldState
    global oldAction
    global wincounter
    wincounter += 1 #testen ob es an der posotion richtig war
    evaluate()
    prevReward = Q[oldState]
    prevReward[oldAction[0]][oldAction[1]] = (1 - alpha) * prevReward[oldAction[0]][oldAction[1]] + \
                                             alpha * rewardWin
    Q[oldState] = prevReward
    oldState = None
    oldAction = (None, None)


def evaluate():
    global wincounter
    global gamecounter
    gamecounter += 1

    if gamecounter % intervallsize == 0:
        print(str(gamecounter) + ": " + str(wincounter / intervallsize))
        cords.append([gamecounter, (wincounter / intervallsize)])
        save()
        wincounter = 0


def onGameover():
    global oldState
    global oldAction

    evaluate()
    prevReward = Q[oldState]
    prevReward[oldAction[0]][oldAction[1]] = (1 - alpha) * prevReward[oldAction[0]][oldAction[1]] + \
                                             alpha * rewardKill
    oldState = None
    oldAction = (None, None)


def paramsToState(params):
    state = ""
    for j in range(0, np.array(params).shape[0]):
        for i in range(0, np.array(params).shape[1]):
            state = state + str(params[j][i]) + "_"
    state = state[:-1]
    return state


def shouldEmulateMove(params):
    global oldState
    global oldAction
    global oldParams
    state = paramsToState(params)
    estReward = Q[state]
    prevReward = Q[oldState]
    prevReward[oldAction[0]][oldAction[1]] = (1 - alpha) * np.array(prevReward[oldAction[0]][oldAction[1]]) + \
                                             alpha * (rewardAlive + gamma * estReward[pick(estReward, oldParams)[0]][
        pick(estReward, oldParams)[1]])
    Q[oldState] = prevReward
    oldState = state
    oldParams = params
    pos = pick(estReward, params)
    oldAction = pos

    return pos


if __name__ == "__main__":
    main()
