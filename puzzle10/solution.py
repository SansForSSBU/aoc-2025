with open("puzzle10/input.txt", "r") as f:
    input_text = f.read()

from copy import deepcopy
from itertools import permutations, combinations
import math

def parse_button(button_text):
    return [int(x) for x in button_text.strip("()").split(",")]

def parse_lights(light_text):
    txt = light_text.strip("[]")
    return [1 if chr == "#" else 0 for chr in txt]
    
class Machine():
    def __init__(self, lights, buttons, joltages):
        self.lights = lights
        self.buttons = buttons
        self.joltages = joltages
    
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
        return f"{" ".join([str(x) for x in self.lights])} {self.buttons} {self.joltages}"

def parse_joltages(joltage_text):
    return [int(x) for x in joltage_text.strip("{}").split(",")]

def parse_machine(line):
    things = line.split(" ")
    lights = parse_lights(things[0])
    buttons = [parse_button(b) for b in things[1:-1]]
    joltages = parse_joltages(things[-1])
    return Machine(lights, buttons, joltages)

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
                return buttons_on
    raise ValueError

def read_simultaneous_equations(buttons, joltages):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    equations = []
    for idx, joltage in enumerate(joltages):
        letters = []
        for idx2, button in enumerate(buttons):
            if idx in button:
                letters.append(alphabet[idx2])
        equations.append("+".join(letters) + "=" + str(joltage))
    
    return "\n".join(equations)

class Equation():

    def __init__(self, coefficients, rhs):
        self.coefficients = coefficients
        self.rhs = rhs

    def __str__(self):
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        terms = []
        for idx, coefficient in enumerate(self.coefficients):
            terms.append(f"{coefficient}{alphabet[idx]}")
        LHS = " + ".join(terms)
        return f"<{LHS} = {self.rhs}>"
    
    def __repr__(self):
        return self.__str__()
    
    def multiplied(self, factor):
        # Multiply self by factor. Returns new eq without modifying existing.
        new_eq = deepcopy(self)
        for idx in range(len(new_eq.coefficients)):
            new_eq.coefficients[idx] *= factor
        new_eq.rhs *= factor
        return new_eq

    def subtract_other_eq(self, other_eq):
        # Subtract other_eq from self. Returns new eq without modifying existing.
        new_eq = deepcopy(self)
        for idx in range(len(new_eq.coefficients)):
            new_eq.coefficients[idx] -= other_eq.coefficients[idx]
        new_eq.rhs -= other_eq.rhs
        return new_eq


    def num_terms(self):
        return len([coeff for coeff in self.coefficients if coeff != 0])


def get_equations(buttons, joltages):
    pass
    equations = []
    for idx1, joltage in enumerate(joltages):
        coeffs = [float(0)]*len(buttons)
        for idx2, button in enumerate(buttons):
            if idx1 in button:
                coeffs[idx2] = float(1)
        equations.append(Equation(coeffs, joltage))
    return equations

def print_simeq(simeq):
    print("\n".join([str(x) for x in simeq]))

def get_most_common_term(simeq):
    num_terms = len(simeq[0].coefficients)
    best = 0
    best_idx = None
    for idx in range(num_terms):
        num_occurrences = 0
        for eq in simeq:
            if eq.coefficients[idx] != 0:
                num_occurrences += 1
        if num_occurrences > best:
            best_idx = idx
            best = num_occurrences
    return best_idx

def solve_simeq(simeq):
    total_num_terms = len(simeq[0].coefficients)
    while True:
        subtractable_eq = simeq.pop(0)
        for idx, eq in enumerate(simeq):
            new_eq = eq.subtract_other_eq(subtractable_eq)
            if new_eq.num_terms() <= eq.num_terms():
                simeq[idx] = new_eq
            new_eq = eq.subtract_other_eq(subtractable_eq.multiplied(-1))
            if new_eq.num_terms() <= eq.num_terms():
                simeq[idx] = new_eq

        simeq.append(subtractable_eq)
        pass
        for eq in simeq:
            if eq.num_terms() == 1:
                pass
        # TODO: Search for 1 coeff = 1 number cases now in simeq.

def solve_machine_pt2(machine):
    pass
    buttons = [tuple(e) for e in machine.buttons]
    joltages = machine.joltages
    simeq = get_equations(buttons, joltages)
    answers = solve_simeq(simeq)
    # The best buttons affect the most joltages. Optimize to press these as much as possible?
    # Take lowest joltage. Get buttons which affect it.
    # Filter by which include the largest joltage.
    # If none do, consider the 2nd largest joltage.
    # If multiple do, consider the 2nd largest joltage.
    pass

def solve_pt1(machines):
    return sum([solve_machine_pt1(machine) for machine in machines])

def solve_pt2(machines):
    return sum([solve_machine_pt2(machine) for machine in machines])

machines = parse_input(input_text)
print("Part 1 answer:", solve_pt1(machines))
print("Part 2 answer:", solve_pt2(machines))