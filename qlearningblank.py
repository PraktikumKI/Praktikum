import numpy as np
from collections import defaultdict
import pickle
import minesweeperheadless

# Learning Parameters
rewardAlive = 0
rewardKill = 0
rewardWin = 0
alpha = 0
gamma = 0

# Global Parameters
mines: int = 0
length: int = 0
width: int = 0
namespace = ""
cords = []
# TODO ADD MISSING PARAMETERS

def main():
    minesweeperheadless.main(shouldEmulateMove, onGameover, onWin, mines, length, width)


def save():
    global namespace
    with open("Q_Evo/" + str(namespace) + "_evodata" + ".pickle", "wb") as fileevo:
        pickle.dump(cords, fileevo)
    # TODO FINISH THIS METHOD


def load():
    global cords
    with open("Q_Evo/" + str(namespace) + "_evodata.pickle", "rb") as file:
       cords = pickle.load(file)
    # TODO FINISH THIS METHOD


def pick(reward, params):
    # TODO IMPLEMENT THIS METHODE
    pass


def onWin():
    # TODO IMPLEMENT THIS METHODE
    pass


def evaluate():
    # TODO IMPLEMENT THIS METHODE
    pass


def onGameover():
    # TODO IMPLEMENT THIS METHODE
    pass


def paramsToState(params):
    # TODO IMPLEMENT THIS METHODE
    pass


def shouldEmulateMove(params):
    # TODO IMPLEMENT THIS METHODE
    pass


if __name__ == "__main__":
    main()
