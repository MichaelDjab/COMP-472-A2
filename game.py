from math import sqrt
from copy import deepcopy
from time import time


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
    def __init__(self, board_string, cars, blank_spaces, size, previous_move, parent, g_n):
        self.board_string = board_string
        self.cars = cars
        self.blank_spaces = blank_spaces
        self.size = size
        self.previous_move = previous_move
        self.parent = parent
        self.g_n = g_n

    def __repr__(self):
        board_string_2d = ""
        for i in range(self.size):
            if (i + 1) % int(sqrt(self.size)) == 0:
                board_string_2d += self.board_string[i] + "\n"
            else:
                board_string_2d += self.board_string[i]

        return board_string_2d

    def __eq__(self, other):
        assert isinstance(other, Board)
        return self.board_string == other.board_string

    def generate_board_string(self):
        game_string = [None] * self.size

        for car in self.cars:
            if car.is_horizontal:
                for i in range(car.length):
                    game_string[car.row * int(sqrt(self.size)) + car.column + i] = car.name
            else:
                for i in range(car.length):
                    game_string[(car.row * int(sqrt(self.size))) + car.column + (i * int(sqrt(self.size)))] = car.name

        for blank_space in self.blank_spaces:
            game_string[blank_space[0] * int(sqrt(self.size)) + blank_space[1]] = "."

        self.board_string = ''.join(game_string)

    # given a board, find all possible moves of each car
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

    def get_children(self):
        children = []
        for car in self.cars:
            for move in car.possible_moves:
                children.append(self.new_board_after_move(car, move))

        return children

    def is_goal_state(self):
        goal_state = False
        for car in self.cars:
            if car.name == "A" and car.row == 2 and car.column == 1 + 5 - car.length:
                goal_state = True
        return goal_state

    def new_board_after_move(self, move_car, move):
        # initialize child board member variables
        parent = self
        g_n = self.g_n + 1
        previous_move = move_car.name + ": " + move
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

        child_board = Board(None, cars, blank_spaces, size, previous_move, parent, g_n)  # initialize the new child game board
        child_board.generate_board_string()  # generate and initialize the child's board string
        child_board.find_possible_moves()  # update each car's possible move list with a new set of moves
        return child_board


def read_game_file(file_name):
    with open(file_name) as file:
        lines = file.read().splitlines()

    game_strings = []

    for line in lines:
        if '#' not in line and line:
            game_strings.append(line.strip())

    return game_strings


# given a game string and board size, returns the corresponding fully initialized board
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
                while game_string[temp_index] == game_string[temp_index + 1]:  # check if the next character is the same as the current
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

    game_board = Board(game_string[0: board_size], cars, blank_spaces, board_size, None, None, 0)
    game_board.find_possible_moves()
    return game_board


def uniform_cost_search(file_name):
    initial_game_board_strings = read_game_file(file_name)

    for game_board_string in initial_game_board_strings:
        initial_board = initialize_game_components(game_board_string)
        print(initial_board.board_string)
        open_list = []
        closed_list = []
        goal_state_found = False

        open_list.append(initial_board)
        start = time()
        while not goal_state_found and len(open_list) != 0:
            open_list.sort(key=lambda x: x.g_n, reverse=False)  # check if sort works
            if open_list[0].is_goal_state():
                goal_state_found = True
            else:
                children = open_list[0].get_children()
                for child in children:
                    if child not in closed_list:
                        board_in_open_list = False
                        for board in open_list:
                            if board.board_string == child.board_string and child.g_n >= board.g_n:
                                board_in_open_list = True
                                break
                            elif board.board_string == child.board_string and child.g_n < board.g_n:
                                board_in_open_list = True
                                open_list.remove(board)
                                open_list.append(child)
                                break
                        if not board_in_open_list:
                            open_list.append(child)

            closed_list.append(open_list.pop(0))
        end = time()
        if goal_state_found:
            solution_path = []
            goal_state = closed_list[-1]
            solution_path.append(goal_state)

            next_parent = goal_state.parent
            while next_parent is not None:
                solution_path.insert(0, next_parent)
                next_parent = next_parent.parent

            solution_path_string = ""
            for node in solution_path:
                solution_path_string += (str(node.previous_move) + " ")
            print("Runtime: ", end - start, " seconds")
            print("Search path length: ", len(closed_list), " states")
            print("Solution path length: ", len(solution_path) - 1, " moves")
            print("Solution path: ", solution_path_string)
        else:
            print("Sorry, could not solve the puzzle as specified.")
            print("Error: no solution found")
            print("Runtime: ", end - start, " seconds")

uniform_cost_search("sample-input.txt")