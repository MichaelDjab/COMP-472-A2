from Car import Car


# board class represents the rush hour 6 x 6 board
class Board:

    # initializes the board with a string
    def __init__(self, board_as_string):
        self.board_as_string = board_as_string
        self.valet_service()
        self.board_as_array = self.get_board_array()
        self.fuel_dictionary = self.extract_fuel()
        self.cars = self.extract_cars()
        self.next_moves = 0
        self.is_solution = self.is_solution()

    # shows the board
    def show_board(self):
        for i in range(6):
            print(self.board_as_array[i])

    # gets the board as an array
    def get_board_array(self):
        board_array = [[0 for x in range(6)] for y in range(6)]

        x = 0
        for i in range(6):
            for j in range(6):
                board_array[i][j] = self.board_as_string[x]
                x += 1
        return board_array

    # extracts the fuel
    def extract_fuel(self):
        letters = []
        fuel = []
        for index, character in enumerate(self.board_as_string):
            if index > 36:
                if character.isnumeric():
                    fuel.append(character)
                elif character != ' ' and character != '\n':
                    letters.append(character)

        fuel_dict = {}  # dictionary
        for i, character in enumerate(letters):
            fuel_dict[character] = fuel[i]

        return fuel_dict

    # extracts a list of cars from the board
    def extract_cars(self):

        # list of visited character cells in the board
        visited = list()

        # will be a list of cars on the board
        cars = []

        # iterage through the board array and extract the cars
        for i in range(6):
            for j in range(6):
                # Not visited and is not '.'
                if self.board_as_array[i][j] not in visited and self.board_as_array[i][j] != '.':
                    i_row = i  # initial row
                    i_col = j  # initial col

                    # if arr[i][j] is horizontal, when j == 5 then it's the last elm of the line
                    if j != 5 and self.board_as_array[i][j + 1] == self.board_as_array[i][j]:
                        n = 1  # n is size
                        r_move = 0  # right move
                        l_move = 0  # left move
                        h_moves = []
                        temp_col = j

                        # Fuel amount is specified
                        if self.board_as_array[i][j] in self.fuel_dictionary:
                            fuel = int(self.fuel_dictionary[self.board_as_array[i][j]])
                        else:  # otherwise fuel is 100
                            fuel = 100

                        # Add currently visited cell
                        visited.append(self.board_as_array[i][j])

                        # while loop will run until it reaches the last position of the car
                        while j + n != 6 and self.board_as_array[i][j + n] == self.board_as_array[i][j]:
                            n += 1  # n is size

                        # temp_col is just 'j' which is the initial col number + n (car size) so arr[i][temp_col+n] is
                        # the next elm of the last position of car (in other words, it's checking if there is an
                        # empty space on the right side
                        while temp_col + n != 6 and self.board_as_array[i][temp_col + n] == '.':
                            r_move += 1
                            temp_col += 1
                            f_elm = "R" + str(r_move)
                            h_moves.append(f_elm)

                        # temp_col is back to initial col
                        temp_col = i_col

                        # Back to the first position of the car to check if there is an empty space on the left side
                        while temp_col - 1 >= 0 and self.board_as_array[i][temp_col - 1] == '.':
                            l_move += 1
                            temp_col -= 1
                            b_elm = "L" + str(l_move)
                            h_moves.append(b_elm)

                        # create a car according to the following convention:
                        # Car(size, row, column, is horizontal, letter of car, possible moves, fuel)
                        car = Car(n, i_row, i_col, True, self.board_as_array[i][j], h_moves, fuel)

                        # creating a car object and putting it into cars[]
                        cars.append(car)

                    # if arr[i][j] is vertical
                    elif i != 5:
                        m = 1
                        u_move = 0
                        d_move = 0
                        v_moves = []
                        temp_row = i

                        # fuel is specified
                        if self.board_as_array[i][j] in self.fuel_dictionary:
                            fuel = int(self.fuel_dictionary[self.board_as_array[i][j]])
                        else:
                            fuel = 100

                        # append currently visited cell
                        visited.append(self.board_as_array[i][j])

                        while i + m != 6 and self.board_as_array[i + m][j] == self.board_as_array[i][j]:
                            m += 1  # m is size
                        while temp_row + m != 6 and self.board_as_array[temp_row + m][j] == '.':
                            d_move += 1
                            temp_row += 1
                            f_elm = "D" + str(d_move)
                            v_moves.append(f_elm)

                        temp_row = i_row  # temp_row is back to initial row

                        # If the first position -1 is '.'
                        while temp_row - 1 >= 0 and self.board_as_array[temp_row - 1][j] == '.':
                            u_move += 1
                            temp_row -= 1
                            b_elm = "U" + str(u_move)
                            v_moves.append(b_elm)
                        car = Car(m, i_row, i_col, False, self.board_as_array[i][j], v_moves, fuel)
                        cars.append(car)  # creating a car object and putting it into cars[]
        return cars

    def get_board_given_move(self, move, cr):

        car = Car(cr.size, cr.row, cr.col, cr.is_horizontal, cr.name, cr.moves, cr.fuel)

        # check for available fuel
        if car.fuel is 0:
            return None

        # copy the current board string
        new_board_str = self.board_as_string

        # get number of moves
        num_moves = int(move[1])

        if move.startswith('U'):

            while not num_moves == 0:
                # get the positions
                u_pos_minus_1 = car.row * 6 + car.col - 6
                d_pos = car.row * 6 + car.col + car.size*6 - 6

                num_moves = num_moves - 1

                # moving up means we replace the car character with '.' on the bottom...
                new_board_str = new_board_str[:d_pos] + '.' + new_board_str[d_pos + 1:]

                # and replace '.' with the car character on the top
                new_board_str = new_board_str[:u_pos_minus_1] + car.name + new_board_str[u_pos_minus_1 + 1:]

                car.row = car.row - 1
        if move.startswith('R'):

            while not num_moves == 0:

                # get the positions
                l_pos = car.row * 6 + car.col
                r_pos_plus_1 = car.row * 6 + car.col + car.size

                num_moves = num_moves - 1

                # moving to the right means we replace the car character with '.' on the left...
                new_board_str = new_board_str[:l_pos] + '.' + new_board_str[l_pos + 1:]

                # and replace '.' with the car character on the right
                new_board_str = new_board_str[:r_pos_plus_1] + car.name + new_board_str[r_pos_plus_1 + 1:]

                car.col = car.col + 1

        if move.startswith('D'):

            while not num_moves == 0:
                # get the positions
                u_pos = car.row * 6 + car.col
                d_pos_plus_1 = car.row * 6 + car.col + car.size*6

                num_moves = num_moves - 1

                # moving down means we replace the car character with '.' on the top...
                new_board_str = new_board_str[:u_pos] + '.' + new_board_str[u_pos + 1:]

                # and replace '.' with the car character under
                new_board_str = new_board_str[:d_pos_plus_1] + car.name + new_board_str[d_pos_plus_1 + 1:]

                car.row = car.row + 1

        if move.startswith('L'):

            while not num_moves == 0:
                # get the positions
                l_pos_minus_1 = car.row * 6 + car.col - 1
                r_pos = car.row * 6 + car.col + car.size - 1

                num_moves = num_moves - 1

                # moving to the left means we replace the car character with '.' on the right...
                new_board_str = new_board_str[:r_pos] + '.' + new_board_str[r_pos + 1:]

                # and replace '.' with the car character on the left
                new_board_str = new_board_str[:l_pos_minus_1] + car.name + new_board_str[l_pos_minus_1 + 1:]

                car.col = car.col - 1

        # reduce fuel by 1
        car.fuel = car.fuel - 1

        # adjust the fuel consumption
        fuel_string = new_board_str[37:]

        # if the fuel string already has the car and its fuel amount, adjust it
        if car.name in fuel_string:
            for i, char in enumerate(fuel_string):
                if char == car.name:
                    new_board_str = new_board_str[:38 + i] + str(car.fuel) + new_board_str[39 + i:]
        # otherwise concatenate it at the end
        else:
            new_board_str = new_board_str + " " + car.name + str(car.fuel)

        return Board(new_board_str)

    # returns true if the ambulance is at the exit
    def is_solution(self):
        return self.board_as_string[17] == 'A'

    # removes cars at position f3 free of charge
    def valet_service(self):
        car_name = self.board_as_string[17]
        if car_name is not '.' and car_name is not 'A':
            self.board_as_string = self.board_as_string.replace(car_name, '.')
            print("removed car " + car_name + " --> " + self.board_as_string)

