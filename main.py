from copy import deepcopy
import sys
from random import random
from Car import Car
from Board import Board


def main():
    test_board = Board("BBB..MCCDD.MAAKL.MJ.KLEEJ.GG..JHHHII J0 B4")

    test_board.show_board()
    print()

    for car in test_board.cars:
        car.show_car()

    print(test_board.is_solution)


main()
