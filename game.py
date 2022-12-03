from math import sqrt
from copy import deepcopy
from time import time
import pandas as pd


class Car:
    def __init__(self, name, row, column, is_horizontal, length, possible_moves, fuel):
        self.name = name
        self.row = row
        self.column = column
        self.is_horizontal = is_horizontal
        self.length = length
        self.possible_moves = possible_moves
        self.fuel = fuel

    def __repr__(self):
        return "Car " + self.name + ": row=" + str(self.row) + ", column=" + str(
            self.column) + ", is_horizontal=" + str(self.is_horizontal) + ", length=" + str(
            self.length) + ", possible_moves=" + str(self.possible_moves) + ", fuel=" + str(self.fuel)

    def __eq__(self, other):
        assert isinstance(other, Car)
        return self.name == other.name


class Board:
    def __init__(self, board_string, cars, blank_spaces, size, previous_move, parent, g_n=0, h_n=0):
        self.board_string = board_string
        self.cars = cars
        self.blank_spaces = blank_spaces
        self.size = size
        self.previous_move = previous_move
        self.parent = parent
        self.g_n = g_n
        self.h_n = h_n

    def __repr__(self):
        board_string_2d = ""
        for i in range(self.size):
            if (i + 1) % int(sqrt(self.size)) == 0:
                board_string_2d += self.board_string[i] + "\n"
            else:
                board_string_2d += self.board_string[i]

        return board_string_2d

    # two board are equal if they have the same board_string
    def __eq__(self, other):
        assert isinstance(other, Board)
        return self.board_string == other.board_string

    # generate and set the string representation of the board
    def generate_board_string(self):
        board_string = [None] * self.size  # set game_string size to be the size of the board

        for car in self.cars:  # for each car in the game board
            if car.is_horizontal:  # if the car is horizontal
                for i in range(car.length):  # number of characters to add to the board_string is equal to the length of the given car
                    board_string[car.row * int(sqrt(self.size)) + car.column + i] = car.name
            else:  # if the car is vertical
                for i in range(car.length):  # number of characters to add to the board_string is equal to the length of the given car
                    board_string[(car.row * int(sqrt(self.size))) + car.column + (i * int(sqrt(self.size)))] = car.name

        for blank_space in self.blank_spaces:  # for each blank space in the board's blank_spaces list add the "." to the corresponding index
            board_string[blank_space[0] * int(sqrt(self.size)) + blank_space[1]] = "."

        self.board_string = ''.join(board_string)  # set board_string to the string representation of the created list

    # given a board, find and set all possible moves of each car
    def find_possible_moves(self):
        for car in self.cars:
            if car.is_horizontal:  # if the car is horizontal it can only move left and right
                all_possible_left_moves = []  # number of left moves assuming the car is alone on the board
                all_possible_right_moves = []  # number of right moves assuming the car is alone on the board
                car_fuel_left = car.fuel   # fuel available to move left
                car_fuel_right = car.fuel  # fuel available to move right

                # given a car's position, calculate all possible left moves (assuming the car is alone on the board)
                for i in range(car.column - 1, -1, -1):
                    if car_fuel_left > 0:
                        all_possible_left_moves.append((car.row, i))
                        car_fuel_left -= 1

                # given a car's position, calculate all possible right moves (assuming the car is alone on the board)
                for i in range(car.column + car.length, int(sqrt(self.size))):
                    if car_fuel_right > 0:
                        all_possible_right_moves.append((car.row, i))
                        car_fuel_right -= 1

                # for each possible left move, check if the coordinate is in the board's blank spaces list
                left_move_count = 0
                for left_move in all_possible_left_moves:
                    if left_move in self.blank_spaces:
                        left_move_count += 1
                        car.possible_moves.append("L" + str(left_move_count))
                    else:  # once a non-blank space is reached, the car can no longer move in that direction
                        break

                # for each possible right move, check if the coordinate is in the board's blank spaces list
                right_move_count = 0
                for right_move in all_possible_right_moves:
                    if right_move in self.blank_spaces:
                        right_move_count += 1
                        car.possible_moves.append("R" + str(right_move_count))
                    else:  # once a non-blank space is reached, the car can no longer move in that direction
                        break

            else:  # if the car is vertical it can only move up and down
                all_possible_up_moves = []  # number of up moves assuming the car is alone on the board
                all_possible_down_moves = []  # number of down moves assuming the car is alone on the board
                car_fuel_up = car.fuel  # fuel available to move up
                car_fuel_down = car.fuel  # fuel available to move down

                # given a car's position, calculate all possible up moves (assuming the car is alone on the board)
                for i in range(car.row - 1, -1, -1):
                    if car_fuel_up > 0:
                        all_possible_up_moves.append((i, car.column))
                        car_fuel_up -= 1

                # given a car's position, calculate all possible down moves (assuming the car is alone on the board)
                for i in range(car.row + car.length, int(sqrt(self.size))):
                    if car_fuel_down > 0:
                        all_possible_down_moves.append((i, car.column))
                        car_fuel_down -= 1

                # for each possible up move, check if the coordinate is in the board's blank spaces list
                up_move_count = 0
                for up_move in all_possible_up_moves:
                    if up_move in self.blank_spaces:
                        up_move_count += 1
                        car.possible_moves.append("U" + str(up_move_count))
                    else:  # once a non-blank space is reached, the car can no longer move in that direction
                        break

                # for each possible down move, check if the coordinate is in the board's blank spaces list
                down_move_count = 0
                for down_move in all_possible_down_moves:
                    if down_move in self.blank_spaces:
                        down_move_count += 1
                        car.possible_moves.append("D" + str(down_move_count))
                    else:  # once a non-blank space is reached, the car can no longer move in that direction
                        break

    # return the list of children for a given board
    def get_children(self):
        children = []
        for car in self.cars:
            for move in car.possible_moves:
                children.append(self.new_board_after_move(car, move))

        return children

    # return true if board is a goal state
    def is_goal_state(self):
        goal_state = False
        for car in self.cars:
            if car.name == "A" and car.row == 2 and car.column == 1 + 5 - car.length:  # if the ambulance's last column index is at the exit
                goal_state = True
        return goal_state

    # helper function for get_children() - given a board, car and move, return the new board
    def new_board_after_move(self, move_car, move):
        # initialize child board member variables
        parent = self
        previous_move = previous_move = move_car.name + ": " + move
        size = self.size
        cars = deepcopy(self.cars)
        blank_spaces = deepcopy(self.blank_spaces)

        car_exited = False  # if the current move causes the car to exit the board

        old_car_pos = []  # car's current position
        new_car_pos = []  # car's position after it moves
        if move_car.is_horizontal:  # if car is horizontal it can move left or right
            for i in range(move_car.length):
                old_car_pos.append((move_car.row, move_car.column + i))  # get the current position of each car component

            if move[0] == "L":  # car moving left
                for i in range(move_car.length):
                    new_car_pos.append((old_car_pos[i][0], old_car_pos[i][1] - int(move[1])))  # get the position of each car component after it moves
            else:  # car moving right
                for i in range(move_car.length):
                    new_car_pos.append((old_car_pos[i][0], old_car_pos[i][1] + int(move[1])))  # get the position of each car component after it moves

                # if the column for the car's most right index = (3,5) and the car is not the ambulance, it exits the board (only possible for horizontal cars moving right)
                if new_car_pos[move_car.length - 1][0] == 2 and new_car_pos[move_car.length - 1][1] == int(sqrt(self.size)) - 1 and move_car.name != "A":
                    car_exited = True
        else:  # if car is vertical it can move up or down
            for i in range(move_car.length):
                old_car_pos.append((move_car.row + i, move_car.column))  # get the current position of each car component

            if move[0] == "U":  # car moving up
                for i in range(move_car.length):
                    new_car_pos.append((old_car_pos[i][0] - int(move[1]), old_car_pos[i][1]))  # get the position of each car component after it moves
            else:  # car moving down
                for i in range(move_car.length):
                    new_car_pos.append((old_car_pos[i][0] + int(move[1]), old_car_pos[i][1]))  # get the position of each car component after it moves

        if car_exited:  # if after the car moves it has reached the exit
            for position in old_car_pos:
                blank_spaces.append(position)  # all the car's previously occupied spaces turn empty
        else:  # if the car is still on the board after it moves
            for new_pos in new_car_pos:
                if new_pos not in old_car_pos:  # if the new position is not in the old positions list
                    blank_spaces.remove(new_pos)  # the new position is no longer a blanks space
            for old_pos in old_car_pos:
                if old_pos not in new_car_pos:  # if the old position is not in the new positions list
                    blank_spaces.append(old_pos)  # the old position is now a blanks space

        # for each car in the new cars list (copied)
        for car in cars:
            car.possible_moves.clear()  # clear each car's possible moves
            if car_exited:  # if the car exited the board and car is not the ambulance, remove the car from the game
                if car.name == move_car.name:
                    cars.remove(car)
            else:  # if the car is still on the board
                if car.name == move_car.name:
                    car.fuel = car.fuel - int(move[1])  # update the car's fuel
                    car.row = new_car_pos[0][0]  # update the car's row position
                    car.column = new_car_pos[0][1]  # update the car's column position

        child_board = Board(None, cars, blank_spaces, size, previous_move, parent)  # initialize the new child game board
        child_board.generate_board_string()  # generate and initialize the child's board string
        child_board.find_possible_moves()  # update each car's possible move list with a new set of moves
        return child_board

    # returns the number of blocking positions
    def num_of_blocking_positions(self):
        a_car = None
        for car in self.cars:  # find the A car
            if car.name == "A":
                a_car = car
                break
        characters_after_a = self.board_string[12 + a_car.column + a_car.length:18]  # slice the remaining characters after car A in its row

        num_of_blocked_pos_between_a_and_exit = 0
        for char in characters_after_a:  # for each  character after the A car, if the character is not "." it is a new blocking position
            if char != ".":
                num_of_blocked_pos_between_a_and_exit += 1

        return num_of_blocked_pos_between_a_and_exit

    # returns the number of blocking cars given a game board
    def num_of_blocking_cars(self):
        a_car = None
        for car in self.cars:  # find the A car
            if car.name == "A":
                a_car = car
                break
        characters_after_a = self.board_string[12 + a_car.column + a_car.length:18]  # slice the remaining characters after car A in its row
        unique_characters_after_a = set(characters_after_a)  # find unique characters

        blocking_cars_count = 0
        for char in unique_characters_after_a:  # for each unique character, if the character is not "." it is a new blocking car
            if char != ".":
                blocking_cars_count += 1
        return blocking_cars_count

    # sets board's h_n = number of blocking cars
    def heuristic_1(self):
        self.h_n = self.num_of_blocking_cars()

    # sets board's h_n = number of blocking positions
    def heuristic_2(self):
        self.h_n = self.num_of_blocking_positions()

    # sets board's h_n = 5 * the number of blocking cars
    def heuristic_3(self):
        self.h_n = 5 * self.num_of_blocking_cars()

    # sets board's h_n = 0
    def heuristic_4(self):
        self.h_n = 0


# read a game file and return a list of game strings
def read_game_file(file_name):
    with open(file_name) as file:
        lines = file.read().splitlines()

    game_strings = []

    for line in lines:
        if '#' not in line and line:  # if line does not start with # and is not blank append it to the game_strings list
            game_strings.append(line.strip())

    return game_strings


# given a game string and board size, returns the corresponding fully initialized board with its initialized cars
def initialize_game_components(game_string, board_size=36):
    cars = []  # list of car objects
    blank_spaces = []  # list of tuple coordinates to blank spaces
    fuel_list = game_string[board_size: len(game_string)].split()  # list of fuel info (all chars after the board len)
    index = 0  # current index in the game_string
    while index < board_size:
        row_index = int(index / 6)  # convert 1d index to 2d row index
        column_index = index % 6  # convert 1d index to 2d column index

        if game_string[index] == '.':  # if the char = '.' append its coordinates to the blank spaces list
            blank_spaces.append((row_index, column_index))  # append the indices of the blank space
            index += 1  # increment the current index to the next character

        elif game_string[index] in [car.name for car in cars]:  # skip over car characters already in the cars list
            index += 1  # increment the current index to the next character

        else:
            is_horizontal = True
            if game_string[index] != game_string[index + 1]:  # if the next index is the same as the current, car is horizontal
                is_horizontal = False

            length = 1  # car's length
            temp_index = index

            if is_horizontal:  # if the car is horizontal
                while temp_index + 1 < len(game_string) and game_string[temp_index] == game_string[temp_index + 1]:  # check if the next character is the same as the current
                    temp_index += 1
                    length += 1  # increment the car's length
                temp_index = index  # reset the temp index
                index += length  # increment the current index by the horizontal car length (skip these indices on the next iteration)
            else:  # if the car is vertical
                while temp_index + int(sqrt(board_size)) < board_size and game_string[temp_index] == game_string[temp_index + int(sqrt(board_size))]:  # check if the character in the next row is the as the current
                    temp_index += int(sqrt(board_size))  # increment index to the next row in the same column
                    length += 1  # increment the car's length
                temp_index = index  # reset the temp index
                index += 1  # increment the current index to the next character

            cars.append(Car(game_string[temp_index], row_index, column_index, is_horizontal, length, [],100))  # append new car to the cars list

    # if fuel information is present in the game string, assign it to the corresponding car
    for car_fuel in fuel_list:
        for car in cars:
            if car.name == car_fuel[0]:
                car.fuel = int(car_fuel[1])
                break

    game_board = Board(game_string[0: board_size], cars, blank_spaces, board_size, None, None, 0)  # initialize game board
    game_board.find_possible_moves()  # initialize the possible_moves list of each car
    return game_board


# performs uniform cost search on the give game_board_string and returns a dictionary of search data
def uniform_cost_search(game_board_string, puzzle_number):
    initial_board = initialize_game_components(game_board_string)

    open_list = []
    closed_list = []
    goal_state_found = False

    open_list.append(initial_board)  # append the initial board to the open list
    start = time()  # start algorithm time
    while not goal_state_found and len(open_list) != 0:  # continue to search children if the goal state is not found and the open list is not 0
        open_list.sort(key=lambda x: x.g_n, reverse=False)  # sort the open list by g(n) ascending
        if open_list[0].is_goal_state():  # if the lowest cost node is the goal state
            goal_state_found = True
        else:  # if the lowest cost node is not the goal state
            children = open_list[0].get_children()  # create the node's children
            for child in children:
                if child not in closed_list:  # if the child is not already in the closed list (not visited)
                    child.g_n = child.parent.g_n + 1
                    board_in_open_list = False
                    for board in open_list:  # check if child is already in the open list
                        if board.board_string == child.board_string and child.g_n >= board.g_n:  # if the child is in the open list with a greater cost, do not add it to the open list
                            board_in_open_list = True
                            break
                        elif board.board_string == child.board_string and child.g_n < board.g_n:  # if the child is in the open list with a lower cost, replace the old node with the child
                            board_in_open_list = True
                            open_list.remove(board)
                            open_list.append(child)
                            break
                    if not board_in_open_list:  # if the child is not in the open list, append it to the open list
                        open_list.append(child)

        closed_list.append(open_list.pop(0))  # pop the visited node and add it to the closed list

    end = time()  # when out of the search, stop the end time

    runtime = round(end - start, 2)  # calculate the runtime
    solution_path = []

    if goal_state_found:  # if the goal state was found, calculate the solution path
        goal_state = closed_list[-1]  # the goal state is the last node in the closed list
        solution_path.append(goal_state)

        next_parent = goal_state.parent
        while next_parent.parent is not None:  # append each parent from the goal_state to the solution path list
            solution_path.insert(0, next_parent)
            next_parent = next_parent.parent

    return {"puzzle_number": puzzle_number,
            "algorithm_name": "ucs",
            "heuristic_number": None,
            "solution_path": solution_path,
            "search_path": closed_list,
            "runtime": runtime,
            "game_board_string": game_board_string,
            "initial_board": initial_board,
            "goal_state_found": goal_state_found}


# performs greedy best first search on the give game_board_string and returns a dictionary of search data
def greedy_best_first_search(game_board_string, puzzle_number, heuristic_number):
    initial_board = initialize_game_components(game_board_string)
    heuristic = None

    # set heuristic function based on passed heuristic_num
    match heuristic_number:
        case 1:
            heuristic = Board.heuristic_1
        case 2:
            heuristic = Board.heuristic_2
        case 3:
            heuristic = Board.heuristic_3
        case 4:
            heuristic = Board.heuristic_4

    heuristic(initial_board)  # set heuristic using passed heuristic function

    open_list = []
    closed_list = []
    goal_state_found = False

    open_list.append(initial_board)  # append the initial board to the open list
    start = time()  # start algorithm time
    while not goal_state_found and len(open_list) != 0:  # continue to search children if the goal state is not found and the open list is not 0
        open_list.sort(key=lambda x: x.h_n, reverse=False)  # sort the open list by h(n) ascending
        if open_list[0].is_goal_state():  # if the lowest heuristic node is the goal state
            goal_state_found = True
        else:  # if the lowest heuristic node is not the goal state
            children = open_list[0].get_children()  # create the node's children
            for child in children:
                if child not in open_list and child not in closed_list:  # if the child is not already in the closed list (not visited)
                    heuristic(child)  # apply the heuristic on the child before appending to the open list
                    open_list.append(child)

        closed_list.append(open_list.pop(0))  # pop the visited node and add it to the closed list

    end = time()  # when out of the search, stop the end time
    runtime = round(end - start, 2)  # calculate the runtime
    solution_path = []

    if goal_state_found:  # if the goal state was found, calculate the solution path
        solution_path = []
        goal_state = closed_list[-1]  # the goal state is the last node in the closed list
        solution_path.append(goal_state)

        next_parent = goal_state.parent
        while next_parent.parent is not None:  # append each parent from the goal_state to the solution path list
            solution_path.insert(0, next_parent)
            next_parent = next_parent.parent

    return {"puzzle_number": puzzle_number,
            "algorithm_name": "gbfs",
            "heuristic_number": heuristic_number,
            "solution_path": solution_path,
            "search_path": closed_list,
            "runtime": runtime,
            "game_board_string": game_board_string,
            "initial_board": initial_board,
            "goal_state_found": goal_state_found}


# performs algorithm A on the give game_board_string and returns a dictionary of search data
def algorithm_a(game_board_string, puzzle_number, heuristic_number):
    initial_board = initialize_game_components(game_board_string)
    heuristic = None

    # set heuristic function based on passed heuristic_num
    match heuristic_number:
        case 1:
            heuristic = Board.heuristic_1
        case 2:
            heuristic = Board.heuristic_2
        case 3:
            heuristic = Board.heuristic_3
        case 4:
            heuristic = Board.heuristic_4

    heuristic(initial_board)  # set heuristic using passed heuristic function

    open_list = []
    closed_list = []
    goal_state_found = False

    open_list.append(initial_board)  # append the initial board to the open list
    start = time()  # start algorithm time
    while not goal_state_found and len(open_list) != 0:  # continue to search children if the goal state is not found and the open list is not 0
        open_list.sort(key=lambda x: x.g_n + x.h_n, reverse=False)  # sort the open list by f(n) ascending
        if open_list[0].is_goal_state():  # if the lowest f(n) node is the goal state
            goal_state_found = True
        else:  # if the lowest f(n) node is not the goal state
            children = open_list[0].get_children()  # create the node's children
            for child in children:
                if child not in closed_list:  # if the child is not already in the closed list (not visited)
                    child.g_n = child.parent.g_n + 1
                    board_in_open_list = False
                    for board in open_list:  # check if child is already in the open list
                        if board.board_string == child.board_string and child.g_n >= board.g_n:  # if the child is in the open list with a greater cost, do not add it to the open list
                            board_in_open_list = True
                            break
                        elif board.board_string == child.board_string and child.g_n < board.g_n:  # if the child is in the open list with a lower cost, replace the old node with the child
                            board_in_open_list = True
                            open_list.remove(board)
                            heuristic(child)  # apply the heuristic on the child before appending to the open list
                            open_list.append(child)
                            break
                    if not board_in_open_list:  # if the child is not in the open list, append it to the open list
                        heuristic(child)  # apply the heuristic on the child before appending to the open list
                        open_list.append(child)

        closed_list.append(open_list.pop(0))  # pop the visited node and add it to the closed list

    end = time()  # when out of the search, stop the end time
    runtime = round(end - start, 2)  # calculate the runtime
    solution_path = []

    if goal_state_found:  # if the goal state was found, calculate the solution path
        solution_path = []
        goal_state = closed_list[-1]  # the goal state is the last node in the closed list
        solution_path.append(goal_state)

        next_parent = goal_state.parent
        while next_parent.parent is not None:  # append each parent from the goal_state to the solution path list
            solution_path.insert(0, next_parent)
            next_parent = next_parent.parent

    return {"puzzle_number": puzzle_number,
            "algorithm_name": "a",
            "heuristic_number": heuristic_number,
            "solution_path": solution_path,
            "search_path": closed_list,
            "runtime": runtime,
            "game_board_string": game_board_string,
            "initial_board": initial_board,
            "goal_state_found": goal_state_found}


# creates and writes to a solution file
def create_solution_file(algorithm_name, puzzle_number, initial_board, game_board_string, runtime, found_goal_state, heuristic_number=None, search_path=None, solution_path=None):
    file_name = f"{algorithm_name}-sol-{puzzle_number}"
    if heuristic_number:
        file_name = f"{algorithm_name}-h{heuristic_number}-sol-{puzzle_number}"
    with open(file_name, "w") as file:
        file.write(f"Initial board configuration: {game_board_string}\n")
        file.write(f"\n{str(initial_board)}\n")
        file.write("Car fuel available: ")
        file.write(', '.join([car.name + ":" + str(car.fuel) for car in initial_board.cars]) + "\n\n")

        if found_goal_state:
            file.write(f"Runtime: {runtime} seconds\n")
            file.write(f"Search path length: {len(search_path)} states\n")
            file.write(f"Solution path length: {len(solution_path)} moves\n")
            file.write(f"Solution path: {'; '.join([node.previous_move for node in solution_path if node.previous_move])}\n\n")
            for node in solution_path:
                file.write(f"{node.previous_move}\t{[car.fuel for car in node.cars if car.name == node.previous_move[0]][0]} {node.board_string}\n")
            file.write(f"\n{solution_path[-1]}")
        else:
            file.write("Sorry, could not solve the puzzle as specified.\n")
            file.write("Error: no solution found\n")
            file.write(f"Runtime: {runtime} seconds")


# creates and writes to a search file
def create_search_file(algorithm_name, puzzle_number, search_path, heuristic_number=None):
    file_name = f"{algorithm_name}-search-{puzzle_number}"
    if heuristic_number:
        file_name = f"{algorithm_name}-h{heuristic_number}-search-{puzzle_number}"
    with open(file_name, "w") as file:
        for node in search_path:
            file.write(f"{node.g_n + node.h_n} {node.g_n} {node.h_n} {node.board_string}\n")


# solves the puzzles in the given game file using the requested algorithms, producing the requested output files
def solve_puzzles(game_file, with_ucs=False, with_gbfs=False, with_algo_a=False, create_output_files=False, create_excel_file=False):
    game_strings = read_game_file(game_file)  # all game string puzzles in the input file
    data = []  # list that contains data for excel file output
    puzzle_number = 0  # number of puzzles counter
    for game_string in game_strings:
        puzzle_number += 1

        # if with_ucs=True, ucs is performed on each puzzle in the game_file
        if with_ucs:
            game_info = uniform_cost_search(game_string, puzzle_number)  # save search data dictionary

            # if create_output_files=True, pass required search data
            if create_output_files:
                create_solution_file(game_info["algorithm_name"],
                                     game_info["puzzle_number"],
                                     game_info["initial_board"],
                                     game_info["game_board_string"],
                                     game_info["runtime"],
                                     game_info["goal_state_found"],
                                     game_info["heuristic_number"],
                                     game_info["search_path"],
                                     game_info["solution_path"])

                create_search_file(game_info["algorithm_name"],
                                   game_info["puzzle_number"],
                                   game_info["search_path"],
                                   game_info["heuristic_number"])

            # if create_excel_file=True, pass required search data
            if create_excel_file:
                data.append([puzzle_number,
                             game_info["algorithm_name"],
                             "NA",
                             len(game_info["solution_path"]),
                             len(game_info["search_path"]),
                             game_info["runtime"]])

        # if with_gbfs=True, gbfs is performed on each puzzle in the game_file with all 4 heuristics
        if with_gbfs:

            for i in range(1, 5):  # for each heuristic
                game_info = greedy_best_first_search(game_string, puzzle_number, heuristic_number=i)  # save search data dictionary

                # if create_output_files=True, pass required search data
                if create_output_files:
                    create_solution_file(game_info["algorithm_name"],
                                         game_info["puzzle_number"],
                                         game_info["initial_board"],
                                         game_info["game_board_string"],
                                         game_info["runtime"],
                                         game_info["goal_state_found"],
                                         game_info["heuristic_number"],
                                         game_info["search_path"],
                                         game_info["solution_path"])

                    create_search_file(game_info["algorithm_name"],
                                       game_info["puzzle_number"],
                                       game_info["search_path"],
                                       game_info["heuristic_number"])

                # if create_excel_file=True, pass required search data
                if create_excel_file:
                    data.append([puzzle_number,
                                 game_info["algorithm_name"],
                                 "h" + str(i),
                                 len(game_info["solution_path"]),
                                 len(game_info["search_path"]),
                                 game_info["runtime"]])

        # if with_algo_a=True, algorithm A is performed on each puzzle in the game_file with all 4 heuristics
        if with_algo_a:
            for i in range(1, 5):  # for each heuristic
                game_info = algorithm_a(game_string, puzzle_number, heuristic_number=i)  # save search data dictionary

                # if create_output_files=True, pass required search data
                if create_output_files:
                    create_solution_file(game_info["algorithm_name"],
                                         game_info["puzzle_number"],
                                         game_info["initial_board"],
                                         game_info["game_board_string"],
                                         game_info["runtime"],
                                         game_info["goal_state_found"],
                                         game_info["heuristic_number"],
                                         game_info["search_path"],
                                         game_info["solution_path"])

                    create_search_file(game_info["algorithm_name"],
                                       game_info["puzzle_number"],
                                       game_info["search_path"],
                                       game_info["heuristic_number"])

                # if create_excel_file=True, pass required search data
                if create_excel_file:
                    data.append([puzzle_number,
                                 game_info["algorithm_name"],
                                 "h" + str(i),
                                 len(game_info["solution_path"]),
                                 len(game_info["search_path"]),
                                 game_info["runtime"]])

    # if create_excel_file=True, create data frame with each algorithms search data and output to an excel file
    if create_excel_file:
        df = pd.DataFrame(data, columns=["Puzzle Number", "Algorithm", "Heuristic", "Length of the Solution", "Length of the Search Path", "Execution Time (in seconds)"])
        with pd.ExcelWriter("rush_hour_analysis.xlsx") as writer:
            df.to_excel(writer)
