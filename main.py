from copy import deepcopy
import sys
from random import random
from Car import Car
from Board import Board


def main():
    # to create a board simply pass the string
    test_board = Board("BBB..MCC...MAAKL.MJ.KLEEJ.GG..JHHHII J0 B4")

    # to show the board use the method show_board()
    test_board.show_board()
    print()

    # to show the car use show_car()
    for car in test_board.cars:
        car.show_car()

    # use some test cards just to show how the get_board_given_move() works
    for car in test_board.cars:
        if car.name == 'B':
            test_b_car = car
        if car.name == 'G':
            test_g_car = car
        if car.name == 'M':
            test_m_car = car
        if car.name == 'L':
            test_l_car = car

    # get_board_given_move as the name suggests outputs a new board given a move and a car, it is a board method
    # which means that any board can call this method for all its moves
    next_test_board = test_board.get_board_given_move('U1', test_l_car)

    print(next_test_board.show_board())


main()
