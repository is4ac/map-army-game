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

def main():
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
        choice = input("> ")

# run main
if __name__ == '__main__':
    main()