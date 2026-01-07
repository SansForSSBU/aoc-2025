import sys

def my_main():
    from solutions.puzzle1.solution import main
    puzzle_num = sys.argv[1]
    with open(f"inputs/{puzzle_num}.txt", "r") as f:
        input_file = f.read()
    print(main(input_file))

if __name__ == "__main__":
    my_main()