with open("inputs/1.txt", "r") as f:
    lines = f.read()

moves = lines.split("\n")
moves = [(move[0], int(move[1:])) for move in moves if len(move) > 0]
pass

dial=50
pt1_ans = 0
pt2_ans = 0

def move_dial(move):
    global dial
    global pt1_ans
    global pt2_ans
    n_moves = move[1]
    for _ in range(n_moves):
        if move[0] == "L":
            dial -= 1
        elif move[0] == "R":
            dial += 1
        dial = dial % 100
        if dial == 0:
            pt2_ans += 1
    if dial == 0:
        pt1_ans += 1

def main():
    for move in moves:
        move_dial(move)

    return pt1_ans, pt2_ans