import game


def main():
    game_strings = game.read_game_file("sample-input.txt")

    # Uniform Cost Search
    puzzle_count = 0
    for game_string in game_strings:
        puzzle_count += 1
        game.uniform_cost_search(game_string, puzzle_count)

    # H1: Greedy Best First Search
    puzzle_count = 0
    for game_string in game_strings:
        puzzle_count += 1
        game.greedy_best_first_search(game_string, puzzle_count, 1)

    # H2: Greedy Best First Search
    puzzle_count = 0
    for game_string in game_strings:
        puzzle_count += 1
        game.greedy_best_first_search(game_string, puzzle_count, 2)

    # H3: Greedy Best First Search
    puzzle_count = 0
    for game_string in game_strings:
        puzzle_count += 1
        game.greedy_best_first_search(game_string, puzzle_count, 3)

    # H4: Greedy Best First Search
    puzzle_count = 0
    for game_string in game_strings:
        puzzle_count += 1
        game.greedy_best_first_search(game_string, puzzle_count, 4)


if __name__ == "__main__":
    main()