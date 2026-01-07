class Safe:
    def __init__(self):
        self.dial = 50

    def move_dial(self, move):
        pt1_clicks = 0
        pt2_clicks = 0
        n_moves = move[1]
        for _ in range(n_moves):
            if move[0] == "L":
                self.dial -= 1
            elif move[0] == "R":
                self.dial += 1
            self.dial = self.dial % 100
            if self.dial == 0:
                pt2_clicks += 1
        if self.dial == 0:
            pt1_clicks += 1
        
        return pt1_clicks, pt2_clicks

def main():
    with open("inputs/1.txt", "r") as f:
        lines = f.read()

    moves = lines.split("\n")
    moves = [(move[0], int(move[1:])) for move in moves if len(move) > 0]
    pt1_ans = 0
    pt2_ans = 0
    safe = Safe()
    for move in moves:
        clicks_pt1, clicks_pt2 = safe.move_dial(move)
        pt1_ans += clicks_pt1
        pt2_ans += clicks_pt2

    return pt1_ans, pt2_ans