"""
Holds the map and the units and terrain on the map using two 2D arrays
(I guess they're lists in Python..)
"""

__author__ = 'Isaac'

class Map:
    def __init__(self, unitList, terrainList):
        self.unitList = unitList
        self.terrainList = terrainList

    # for debugging/phase 1/text version only
    def display(self):
        for i in range(0, len(self.unitList)):
            # print out rows in between units
            for j in range(0, len(self.unitList[i])):
                print("+---", end="")
            print("+")

            # print units
            for j in range(0, len(self.unitList[i])):
                if self.unitList[i][j] is None:
                    print("|   ", end="")
                else:
                    print("| " + self.unitList[i][j].char, end=" ")
            print("|")

        # print out last row
        for j in range(0, len(self.unitList[i])):
            print("+---", end="")
        print("+")