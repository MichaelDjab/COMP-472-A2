class Car:
    def __init__(self, size, row, col, is_horizontal, name, moves, fuel):
        self.size = size
        self.row = row
        self.col = col
        self.is_horizontal = is_horizontal
        self.name = name
        self.moves = moves
        self.fuel = fuel

    # show the car's info
    def show_car(self):
        print(self.name + ": size: " + str(self.size) + " row: " + str(self.row) + " column: " + str(self.col)
              + " is horizontal: " + str(self.is_horizontal) + " fuel:" + str(self.fuel))
        print("Possible moves:")
        print(self.moves)

