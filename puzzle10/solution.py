with open("puzzle10/input.txt", "r") as f:
    input_text = f.read()

from copy import deepcopy
from itertools import permutations, combinations

def parse_button(button_text):
    return [int(x) for x in button_text.strip("()").split(",")]

def parse_lights(light_text):
    txt = light_text.strip("[]")
    return [1 if chr == "#" else 0 for chr in txt]
    
class Machine():
    def __init__(self, lights, buttons):
        self.lights = lights
        self.buttons = buttons
    
    def is_valid_solution(self, solution):
        flicks = {}
        for idx, to_press in enumerate(solution):
            button = self.buttons[idx]
            if to_press == 1:
                for num in button:
                    flicks[num] = (flicks.get(num, 0) + 1) % 2
        for idx,v in enumerate(self.lights):
            if flicks.get(idx, 0) % 2 != v:
                return False
        return True

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"{" ".join([str(x) for x in self.lights])} {self.buttons}"

def parse_machine(line):
    things = line.split(" ")
    lights = parse_lights(things[0])
    buttons = [parse_button(b) for b in things[1:-1]]
    return Machine(lights, buttons)

def parse_input(input_text):
    lines = [line for line in input_text.split("\n") if len(line) > 0]
    return [parse_machine(line) for line in lines]

def unique_binary_perms(ones, zeros):
    result = []
    n = ones + zeros
    for ones_positions in combinations(range(n), ones):
        arr = [0] * n
        for i in ones_positions:
            arr[i] = 1
        result.append(arr)
    return result

def solve_machine_pt1(machine):
    for buttons_on in range(len(machine.buttons)+1):
        for perm in unique_binary_perms(buttons_on, len(machine.buttons)-buttons_on):
            p = [int(x) for x in perm]
            if machine.is_valid_solution(p):
                print(buttons_on)
                return buttons_on
    raise ValueError

def solve_pt1(machines):
    return sum([solve_machine_pt1(machine) for machine in machines])

machines = parse_input(input_text)
print("Part 1 answer:", solve_pt1(machines))