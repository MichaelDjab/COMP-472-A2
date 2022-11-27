from copy import deepcopy
import sys
from random import random


class Car:
    def __init__(self, size, row, col, is_horizontal, name, moves, fuel):
        self.size = size
        self.row = row
        self.col = col
        self.is_horizontal = is_horizontal
        self.name = name
        self.moves = moves
        self.fuel = fuel

class Board:
    def __init__(self, arr, cars, parent, parent_car_move):
        self.arr = arr #2-d array
        self.cars = cars #cars is list , that have car objects      cars=[]   cars.append(Car(2, 0, 0, True, 'A', ['R1', 'R2'], 100))
        self.parent_board = parent
        count = 0
        temp_parent_board = self.parent_board
        while(temp_parent_board != None):
            temp_parent_board = temp_parent_board.parent_board
            count += 1
        self.cost = count
        self.parent_car_move = parent_car_move
def regenerateCarsMovelist(cars): #update car move lists
    arr = generateBoard(cars)
    fuel_list=[]
    for car in cars:
        fuel_list.append(car.name + str(car.fuel))
    #print("fuel list", fuel_list)
    fuel_dict = generateFuel_dict(fuel_list)
    cars.clear()#empty cars list because we already have arr(2-d array board) and fuel_dict
    visited=list()
    for i in range(6): #6x6
        for j in range(6):
            if arr[i][j] not in visited and arr[i][j] != '.': #if the current elm is not visited AND is not '.'
                i_row = i #initial row
                i_col = j #initial col
                if j != 5 and arr[i][j+1] == arr[i][j]: #if arr[i][j] is horizontal   , when j ==5 then it's the last elm of the line
                    n = 1 # n is size
                    r_move = 0 #right move
                    l_move = 0 #left move
                    h_moves = []
                    temp_col = j
                    if arr[i][j] in fuel_dict: #if fuel is specified
                        fuel = int(fuel_dict[arr[i][j]])
                    else: #otherwise fule is 100
                        fuel = 100
                    visited.append(arr[i][j]) #arr[i][j] which is the current elm is visited now
                    while j+n != 6 and arr[i][j+n] == arr[i][j]: # while loop will run untill the last position of the car
                        n += 1 #n is size
                    while temp_col+n != 6 and arr[i][temp_col+n] == '.': #temp_col is just 'j' which is initial col number + n (car size) so arr[i][temp_col+n] is the next elm of the last position of car (in other words, it's checking if there is an empty space on the right side
                      r_move +=1
                      temp_col += 1
                      f_elm = "R" + str(r_move)
                      h_moves.append(f_elm)
                    temp_col = i_col #temp_col is back to initial col
                    while temp_col-1 >= 0 and arr[i][temp_col-1] == '.': #Back to the first position of the car to check if there is an empty space on the left side
                      l_move +=1
                      temp_col -= 1
                      b_elm = "L" + str(l_move)
                      h_moves.append(b_elm)
                    cars.append(Car(n, i_row, i_col, True, arr[i][j], h_moves, fuel)) #creating a car object and putting it into cars[]
                elif i != 5: #if arr[i][j] is vertical
                    m = 1
                    u_move = 0
                    d_move = 0
                    v_moves = []
                    temp_row = i
                    if arr[i][j] in fuel_dict:
                        fuel = int(fuel_dict[arr[i][j]])
                    else:
                        fuel = 100
                    visited.append(arr[i][j])
                    while i+m != 6 and arr[i+m][j] == arr[i][j]:
                        m += 1 # m is size
                    while temp_row+m != 6 and arr[temp_row+m][j] == '.' :
                      d_move +=1
                      temp_row += 1
                      f_elm = "D" + str(d_move)
                      v_moves.append(f_elm)
                    temp_row = i_row #temp_row is back to initial row
                    while temp_row-1 >= 0 and arr[temp_row-1][j] == '.': #if the first position -1 is '.'
                      u_move +=1
                      temp_row -= 1
                      b_elm = "U" + str(u_move)
                      v_moves.append(b_elm)
                    cars.append(Car(m, i_row, i_col, False, arr[i][j], v_moves, fuel)) #creating a car object and putting it into cars[]
    return cars





def extractCars(arr, fuel_dict, boards): #extractCars returns cars[]
    visited=list()
    cars = []
    for i in range(6): #6x6
        for j in range(6):
            if arr[i][j] not in visited and arr[i][j] != '.': #if the current elm is not visited AND is not '.'
                i_row = i #initial row
                i_col = j #initial col
                if j != 5 and arr[i][j+1] == arr[i][j]: #if arr[i][j] is horizontal   , when j ==5 then it's the last elm of the line
                    n = 1 # n is size
                    r_move = 0 #right move
                    l_move = 0 #left move
                    h_moves = []
                    temp_col = j
                    if arr[i][j] in fuel_dict: #if fuel is specified
                        fuel = int(fuel_dict[arr[i][j]])
                    else: #otherwise fule is 100
                        fuel = 10000
                    visited.append(arr[i][j]) #arr[i][j] which is the current elm is visited now
                    while j+n != 6 and arr[i][j+n] == arr[i][j]: # while loop will run untill the last position of the car
                        n += 1 #n is size
                    while temp_col+n != 6 and arr[i][temp_col+n] == '.': #temp_col is just 'j' which is initial col number + n (car size) so arr[i][temp_col+n] is the next elm of the last position of car (in other words, it's checking if there is an empty space on the right side
                      r_move +=1
                      temp_col += 1
                      f_elm = "R" + str(r_move)
                      h_moves.append(f_elm)
                    temp_col = i_col #temp_col is back to initial col
                    while temp_col-1 >= 0 and arr[i][temp_col-1] == '.': #Back to the first position of the car to check if there is an empty space on the left side
                      l_move +=1
                      temp_col -= 1
                      b_elm = "L" + str(l_move)
                      h_moves.append(b_elm)
                    cars.append(Car(n, i_row, i_col, True, arr[i][j], h_moves, fuel)) #creating a car object and putting it into cars[]
                elif i != 5: #if arr[i][j] is vertical
                    m = 1
                    u_move = 0
                    d_move = 0
                    v_moves = []
                    temp_row = i
                    if arr[i][j] in fuel_dict:
                        fuel = int(fuel_dict[arr[i][j]])
                    else:
                        fuel = 10000
                    visited.append(arr[i][j])
                    while i+m != 6 and arr[i+m][j] == arr[i][j]:
                        m += 1 # m is size
                    while temp_row+m != 6 and arr[temp_row+m][j] == '.' :
                      d_move +=1
                      temp_row += 1
                      f_elm = "D" + str(d_move)
                      v_moves.append(f_elm)
                    temp_row = i_row #temp_row is back to initial row
                    while temp_row-1 >= 0 and arr[temp_row-1][j] == '.': #if the first position -1 is '.'
                      u_move +=1
                      temp_row -= 1
                      b_elm = "U" + str(u_move)
                      v_moves.append(b_elm)
                    cars.append(Car(m, i_row, i_col, False, arr[i][j], v_moves, fuel)) #creating a car object and putting it into cars[]

    boards.append(Board(arr, cars, None, None))#creation of board object and put it into boards[]
    return cars
#endof extractCars function

   # self.size = size
   #      self.row = row
   #      self.col = col
   #      self.is_horizontal = is_horizontal
   #      self.name = name
   #      self.moves = moves
   #      self.fuel = fuel
def generatePossibleBoards(board): #boad is an object that has many cars
    cars = board.cars
    boards = []
    cars = regenerateCarsMovelist(cars)#updating car moves list
    parent_board = board
    for car in cars:
        if car.moves:
            #print(car.moves)
            for move in car.moves:
                temp_cars = deepcopy(cars)
                temp_car = deepcopy(car)
                steps = int(move[1])  # ex) D2 --> 2 will be steps
                fuel = temp_car.fuel #remaining fuel
                #getting indexofCar
                for x in temp_cars:
                    if(x.name == temp_car.name):
                        indexofCar = temp_cars.index(x)
                if (fuel >= steps):  # only when you have enough fuel for steps
                    if (move.startswith('D')):
                        temp_car.row += steps  # changing x-coordinate
                    elif (move.startswith('U')):
                        temp_car.row -= steps
                    elif (move.startswith('R')):
                        temp_car.col += steps
                    else:  # move.startswith('L')
                        temp_car.col -= steps
                    fuel -= steps  # fuel is going to be reduced by how many steps it went
                    temp_car.fuel = fuel
                    for y in temp_cars:
                        if(y.name == temp_car.name):
                            temp_cars[indexofCar] = temp_car
                    #print("move", temp_car.name+move)
                    arr = generateBoard(temp_cars)
                    # for i in range(6):
                    #     print(arr[i])
                    boards.append(Board(arr, temp_cars, parent_board, temp_car.name+" "+move))
                    parent_bord = boards[-1] #parent board that was just put into boards[] is the last elm of boards[]
    return boards

def generateBoard(cars): #it generates 2-d array board
    w, h = 6, 6
    arr = [[0 for x in range(w)] for y in range(h)]  # arr is 2-darray

    x = 0
    for i in range(6):
        for j in range(6):
            arr[i][j] = '.'  # all the elemnts are going to be empty space for now
            x += 1

    for car in cars:
        size = car.size
        x = car.row #0
        y = car.col #0
        ishorizontal = car.is_horizontal
        letter = car.name
        counter = 0
        while counter < size:
            if ishorizontal: #if car is horizontal
                arr[x][y] = letter
                y += 1
            else: #if car is vertical
                arr[x][y] = letter
                x += 1
            counter+=1

    return arr


def generateFuel_dict(fuel_list):
    letters = []
    fuel = []
    for elm in fuel_list:
        letters.append(elm[0])
        fuel.append(elm[1:])

    fuel_dict = {}  # dictionary
    for i, x in enumerate(letters):
        fuel_dict[x] = fuel[i]

    return fuel_dict


def goalOrNot(arr): #arr is 2-d array
    if arr[2][5] == 'A':
        return True
    else:
        return False

def h1nthvehicles(arr):
    indexAfterAA = arr[2].rfind('A') + 1
    count = 0
    for x in range(indexAfterAA, 6):
        if line[x] != '.':
            count+=1
    return count




def UniformCostSearch(boards):
    opened_list = []
    closed_list = []
    count = 1
    for board in boards:
        opened_list.append(board) #putting into jobs_list
    for node in opened_list:
        #print the size of jobs_list
        #print("jobs_list size: ", len(jobs_list))
        if goalOrNot(node.arr):
            print("goal")
            print("cost ",node.cost)
            for i in range(6):
                print(node.arr[i])
            print()
            while(node.parent_board != None):
                if(node.parent_board.parent_board == None):
                    print("initial board")
                else:
                    print("parent ", count)
                    count+=1
                print(node.parent_car_move)
                for i in range(6):
                    print(node.parent_board.arr[i])
                print()
                node = node.parent_board
            break
        else:
            if node.arr not in closed_list:
                closed_list.append(node.arr)#node is already visited
            else:
                 #remove node from jobs_list
                 opened_list.remove(node)
            children_nodes = generatePossibleBoards(node)
            for child in children_nodes:
                if child.arr not in closed_list:
                    opened_list.append(child)




#Beginning of main
with open("sample-input.txt", "r") as f:
    temp_lines = f.readlines()

lines=[]
for x in temp_lines:
    if not (x.startswith('#') or x.startswith('\n')): #if the line starts with # or '\n' just ignore
       lines.append(x)
boards= [];
game_count =1
for line in lines:#the outermost loop
    boards.clear()
    print("Game " + str(game_count))
    print("Game " + str(game_count) +" "+ "string is : " + line)
    game_count +=1
    print()#line break
    if(game_count == 4):
        print()
    w, h = 6, 6
    arr = [[0 for x in range(w)] for y in range(h)]
    #putting into 2-d array
    x=0
    for i in range(6):
        for j in range(6):
            arr[i][j] = line[x]
            x+=1
    #fuel
    letters=[];
    fuel=[];
    for idx, x in enumerate(line):
        if idx > 36:
            if x.isnumeric():
                fuel.append(x)
            elif x != ' ' and x != '\n':
                letters.append(x)


    fuel_dict={} #dictionary
    for i, x in enumerate(letters):
        fuel_dict[x] = fuel[i]
    #printing arr
    print("Printing the line in 6x6")
    for i in range(6):
        print(arr[i])

    cars = []# a car (length, row, column, is_horizontal, name, list of possible moves, fuel)
    cars = extractCars(arr, fuel_dict, boards)
    print()



    #boards
    boards = generatePossibleBoards(boards[0]) #getting initial board

    UniformCostSearch(boards)







