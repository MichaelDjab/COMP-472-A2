import game


def main():
    game_strings = game.read_game_file("sample-input.txt")

    puzzle_count = 0
    for game_string in game_strings:
        puzzle_count += 1
        game.uniform_cost_search(game_string, puzzle_count)


if __name__ == "__main__":
    main()