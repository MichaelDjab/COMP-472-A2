from math import sqrt


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


class Board:
    def __init__(self, cars, blank_spaces, size, parent, g_n):
        self.cars = cars
        self.blank_spaces = blank_spaces
        self.size = size
        self.parent = parent
        self.g_n = g_n

    def find_possible_moves(self):
        for car in self.cars:
            if car.is_horizontal:  # if the car is horizontal it can only move left to right
                possible_left_moves = []  # number of left moves assuming the car is alone on the board
                possible_right_moves = []  # number of right moves assuming the car is alone on the board
                car_fuel_left = car.fuel   # fuel available to move left
                car_fuel_right = car.fuel  # fuel available to move right

                for i in range(car.column - 1, -1, -1):
                    if car_fuel_left > 0:
                        possible_left_moves.append((car.row, i))
                        car_fuel_left -= 1

                for i in range(car.column + car.length, int(sqrt(self.size))):
                    if car_fuel_right > 0:
                        possible_right_moves.append((car.row, i))
                        car_fuel_right -= 1

                left_move_count = 0
                for left_move in possible_left_moves:
                    if left_move in self.blank_spaces:
                        left_move_count += 1
                        car.possible_moves.append("L" + str(left_move_count))
                    else:
                        break

                right_move_count = 0
                for right_move in possible_right_moves:
                    if right_move in self.blank_spaces:
                        right_move_count += 1
                        car.possible_moves.append("R" + str(right_move_count))
                    else:
                        break

            else:
                possible_up_moves = []  # number of up moves assuming the car is alone on the board
                possible_down_moves = []  # number of down moves assuming the car is alone on the board
                car_fuel_up = car.fuel  # fuel available to move up
                car_fuel_down = car.fuel  # fuel available to move down

                for i in range(car.row - 1, -1, -1):
                    if car_fuel_up > 0:
                        possible_up_moves.append((i, car.column))
                        car_fuel_up -= 1

                for i in range(car.row + car.length, int(sqrt(self.size))):
                    if car_fuel_down > 0:
                        possible_down_moves.append((i, car.column))
                        car_fuel_down -= 1

                up_move_count = 0
                for up_move in possible_up_moves:
                    if up_move in self.blank_spaces:
                        up_move_count += 1
                        car.possible_moves.append("U" + str(up_move_count))
                    else:
                        break

                down_move_count = 0
                for down_move in possible_down_moves:
                    if down_move in self.blank_spaces:
                        down_move_count += 1
                        car.possible_moves.append("D" + str(down_move_count))
                    else:
                        break


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

    game_board = Board(cars, blank_spaces, board_size, None, 0)
    game_board.find_possible_moves()
    return game_board


game_board_strings = read_game_file("sample-input.txt")

for game_board_string in game_board_strings:
    for car in initialize_game_components(game_board_string, 36).cars:
        print(car)
    print("=================================================")
