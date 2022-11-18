
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
    if not (x.startswith('#') or x.startswith('\n')):
       lines.append(x)


for line in lines:
    print(line)
    print()#line break

    n=6

    demo = list([line[i:i+n] for i in range(0, len(line), n)])


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

    visited=list()
    # a car (length, row, column, is_horizontal, name, list of possible moves, fuel)
    cars = []

    for i in range(6):
        for j in range(6):
            if arr[i][j] not in visited and arr[i][j] != '.': #if the current elm is not visited AND is not '.'
                i_row = i
                i_col = j #initial col
                row = i_row #saving initial position
                col = i_col
                if j != 5 and arr[i][j+1] == arr[i][j]: #if arr[i][j] is horizontal   , when j ==5 then it's the last elm of the line
                    n = 1
                    r_move = 0
                    l_move = 0
                    h_moves = []
                    temp_col = j
                    if arr[i][j] in fuel_dict:
                        fuel = int(fuel_dict[arr[i][j]])
                    else:
                        fuel = 100
                    visited.append(arr[i][j])
                    while j+n != 6 and arr[i][j+n] == arr[i][j]: # while will run untill the last position of the car
                        n += 1
                    while temp_col+n != 6 and arr[i][temp_col+n] == '.': #arr[i][j+n] is the last position
                      r_move +=1
                      temp_col += 1
                      f_elm = "R" + str(r_move)
                      h_moves.append(f_elm)
                    while col-1 >= 0 and arr[i][col-1] == '.': #if the first position -1 is '.'
                      l_move +=1
                      col -= 1
                      b_elm = "L" + str(l_move)
                      h_moves.append(b_elm)
                    cars.append([n, i_row, i_col, True, arr[i][j], h_moves, fuel])
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
                        m += 1
                    while temp_row+m != 6 and arr[temp_row+m][j] == '.' : #arr[i+m][j] is the last position
                      d_move +=1
                      temp_row += 1
                      f_elm = "D" + str(d_move)
                      v_moves.append(f_elm)
                    while row-1 >= 0 and arr[row-1][j] == '.': #if the first position -1 is '.'
                      u_move +=1
                      row -= 1
                      b_elm = "U" + str(u_move)
                      v_moves.append(b_elm)
                    cars.append([m, i_row, i_col, False, arr[i][j], v_moves, fuel])

    print(cars)
    print()#line break


