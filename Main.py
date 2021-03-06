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
def getMoveQueue(map, player, group):
    map.initializeMove(player, group)

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
        elif dire == "up" or dire == "w":
            map.addToMoveQueue("up")
        elif dire == "down" or dire == "s":
            map.addToMoveQueue("down")
        elif dire == "left" or dire == "a":
            map.addToMoveQueue("left")
        elif dire == "right" or dire == "d":
            map.addToMoveQueue("right")

def displayGroups(map, currentPlayer):
    groups = map.getGroups(currentPlayer)
    print("Available groups: ")
    for x in groups:
        print(x)

    return groups

# move units on the map
def move(map, currentPlayer):
    groups = displayGroups(map, currentPlayer)

    # Choose a group outer loop
    loop = True
    while loop:
        # TODO: input validation
        choice = input("Choose a group: ")
        for x in groups:
            if choice == str(x):
                loop = getMoveQueue(map, currentPlayer, x)

# choose an attack direction for the player
def getAttackDirection(map, currentPlayer, group):
    map.initializeAttack(currentPlayer, group)

    closeDir = input("Choose a direction for your close ranged units\n"
                     "(return - go back to main menu): ")
    if closeDir == "return":
        return True

    rangeDir = input("Choose a direction for your long ranged units\n"
                     "up, up left, up right, up up, etc\n"
                     "(return - go back to main menu): ")
    if rangeDir == "return":
        return True

    map.closeAttackDirection(closeDir)
    map.rangedAttackDirection(rangeDir)

    map.attack()
    return False

# attack units on the map
def attack(map, currentPlayer):
    groups = displayGroups(map, currentPlayer)

    # Choose a group outer loop
    loop = True
    while loop:
        # TODO: input validation
        choice = input("Choose a group: ")
        for x in groups:
            if choice == str(x):
                loop = getAttackDirection(map, currentPlayer, x)

# calls the corresponding action for the player
def takeAction(choice, map, players, currentPlayer):
    if choice == "move":
        move(map, currentPlayer)
    elif choice == "attack":
        attack(map, currentPlayer)

# main driver
def main():
    player1 = Player("Player 1")
    player2 = Player("Player 2")
    players = [player1, player2] # TODO: Change when number of players changes
    numOfPlayers = len(players)
    currentPlayer = player1.id

    inf1 = Unit("infantry", 0, 5, "green", 0, 0)
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