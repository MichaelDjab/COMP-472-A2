class UniformCostSearch:
    def __init__(self, root):
        self.root = root

    def do_uniform_cost_search(self):

        # initialize open list, closed list and the current node
        current_node = self.root
        opened_list = [current_node]
        closed_list = []

        # loop while solution is not found
        while not current_node.board.is_solution:

            print(current_node)

            # change current to the smallest node in the open list
            current_node = opened_list[0]

            # add current node's children to the open list (already sorted)
            opened_list = opened_list + current_node.get_children()

            # remove the current node from the open list and add it to the closed list
            opened_list.remove(current_node)
            closed_list.append(current_node)

            # remove duplicates of current from the open list
            to_remove = None
            for node in opened_list:
                if node.board.board_as_string == current_node.board.board_as_string:
                    opened_list.remove(node)

        if current_node.board.is_solution:
            return current_node
        else:
            return "No solution"
