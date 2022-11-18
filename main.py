
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

    print(cars)
    print()#line break
#end

