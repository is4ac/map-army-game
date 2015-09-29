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
        self.tempUnitList = []
        self.group = -1
        self.currentPlayer = -1
        self.closeDir = ""
        self.rangeDir = ""

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
                if unit is not None:
                    unit.resetMoveQueue()

    # for debugging/phase 1/text version only
    def display(self):
        self.displayHelper(self.unitList)

    # helps display the unit map
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

    # cloning the 2D unit list
    def clone(self):
        newList = []

        for i in range(0, len(self.unitList)):
            newList.append([])
            for j in range(0, len(self.unitList[i])):
                if self.unitList[i][j] is not None:
                    newList[i].append(self.unitList[i][j])
                else:
                    newList[i].append(None)

        return newList

    # removes the last move in the move queue
    def deleteLastMove(self):
        self.moveQueue = self.moveQueue[:-1]

        for lists in self.tempUnitList:
            for unit in lists:
                if unit is not None:
                    unit.deleteLastMove()

    # initializes which group of units are gonna be moved
    def initializeMove(self, player, group):
        self.group = group
        self.currentPlayer = player
        self.ghostList = self.clone()
        self.tempUnitList = self.clone()

        for i in range(0, len(self.ghostList)):
            for j in range(0, len(self.ghostList[i])):
                if self.ghostList[i][j] is not None:
                    if self.ghostList[i][j].group != group and self.ghostList[i][j].owner == player:
                        self.ghostList[i][j] = None

    # adds the direction to the move queue
    def addToMoveQueue(self, dire):
        self.moveQueue.append(dire)

        # add direction to all units in the group
        for lists in self.ghostList:
            for unit in lists:
                if unit is not None:
                    if unit.group == self.group:
                        unit.addMove(dire)

    # remove the given unit id from the map
    def remove(self, units, id):
        for i in range(0, len(units)):
            for j in range(0, len(units[i])):
                if units[i][j] is not None:
                    if units[i][j].id == id:
                        units[i][j] = None

    # remove all dead units from the map
    def removeDeadUnits(self):
        for i in range(0, len(self.unitList)):
            for j in range(0, len(self.unitList[i])):
                if self.unitList[i][j] is not None and self.unitList[i][j].hp <= 0:
                    self.unitList[i][j] = None

    # move units one step in one direction
    def move(self, units, dire, num):
        print(dire)
        # use a "ghost" to track units that are on top of their own team
        # move ghost units first, then update the actual map
        if dire == "up" or dire == "w":
            # loop through all units
            for i in range(1, len(units)):
                for j in range(0, len(units[i])):
                    if self.ghostList[i][j] is not None:
                        if (self.ghostList[i][j].group == self.group and
                                self.ghostList[i][j].moveQueue[num] is not None):
                            # move up if possible
                            if self.ghostList[i-1][j] is None:
                                self.ghostList[i-1][j] = self.ghostList[i][j]
                                self.ghostList[i][j] = None
        elif dire == "down" or dire == "s":
            # loop through all units
            for i in range(len(units)-2, -1, -1):
                for j in range(0, len(units[i])):
                    if self.ghostList[i][j] is not None:
                        if (self.ghostList[i][j].group == self.group and
                                self.ghostList[i][j].moveQueue[num] is not None):
                            # move down if possible
                            if self.ghostList[i+1][j] is None:
                                self.ghostList[i+1][j] = self.ghostList[i][j]
                                self.ghostList[i][j] = None
        elif dire == "left" or dire == "a":
            # loop through all units
            for j in range(1, len(units[0])):
                for i in range(0, len(units)):
                    if self.ghostList[i][j] is not None:
                        if (self.ghostList[i][j].group == self.group and
                                self.ghostList[i][j].moveQueue[num] is not None):
                            # move left if possible
                            if self.ghostList[i][j-1] is None:
                                self.ghostList[i][j-1] = self.ghostList[i][j]
                                self.ghostList[i][j] = None
        elif dire == "right" or dire == "d":
            # loop through all units
            for j in range(len(units[0])-2, -1, -1):
                for i in range(0, len(units)):
                    if self.ghostList[i][j] is not None:
                        if (self.ghostList[i][j].group == self.group and
                                self.ghostList[i][j].moveQueue[num] is not None):
                            # move right if possible
                            if self.ghostList[i][j+1] is None:
                                self.ghostList[i][j+1] = self.ghostList[i][j]
                                self.ghostList[i][j] = None

        # update real map from ghost map
        for i in range(0, len(units)):
            for j in range(0, len(units[i])):
                if self.ghostList[i][j] is not None:
                    if self.ghostList[i][j].group == self.group:
                        if units[i][j] is None:
                            # remove original from map
                            self.remove(units, self.ghostList[i][j].id)
                            units[i][j] = self.ghostList[i][j]

    # finalize move choices
    def submitMove(self):
        self.unitList = self.tempUnitList
        self.resetMoveQueue()

    # for displaying temporary map while selecting intermediary moves
    def displayQueue(self):
        self.tempUnitList = self.clone()
        self.ghostList = self.clone()

        for x in range(0, len(self.moveQueue)):
            self.move(self.tempUnitList, self.moveQueue[x], x)

        print(self.moveQueue)
        self.displayHelper(self.tempUnitList)

    # initializes the attack phase
    def initializeAttack(self, currentPlayer, group):
        self.currentPlayer = currentPlayer
        self.group = group

    # sets close ranged units attack direction
    def closeAttackDirection(self, closeDir):
        self.closeDir = closeDir

    # sets ranged units attack direction
    def rangedAttackDirection(self, rangeDir):
        self.rangeDir = rangeDir

    # conducts the attack
    def attack(self):
        # attempt to battle all units for short range units
        for i in range(0, len(self.unitList)):
            for j in range(0, len(self.unitList[i])):
                if self.unitList[i][j] is not None:
                    if self.closeDir == "up":
                        if i-1 < 0:
                            continue
                        else:
                            if self.unitList[i-1][j] is not None:
                                self.unitList[i][j].battle(self.unitList[i-1][j],
                                                           self.terrainList[i][j],
                                                           self.terrainList[i-1][j])

                    elif self.closeDir == "down":
                        if i+1 >= len(self.unitList):
                            continue
                        else:
                            if self.unitList[i+1][j] is not None:
                                self.unitList[i][j].battle(self.unitList[i+1][j],
                                                           self.terrainList[i][j],
                                                           self.terrainList[i+1][j])

                    elif self.closeDir == "left":
                        if j-1 < 0:
                            continue
                        else:
                            if self.unitList[i][j-1] is not None:
                                self.unitList[i][j].battle(self.unitList[i][j-1],
                                                           self.terrainList[i][j],
                                                           self.terrainList[i][j-1])

                    elif self.closeDir == "right":
                        if j+1 >= len(self.unitList[i]):
                            continue
                        else:
                            if self.unitList[i][j+1] is not None:
                                self.unitList[i][j].battle(self.unitList[i][j+1],
                                                           self.terrainList[i][j],
                                                           self.terrainList[i][j+1])

        # TODO: ranged units attacking
        # Preference is given for the specific location given for ranged units,
        # but if there is another unit in range in that general direction,
        # then that unit gets attacked.
        for i in range(0, len(self.unitList)):
            for j in range(0, len(self.unitList[i])):
                if self.unitList[i][j] is not None:
                    if self.rangeDir == "up up":


        self.removeDeadUnits()