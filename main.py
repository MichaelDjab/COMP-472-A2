from copy import deepcopy

def generateBoard(cars):
    print("generate board")
    w, h = 6, 6
    arr = [[0 for x in range(w)] for y in range(h)]  # arr is 2-darray

    x = 0
    for i in range(6):
        for j in range(6):
            arr[i][j] = '.'  # all the elemnts are going to be empty space for now
            x += 1

    for car in cars:
        size = car[0]
        x = car[1] #0
        y = car[2] #0
        ishorizontal = car[3]
        letter = car[4]
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


def goalOrNot(line):
    if line[5] == 'A':
        return True
    else:
        return False

def h1nthvehicles(line):
    indexAfterAA = line.rfind('A') + 1
    count = 0
    for x in range(indexAfterAA, 6):
        if line[x] != '.':
            count+=1
    return count

with open("sample-input.txt", "r") as f:
    temp_lines = f.readlines()

lines=[]
for x in temp_lines:
    if not (x.startswith('#') or x.startswith('\n')): #if the line starts with # or '\n' just ignore
       lines.append(x)


for line in lines:#the outermost loop
    print(line)
    print()#line break

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
    for i in range(6):
        print(arr[i])

    visited=list() #visited list, it checkes if the car is already visited

    cars = []# a car (length, row, column, is_horizontal, name, list of possible moves, fuel)


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
                    cars.append([n, i_row, i_col, True, arr[i][j], h_moves, fuel]) #car appended
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
                    cars.append([m, i_row, i_col, False, arr[i][j], v_moves, fuel])

    #print("cars is here")
    #print(cars)
    #print()#line break
    #print(arr)
    # for car in cars:
    #     if car[5]: #if car[5] - move list is not empty
    #         print(car[4])
    #         print(car[5])
    #         print(arr)
    #         for move in car[5]:
    #             temp_arr = deepcopy(arr)
    #             x = car[1]
    #             y = car[2]
    #             index = 0
    #             if(move.startswith('D')): #D1 , D2 , D3
    #                 print(move)
    #                 while car[0] > index: #it will loop size times (moving one by one)
    #                     steps = int(move[1])
    #                     temp_arr[x+steps][y] = temp_arr[x][y] #putting arr[x][y] elm to the next line
    #                     if index >= steps:
    #                         counter = 0
    #                         while counter < steps:
    #                             temp_arr[x+counter][y] = '.'  # the old place for the elm will be empty space because it moved
    #                             counter += 1
    #                     index +=1
    #                     x += 1
    #                 boards.append(temp_arr)
    #                 print(temp_arr)
    #             if (move.startswith('U')):
    #                 print(move)
    #                 while car[0] > index:  # it will loop size times
    #                     steps = int(move[1])
    #                     temp_arr[x - steps][y] = temp_arr[x][y]  # putting arr[x][y] elm to the next line
    #                     if index+1 >= steps: #steps = 2, index = 0,1
    #                         counter = 0
    #                         while counter < steps:
    #                             temp_arr[x-counter][y] = '.'  # the old place for the elm will be empty space because it moved
    #                             counter += 1
    #
    #                     index += 1
    #                     x += 1
    #                 boards.append(temp_arr)
    #                 print(temp_arr)
    # print()#line break


    boards = []

    for car in cars:
        if car[5] :
            # print("car is here")
            # print(cars)
            for move in car[5]:
                steps = int(move[1])  # ex) D2 --> 2 will be steps
                #i_car = deepcopy(car)
                if(move == 'D2'):
                    print()
                if(move.startswith('D')):
                    car[1] += steps #changing x-coordinate
                elif(move.startswith('U')):
                    car[1] -= steps
                elif(move.startswith('R')):
                    car[2] += steps
                else:
                    car[2] -= steps
                print(car[4] + move)
                print("this is car", car)
                print(generateBoard(cars))

    #print(generateBoard(cars))