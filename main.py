from copy import deepcopy
import sys
from random import random
from Car import Car
from Board import Board
from Node import Node
from Uniform_cost_search import UniformCostSearch


def main():
    # to create a board simply pass the string
    test_board = Board("....F...B.F.AABCF....C.....C....EE..")

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
    # next_test_board = test_board.get_board_given_move('U2', test_l_car)

    # print(next_test_board.show_board())
    # print(next_test_board.board_as_string)

    node = Node(test_board, None)

    # next_node = Node(next_test_board, node)

    ucs = UniformCostSearch(node).do_uniform_cost_search()

    if ucs is str:
        print(ucs)
    else:
        ucs.board.show_board()






    # ignore this for now....

    # def do_uniform_cost_search(root_board):
    #
    #     # initialize open list, closed list and the current node
    #     current_board = root_board
    #     opened_list = [current_board]
    #     closed_list = []
    #
    #     # loop while solution is not found
    #     while not is_solution(current_board):
    #
    #         print(current_board)
    #
    #         # change current to the smallest node in the open list
    #         current_board = opened_list[0]
    #
    #         # add current node's children to the open list (already sorted)
    #         opened_list = opened_list + get_children(current_board)
    #
    #         # remove the current node from the open list and add it to the closed list
    #         opened_list.remove(current_board)
    #         closed_list.append(current_board)
    #
    #         # remove duplicates of current from the open list
    #         to_remove = None
    #         for node in opened_list:
    #             if node.board.board_as_string == current_board.board.board_as_string:
    #                 opened_list.remove(node)
    #
    #     if current_board.board.is_solution:
    #         return current_board
    #     else:
    #         return "No solution"
    #
    # # returns true  if board is solution
    # def is_solution(board):
    #     return board[17] == 'A'
    #
    # # return children boards of given board
    # def get_children(board):
    #
    #     children = []
    #
    #     moves = get_moves(board)
    #
    #     for car in self.board.cars:
    #         for move in car.moves:
    #             child_board = self.board.get_board_given_move(move, car)
    #             child = Node(child_board, self) if child_board is not None else None
    #             if child is not None:
    #                 children.append(child)
    #
    #     for child in children:
    #         if child is None:
    #             children.remove(child)
    #
    #     children = sorted(children, key=lambda node: int('inf') if node is None else node.g_of_n)  # sort by cost
    #
    #     return children
    #
    # def get_moves(board):
    #
    #     board_as_array = get_board_array(board)
    #
    #     # list of visited character cells in the board
    #     visited = list()
    #
    #     # will be a list of cars on the board
    #     cars = []
    #
    #     fuel_dictionary = extract_fuel(board)
    #
    #     # iterage through the board array and extract the cars
    #     for i in range(6):
    #         for j in range(6):
    #             # Not visited and is not '.'
    #             if board_as_array[i][j] not in visited and board_as_array[i][j] != '.':
    #                 i_row = i  # initial row
    #                 i_col = j  # initial col
    #
    #                 # if arr[i][j] is horizontal, when j == 5 then it's the last elm of the line
    #                 if j != 5 and board_as_array[i][j + 1] == board_as_array[i][j]:
    #                     n = 1  # n is size
    #                     r_move = 0  # right move
    #                     l_move = 0  # left move
    #                     h_moves = []
    #                     temp_col = j
    #
    #                     # Fuel amount is specified
    #                     if board_as_array[i][j] in fuel_dictionary:
    #                         fuel = int(fuel_dictionary[board_as_array[i][j]])
    #                     else:  # otherwise fuel is 100
    #                         fuel = 100
    #
    #                     # Add currently visited cell
    #                     visited.append(board_as_array[i][j])
    #
    #                     # while loop will run until it reaches the last position of the car
    #                     while j + n != 6 and board_as_array[i][j + n] == board_as_array[i][j]:
    #                         n += 1  # n is size
    #
    #                     # temp_col is just 'j' which is the initial col number + n (car size) so arr[i][temp_col+n] is
    #                     # the next elm of the last position of car (in other words, it's checking if there is an
    #                     # empty space on the right side
    #                     while temp_col + n != 6 and board_as_array[i][temp_col + n] == '.':
    #                         r_move += 1
    #                         temp_col += 1
    #                         f_elm = "R" + str(r_move)
    #                         h_moves.append(f_elm)
    #
    #                     # temp_col is back to initial col
    #                     temp_col = i_col
    #
    #                     # Back to the first position of the car to check if there is an empty space on the left side
    #                     while temp_col - 1 >= 0 and board_as_array[i][temp_col - 1] == '.':
    #                         l_move += 1
    #                         temp_col -= 1
    #                         b_elm = "L" + str(l_move)
    #                         h_moves.append(b_elm)
    #
    #                     # create a car according to the following convention:
    #                     # Car(size, row, column, is horizontal, letter of car, possible moves, fuel)
    #                     car = Car(n, i_row, i_col, True, board_as_array[i][j], h_moves, fuel)
    #
    #                     # creating a car object and putting it into cars[]
    #                     cars.append(car)
    #
    #                 # if arr[i][j] is vertical
    #                 elif i != 5:
    #                     m = 1
    #                     u_move = 0
    #                     d_move = 0
    #                     v_moves = []
    #                     temp_row = i
    #
    #                     # fuel is specified
    #                     if board_as_array[i][j] in fuel_dictionary:
    #                         fuel = int(fuel_dictionary[board_as_array[i][j]])
    #                     else:
    #                         fuel = 100
    #
    #                     # append currently visited cell
    #                     visited.append(board_as_array[i][j])
    #
    #                     while i + m != 6 and self.board_as_array[i + m][j] == self.board_as_array[i][j]:
    #                         m += 1  # m is size
    #                     while temp_row + m != 6 and self.board_as_array[temp_row + m][j] == '.':
    #                         d_move += 1
    #                         temp_row += 1
    #                         f_elm = "D" + str(d_move)
    #                         v_moves.append(f_elm)
    #
    #                     temp_row = i_row  # temp_row is back to initial row
    #
    #                     # If the first position -1 is '.'
    #                     while temp_row - 1 >= 0 and self.board_as_array[temp_row - 1][j] == '.':
    #                         u_move += 1
    #                         temp_row -= 1
    #                         b_elm = "U" + str(u_move)
    #                         v_moves.append(b_elm)
    #                     car = Car(m, i_row, i_col, False, self.board_as_array[i][j], v_moves, fuel)
    #                     cars.append(car)  # creating a car object and putting it into cars[]
    #     return cars
    #
    # # show board
    # def show_board(board):
    #     board_as_array = get_board_array(board)
    #     for i in range(6):
    #         print(board_as_array[i])
    #
    # # gets the board as an array
    # def get_board_array(board):
    #     board_array = [[0 for x in range(6)] for y in range(6)]
    #
    #     x = 0
    #     for i in range(6):
    #         for j in range(6):
    #             board_array[i][j] = board[x]
    #             x += 1
    #     return board_array
    #
    # # extract fuel
    # def extract_fuel(board):
    #     letters = []
    #     fuel = []
    #     for index, character in enumerate(board):
    #         if index > 36:
    #             if character.isnumeric():
    #                 fuel.append(character)
    #             elif character != ' ' and character != '\n':
    #                 letters.append(character)
    #
    #     fuel_dict = {}  # dictionary
    #     for i, character in enumerate(letters):
    #         fuel_dict[character] = fuel[i]
    #
    #     return fuel_dict

main()
