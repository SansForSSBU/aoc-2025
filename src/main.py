import sys

def my_main():
    from solutions.puzzle1.solution import main
    puzzle_num = sys.argv[1]
    with open(f"inputs/{puzzle_num}.txt", "r") as f:
        input_file = f.read()
    answers = main(input_file)
    for idx, answer in enumerate(answers):
        print(f"Part {idx+1} answer: {answer}")

if __name__ == "__main__":
    my_main()