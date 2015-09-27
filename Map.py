"""
Holds the map and the units and terrain on the map using two 2D arrays
(I guess they're lists in Python..)
"""

__author__ = 'Isaac'

class Map:
    def __init__(self, unitList, terrainList):
        self.unitList = unitList
        self.terrainList = terrainList
        self.moveQueue = []
        self.ghostList = []
        self.group = -1
        self.currentPlayer = -1

    # get all possible group options for current player
    def getGroups(self, currentPlayer):
        groups = []
        for lists in self.unitList:
            for unit in lists:
                if unit is not None:
                    if unit.owner == currentPlayer and unit.group not in groups:
                        groups.append(unit.group)

        return groups

    # Resets all units move queues
    def resetMoveQueue(self):
        self.moveQueue = []

        for lists in self.unitList:
            for unit in lists:
                unit.moveQueue = []

    # for debugging/phase 1/text version only
    def display(self):
        self.displayHelper(self.unitList)

    def displayHelper(self, unitList):
        for i in range(0, len(unitList)):
            # print out rows in between units
            for j in range(0, len(unitList[i])):
                print("+---", end="")
            print("+")

            # print units
            for j in range(0, len(unitList[i])):
                if unitList[i][j] is None:
                    print("|   ", end="")
                else:
                    print("| " + unitList[i][j].char, end=" ")
            print("|")

        # print out last row
        for j in range(0, len(unitList[i])):
            print("+---", end="")
        print("+")

    # cloning the 2D lists
    def clone(self):
        newList = []

        for i in range(0, len(self.unitList)):
            newList.append([])
            for j in range(0, len(self.unitList[i])):
                if self.unitList[i][j] is not None:
                    newList[i].append(self.unitList[i][j].clone())
                else:
                    newList[i].append(None)

        return newList

    def initializeMove(self, player, group):
        self.group = group
        self.currentPlayer = player
        self.ghostList = self.clone()

        for i in range(0, len(self.ghostList)):
            for j in range(0, len(self.ghostList[i])):
                if self.ghostList[i][j] is not None:
                    if self.ghostList[i][j].group != group and self.ghostList[i][j].owner == player:
                        self.ghostList[i][j] = None

    def addToMoveQueue(self, dire):
        # add direction to all units in the group
        for lists in self.unitList:
            for unit in lists:
                if unit is not None:
                    if unit.group == self.group:
                        unit.addMove(dire)

    # move units one step in one direction
    def move(self, units, dire):
        # use a "ghost" to track units that are on top of their own team
        # move ghost units first, then update the actual map
        if dire == "up" or "w":
            # loop through all units
            for i in range(1, len(units)):
                for j in range(0, len(units[i])):
                    if self.ghostList[i][j].group == self.group:
                        # move up if possible
                        if self.ghostList[i-1][j] is None:
                            self.ghostList[i-1][j] = self.ghostList[i][j]
                            self.ghostList[i][j] = None
        elif dire == "down" or "s":
        elif dire == "left" or "a":
        elif dire == "right" or "d":

        # update real map from ghost map


    # finalize move choices
    def submitMove(self):
        for move in self.moveQueue:
            self.move(self.unitList, move)

        self.resetMoveQueue()

    # for displaying temporary map while selecting intermediary moves
    def displayQueue(self):
        tempUnitList = self.clone()

        for move in self.moveQueue:
            self.move(tempUnitList, move)

        self.displayHelper(tempUnitList)