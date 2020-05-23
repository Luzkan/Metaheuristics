import math
import random
import time
import copy
import sys

# === Function ===
def yang(x, eps):
    part_loop, idx = 0.0, 1
    for xi in x:
        part_loop += eps[idx-1] * abs(xi)**idx
        idx += 1
    return part_loop

# === Assisting ===
def crossover(a, b): 
    break_point = random.randint(0, len(a))
    child_one = a[0:break_point] + b[break_point:len(a)]
    child_two = b[0:break_point] + a[break_point:len(a)]
    return (child_one, child_two)

def mutate(indiv, probability=0.8, noise=0.001):
    mutated = copy.deepcopy(indiv)
    for i, pre_mutated in enumerate(mutated):
        if random.random() < probability:
            mutated[i] = random.gauss(pre_mutated, noise)
    return mutated

def pickMate(fitnesses, rounds=3):
    best = random.randrange(len(fitnesses))
    for _ in range(1, rounds):
        n = random.randrange(len(fitnesses))
        if fitnesses[n] < fitnesses[best]:
            best = n
    return best

# === Algorithm ===
def geneticAlgorithm(max_time, x, eps, population_size=6):
    # General Starting Stuff
    number_of_couples = population_size//2
    population = []
    for _ in range(population_size):
        population.append(mutate(x))
    
    # Starting Informations about first generation
    generation = 0
    best_ever_answ = population[0]
    best_ever_score = yang(population[0], eps)

    # Lets go
    timeout = time.time() + float(max_time)
    
    while time.time() < timeout:
        scores = []
        new_generation = []

        # Score individuals in current population
        for individual in population:
            score = yang(individual, eps)
            scores.append(score)

            # Update new best
            if score < best_ever_score:
                best_ever_answ = individual
                best_ever_score = score

        # Start breeding new population
        # Breed based on relative score (better individuals are more likelly to breed with eac other)
        for _ in range(0, number_of_couples):
            new_1, new_2 = crossover(population[pickMate(scores)], population[pickMate(scores)])
            new_generation += [mutate(new_1), mutate(new_2)]

        generation += 1
        population = new_generation

    return best_ever_answ, best_ever_score

# Outputs
def taskListOutput():
    x = [x1, x2, x3, x4]
    eps = [eps1, eps2, eps3, eps4]
    answer, score = geneticAlgorithm(t_in, x, eps)
    print(" ".join(map(str, answer)), score)

def myOutput():
    x = [x1, x2, x3, x4]
    eps = [eps1, eps2, eps3, eps4]
    print("Timeout Set to:", t_in)
    print("Analysing: Yang")
    print("______")
    print("Starting X's:", x)
    print("Starting Eps's:", eps)
    print("Result:", yang(x, eps))
    print("Smelting the answer...")
    answer, score = geneticAlgorithm(t_in, x, eps)
    print("______")
    print("Output X:", answer)
    print("Result:", score)

# Standard Input
t_in, x1, x2, x3, x4, eps1, eps2, eps3, eps4 = list(map(float, input().split()))
# t_in, x1, x2, x3, x4, eps1, eps2, eps3, eps4 = [5, 2, 3, 4, 5, 0.4, 0.3, 0.2, 0.1]

# Preparing stuff based on stdin
# print("Inputs: ", t_in, x1, x2, x3, x4)
# myOutput()
taskListOutput()