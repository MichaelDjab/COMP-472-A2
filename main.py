import game


def main():

    game.solve_puzzles("sample-input.txt", with_ucs=True, with_algo_a=True, with_gbfs=True, create_output_files=False, create_excel_file=True)


if __name__ == "__main__":
    main()