from copy import deepcopy
import sys
from random import random
from Car import Car
from Board import Board
from Uniform_cost_search import UniformCostSearch
import time


def main():

    def do_uniform_cost_search(root):

        # initialize open list, closed list and the current node
        current_node = root
        opened_list = [current_node]
        closed_list = []
        stop_loop = False

        # loop while solution is not found
        while not current_node.is_solution and not stop_loop:

            # print(" g(n): " + str(current_node.g_of_n) + ": " + current_node.board_as_string)
            # print()
            # print(current_node.moves)
            # current_node.show_board()

            # change current to the smallest node in the open list
            current_node = opened_list[0]

            # remove node if it is already in the closed list
            for node in closed_list:
                if node.board_as_string[:36] == current_node.board_as_string[:36]:

                    if len(opened_list) == 1:
                        stop_loop = True

                    if len(opened_list) > 1:
                        current_node = opened_list[1]
                        del opened_list[0]

                    continue

            # add current node's children to the open list (already sorted)
            opened_list = opened_list + current_node.get_children()

            # remove the current node from the open list and add it to the closed list
            del opened_list[0]
            closed_list.append(current_node)

            # remove duplicates of current from the open list
            to_remove = None
            for node in opened_list:
                if node.board_as_string[:36] == current_node.board_as_string[:36]:
                    opened_list.remove(node)

        if current_node.is_solution:
            print("solution:")
            print(current_node.moves)
            print(current_node.board_as_string)
        else:
            print("No solution")

    boards = [
        "BBIJ....IJCC..IAAMGDDK.MGH.KL.GHFFL.",
        "..I...BBI.K.GHAAKLGHDDKLG..JEEFF.J..",
        "JBBCCCJDD..MJAAL.MFFKL.N..KGGN.HH...",
        "BBB..MCCDD.MAAKL.MJ.KLEEJ.GG..JHHHII J0 B4",
        "IJBBCCIJDDL.IJAAL.EEK.L...KFF..GGHH. F0 G6",
        "BB.G.HE..G.HEAAG.I..FCCIDDF..I..F..."
    ]

    for b in boards:

        board = Board(b)
        print()
        print("----------------------------------")
        print(board.board_as_string)
        print()
        board.show_board()

        t0 = time.time()
        do_uniform_cost_search(board)
        t1 = time.time()

        print(str(t1-t0) + " Seconds")


main()
