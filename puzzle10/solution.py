with open("puzzle10/input.txt", "r") as f:
    input_text = f.read()

from copy import deepcopy
from itertools import permutations, combinations
import numpy as np
from pulp import *
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
            if coefficient != 0:
                terms.append(f"{alphabet[idx]}")
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
        coeffs = [0]*len(buttons)
        for idx2, button in enumerate(buttons):
            if idx1 in button:
                coeffs[idx2] = 1
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

def compute_new_bounds(simeq, upper_bounds, lower_bounds):
    num_terms = len(simeq[0].coefficients)
    changed = False
    for term_idx in range(num_terms):
        for eq in simeq:
            if eq.coefficients[term_idx] == 1:
                other_terms = list(range(num_terms))
                other_terms.remove(term_idx)
                other_terms = [term for term in other_terms if eq.coefficients[term] == 1]
                # Compute new upper bounds
                this_eq_ub = eq.rhs
                for other_term in other_terms:
                    this_eq_ub -= lower_bounds[other_term]
                new_upper_bound = min(this_eq_ub, upper_bounds[term_idx])
                if new_upper_bound != upper_bounds[term_idx]:
                    upper_bounds[term_idx] = new_upper_bound
                    changed = True

                # Compute new lower bounds
                this_eq_lb = eq.rhs
                for other_term in other_terms:
                    this_eq_lb -= upper_bounds[other_term]
                new_lower_bound = max(this_eq_lb, lower_bounds[term_idx])
                if new_lower_bound != lower_bounds[term_idx]:
                    lower_bounds[term_idx] = new_lower_bound
                    changed = True
    return changed


def setup_bounds(simeq):
    num_terms = len(simeq[0].coefficients)
    upper_bounds = {}
    lower_bounds = {}
    for i in range(num_terms):
        upper_bounds[i] = math.inf
        lower_bounds[i] = 0
    return upper_bounds, lower_bounds

def get_bounds(simeq, existing_bounds=None):
    upper_bounds, lower_bounds = setup_bounds(simeq)
    if existing_bounds is not None:
        for k,v in existing_bounds.items():
            lower_bounds[k] = v[0]
            upper_bounds[k] = v[1]
    while True:
        changed = compute_new_bounds(simeq, upper_bounds, lower_bounds)
        if not changed:
            # We want to press the button which reduces the upper bounds of as many buttons which can have their upper bounds reduced as possible.
            range_sizes = [abs(upper_bounds[k]-lower_bounds[k])+1 for k in upper_bounds.keys()]
            break
        
    bounds = {}
    for k in upper_bounds.keys():
        bounds[k] = (lower_bounds[k], upper_bounds[k])
    return bounds
            

def solve_simeq(simeq):
    bounds = get_bounds(simeq)
    return [bound[0] for bound in bounds.values()]

def get_matches(priorities, candidate):
    matches = 0
    for priority in priorities:
        if priority in candidate:
            matches += 1
        else:
            return matches * 10000 + len(candidate) # God damn this is a hack. Length of candidate needs to be baked on.

def solve_machine_pt2(machine):
    presses = 0
    buttons = [tuple(e) for e in machine.buttons]
    joltages = machine.joltages
    original_joltages = deepcopy(joltages)
    simeq = get_equations(buttons, joltages)
    coefficients = np.array([eq.coefficients for eq in simeq])
    dependent_variables = np.array([eq.rhs for eq in simeq])
    n=len(coefficients[0])
    variables = []
    problem = LpProblem("MinimizeSum", LpMinimize)
    for i in range(n):
        variables.append(LpVariable(f"x{i}", 0, cat=LpInteger))
    problem += sum(variables)
    for idx, coeff in enumerate(coefficients):
        lhs = sum([c*v for c, v in zip(coeff, variables)])
        rhs = dependent_variables[idx]
        problem += lhs >= rhs
        problem += lhs <= rhs
    status = problem.solve(PULP_CBC_CMD(msg=False))
    return sum([int(var.value()) for var in variables])

def solve_pt1(machines):
    return sum([solve_machine_pt1(machine) for machine in machines])

def solve_pt2(machines):
    return sum([solve_machine_pt2(machine) for machine in machines])

machines = parse_input(input_text)
print("Part 1 answer:", solve_pt1(machines))
print("Part 2 answer:", solve_pt2(machines))