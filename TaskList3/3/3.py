import copy
import numpy as np
import time
import sys
import random
import math

# Reading input
def readInfo(path):
    with open(path, 'r') as f:
        arr = [line.strip('\n').split(' ') for line in f]
        return arr

path = sys.argv[1]
data = readInfo(path)

# Save Time & Map Size
tIn = int(data[0][0])
sizeN = int(data[0][1])
sizeM = int(data[0][2])
sIn = int(data[0][3])
pIn = int(data[0][4])
data.pop(0)
maze_length = ((sizeN-1)*(sizeM-1))

# With int(area[n][m]) we'll access information about position
area = [b for a in data for b in a]

# Test legal moves & if finish found
def checkMove(n, m, area):
    if (n in range(0, sizeN)) and (m in range (0, sizeM)):
        return area[n][m] != '1' and area[n][m] != '9'
    return False

def checkWin(n, m):
    return area[n][m] == '8'

# Retrieve starting position
def startPos():
    for idn, s in enumerate(area):
        idm = s.find('5')
        if (idm == -1):
            continue
        else:
            return idn, idm

def lookAround(n, m):
    if checkWin(n+1, m):
        return n+1, m
    elif checkWin(n, m+1):
        return n, m+1
    elif checkWin(n-1, m):
        return n-1, m
    elif checkWin(n, m-1):
        return n, m-1
    else:
        return False

def whereDidMove(n, m, new_n, new_m):
    if (new_n - n) == -1:
        return 'U'
    if (new_n - n) == 1:
        return 'D'
    if (new_m - m) == -1:
        return 'L'
    if (new_m - m) == 1:
        return 'R'

def moveStraight(direction, n, m, area):
    if direction == 'U':
        if checkMove(n-1, m, area):
            return n-1, m
    elif direction == 'R':
        if checkMove(n, m+1, area):
            return n, m+1
    elif direction == 'D':
        if checkMove(n+1, m, area):
            return n+1, m
    elif direction == 'L':
        if checkMove(n, m-1, area):
            return n, m-1
    return False

def testPath(moves):
    n, m = startPos()
    checked = []
    for move in moves:
        if (moveStraight(move, n, m, area)) != False:
            n, m = moveStraight(move, n, m, area)
            checked.append(move)
            if lookAround(n, m) != False:
                nn, mm = lookAround(n, m)
                direction = whereDidMove(n, m, nn, mm)
                checked.append(direction)
                return checked
        else:
            return False
    return False

def value(state, es):
    return abs(es[0] - state[0]) + abs(es[1] - state[1])

def neighbor(n, m):
    if area[n+1][m] == str(0): # Down
        yield [n+1, m, 'D']
    if area[n][m-1] == str(0): # Left
        yield [n, m-1, 'L']
    if area[n-1][m] == str(0): # Up
        yield [n-1, m, 'U']
    if area[n][m+1] == str(0): # Right
        yield [n, m+1, 'R']


### ===== Genetic Algorithm =====

# Get Populations based on sIn (number of input populations)
def getPopulation():
    populations = []
    
    # Reading starts from lastline
    last_line = -1
    for _ in range(0, sIn):
        populations.append(data[last_line][0])
        last_line -= 1
    
    return populations

# So the fitness is basically the length of the array
# If the move doesn't reach end - return big value
def fitness(test_path):
    new = testPath(test_path)
    if new != False:
        return len(new), new
    return 9999999, new

# Gets all scores in a array and best route with its score
def scorePopulation(population):
    scores = []

    best = ""
    best_cost = 999999999

    for i in range(0, len(population)):
        current, new = fitness(population[i])
        scores += [current]

        if current < best_cost:
            best = new
            best_cost = current

    return scores, best, best_cost

array_of_zero = []

# Parents decide to meet each other and create a new_gen child
def crossover(a, b): 
    break_point = random.randint(0, maze_length)
    child_one = a[0:break_point] + b[break_point:maze_length]
    child_two = b[0:break_point] + a[break_point:maze_length]
    return (child_one, child_two)

# Do not make stupid moves
def educate(population):
    new_population = []
    for route in population:
        new_route_1 = route.replace("DU", "")
        new_route_2 = new_route_1.replace("UD", "")
        new_route_3 = new_route_2.replace("LR", "")
        new_route = new_route_3.replace("RL", "")
        new_population.append(new_route)

    return new_population

# Modify the gene (split and paste)
def mutate(route, probability):
    new_route = copy.deepcopy(route)
    for i in range(0, len(new_route)):
        if random.random() < probability:

            low_cut = random.randint(0, len(route))
            up_cut = random.randint(low_cut, len(route))

            subset_individual = list(new_route[low_cut:up_cut])

            random.shuffle(subset_individual)
            new_route = route[0:low_cut] + ''.join(subset_individual) + route[up_cut: maze_length]

    return new_route

# Picking Mate based on their scores
# Reminder: Routes that do not work are big nums 
def pickMate(scores):
    array = np.array(scores)
    temp = array.argsort()
    ranks = np.empty_like(temp)
    ranks[temp] = np.arange(len(array))
    fitness = [len(ranks) - x for x in ranks]
    cum_scores = copy.deepcopy(fitness)
    for i in range(1, len(cum_scores)):
        cum_scores[i] = fitness[i] + cum_scores[i-1]
        
    probs = [x / cum_scores[-1] for x in cum_scores]
    rand = random.random()
    for i in range(0, len(probs)):
        if rand < probs[i]:
            return i

def geneticAlgorithm(iters=99999999, n=sizeN, m=sizeM):
    inputPopulation = getPopulation()
    population = inputPopulation

    # Number of meetings based on 'p' in value.
    number_of_couples = math.ceil(pIn/2)
    kill_child = False
    if pIn % 2:
        kill_child = True

    # Variables
    mutation_chance = 0.3
    keep_best = True
    keep_past = True
    use_motivation = True
    motivation_fresh = 15000
    motivation = motivation_fresh

    # Iteration Counter (Generations_) and Timer
    gen = 1
    timeout = time.time() + float(tIn)
    timenow = time.time()
    
    # Best Ever is the cost we just found (because nothing started yet)
    best_answ_ever = min(population, key=len)
    best_score_ever = len(best_answ_ever)
    best_score = len(best_answ_ever)

    while gen <= iters and time.time() < timeout:
        # print(f"[Dev] ({gen}) Costs: ({best_score}/{best_score_ever}), Time left: {timeout - time.time()}")

        if motivation == 0:
            population = getPopulation()
            motivation = motivation_fresh

        new_population = []

        # Get Scores and best route of current population
        scores, best, best_score = scorePopulation(population)
        # print(f"[Dev] Pop: {population}")
        # print(f"[Dev] Scr: {scores}")

        # Update new best score if found
        if best_score < best_score_ever:
            best_as_str = ""
            for move in best:
                best_as_str += move
            # print(f"[Dev] ({gen}) New best! ({best_score_ever} -> {best_score}) Time: {time.time() - timenow} ({best_answ_ever} -> {best_as_str}), Timeleft: {timeout - time.time()}")
            best_score_ever = best_score
            best_answ_ever = best_as_str
            motivation = motivation_fresh

        # Start breeding new population
        # Breed based on relative score (better individuals are more likelly to breed with eac other)
        for _ in range(0, number_of_couples):
            new_1, new_2 = crossover(population[pickMate(scores)], population[pickMate(scores)])
            new_population += [new_1, new_2]
            
        # Kill if exceeded population limit
        if kill_child:
            new_population.pop(0)

        # Mutate a bit the gene pool
        for i in range(0, len(new_population)):
            new_population[i] = mutate(new_population[i], mutation_chance)

        # Keep the best route in the population
        if keep_best:
            new_population.pop(0)
            new_population += [best_answ_ever]

        # Remember input ancestor
        if keep_past:
            new_population.pop(0)
            ancestor = random.choice(inputPopulation)
            new_population += [ancestor]

        # New Population replaces the current one
        population = copy.deepcopy(educate(new_population))
        gen += 1

        # Not used anymore as it finds global optimum too fast :3
        if use_motivation:
            mutation_chance = random.choice([0.1, 0.3, 0.5, 0.7, 0.9])
            motivation -= 1
    return best_score_ever, best_answ_ever

def main():
    answ = geneticAlgorithm()
    print(answ[0])
    print(answ[1], file=sys.stderr)

if __name__ == "__main__":
    main()
