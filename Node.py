class Node:
    def __init__(self, board, parent):

        if board is None:
            self = None
        else:
            self.board = board
            self.parent = parent
            self.g_of_n = self.get_g_of_n()

    def __str__(self):
        details = ''
        details += f'Board  : {self.board.board_as_string}\n'
        if self.parent is not None:
            details += f'Parent : {self.parent.board.board_as_string}\n'
        else:
            details += f'Parent : {None}\n'
        details += f'G(n)   : {self.g_of_n}\n'
        return details

    # show the node
    def show_node(self):
        print("Node board:")
        print(self.board.show_board())

        print("Parent board:")

        if self.parent is None:
            print("No parent")
        else:
            print(self.parent.board.show_board())

        print("Total cost from root node: " + str(self.g_of_n))

    # returns all the child nodes of a given node with the smallest g(n) first
    def get_children(self):

        children = []
        for car in self.board.cars:
            for move in car.moves:
                child_board = self.board.get_board_given_move(move, car)
                child = Node(child_board, self) if child_board is not None else None
                if child is not None:
                    children.append(child)

        for child in children:
            if child is None:
                children.remove(child)

        children = sorted(children, key=lambda node: int('inf') if node is None else node.g_of_n)  # sort by cost

        return children

    # returns cost
    def get_g_of_n(self):

        # start with cost 0
        cost = 0
        found_root = self.parent is None
        current = self

        while not found_root:
            parent = current.parent
            current = parent
            if parent is None:
                found_root = True
            else:
                cost = cost + 1

        return cost
