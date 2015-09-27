"""
Main driver program: AKA where all the FUN TAKES PLACE
"""

__author__ = 'Isaac'

from Unit import *
from Terrain import *
from Player import *
from Map import *

# Terrains: mountain, forest, plains, river, city
mountains = Terrain("mountains", 2)
forest = Terrain("forest", 1)
plains = Terrain("plains", 0)

def initialize_map_1(unitsList, terrainList, width, height):
    for i in range(0, height):
        unitsList.append([])
        terrainList.append([])

        for j in range(0, width):
            unitsList[i].append(None)
            terrainList[i].append(plains)

def displayUnits(unitsList):
    for i in range(0, len(unitsList)):
        for j in range(0, len(unitsList[i])):
            if unitsList[i][j] is not None:
                unitsList[i][j].display()

def nextTurn(currentTurn, numOfPlayers):
    currentTurn += 1
    if currentTurn == numOfPlayers:
        currentTurn = 0

    return currentTurn

def menuDisplay(players, current):
    players[current].display()
    print("commands - move, attack, exit")

# Get input from user to enter all the movement queue from the player
# and move the units in the selected group. Returns true if successful,
# false if user undos their choice of the group and wants to return to
# the previous menu
def getMoveQueue(map, group):
    while True:
        map.displayQueue()  # display temp map
        dire = input("Choose a direction - up, left, right, down"
                    "\nreturn - return to menu\n"
                    "del - delete last move\n"
                    "(enter) - submit move: ")

        if dire == "return":  # go back to main menu
            map.resetMoveQueue()
            return True
        elif dire == "del":  # remove most recent move
            map.deleteLastMove()
        elif dire == "":
            map.submitMove()
            return False  # was successful
        elif dire == "up" or "w":
            map.addToMoveQueue("up", group)
        elif dire == "down" or "s":
            map.addToMoveQueue("down", group)
        elif dire == "left" or "a":
            map.addToMoveQueue("left", group)
        elif dire == "right" or "d":
            map.addToMoveQueue("right", group)

# move units on the map
def move(map, currentPlayer):
    groups = map.getGroups(currentPlayer)
    print("Available groups: ")
    for x in groups:
        print(x)

    # Choosing group outer loop
    loop = True
    while loop:
        # TODO: input validation
        choice = input("Choose a group: ")
        # TODO: allow people to undo their choice and choose a different group
        for x in groups:
            if choice == str(x):
                loop = getMoveQueue(map, x)



def takeAction(choice, map, players, currentPlayer):
    if choice == "move":
        move(map, currentPlayer)

def main():
    player1 = Player("Player 1")
    player2 = Player("Player 2")
    players = [player1, player2] # TODO: Change when number of players changes
    numOfPlayers = len(players)
    currentPlayer = player1.id

    inf1 = Unit("infantry", 0, 0, "green", 0, 0)
    cav1 = Unit("cavalry", 0, 1, "blue", 1, 1)

    # Test code for Map
    unitsList = []
    terrainList = []
    initialize_map_1(unitsList, terrainList, 15, 8)

    unitsList[inf1.y][inf1.x] = inf1
    unitsList[cav1.y][cav1.x] = cav1

    map = Map(unitsList, terrainList)

    # Main game loop
    choice = " "
    while choice != "exit":
        displayUnits(unitsList)
        map.display()
        menuDisplay(players, currentPlayer)
        choice = input("> ")

        # Make the appropriate action
        takeAction(choice, map, players, currentPlayer)

        # switch to next player's turn
        currentPlayer = nextTurn(currentPlayer, numOfPlayers)

# run main
if __name__ == '__main__':
    main()