with open("inputs/7.txt", "r") as f:
    input_text = f.read()

lines = input_text.split()
start_beam_idx = lines[0].index("S")
def solve_puzzle(lines, start_beam_idx):
    timelines = {start_beam_idx: 1}
    beams = [start_beam_idx]
    splits = 0
    for line in lines[1:]:
        new_beams = []
        new_timelines = {}
        for beam in beams:
            if beam >= len(line) or beam < 0:
                continue
            if line[beam] == "^":
                new_beams.extend([beam-1, beam+1])
                new_timelines[beam-1] = new_timelines.get(beam-1,0)+timelines[beam]
                new_timelines[beam+1] = new_timelines.get(beam+1,0)+timelines[beam]
                splits += 1
            else:
                new_beams.append(beam)
                new_timelines[beam] = new_timelines.get(beam,0)+timelines[beam]
        beams = list(set(new_beams))
        timelines = new_timelines
    return splits, sum(timelines.values())

pt1_ans, pt2_ans = solve_puzzle(lines, start_beam_idx)
print("Part 1 ans:", pt1_ans)
print("Part 2 ans:", pt2_ans)