import copy
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
data.pop(0)

# With int(area[n][m]) we'll access information about position
area = [b for a in data for b in a]

# Test legal moves & if finish found
def checkMove(n, m, area):
    if (n in range(0, sizeN)) and (m in range (0, sizeM)):
        return area[n][m] != '1' and area[n][m] != '9'
    return False

def checkWin(n, m):
    return area[n][m] == '8'

def prep(pos, rel):
    for x in rel:
        if x == 'U': pos[0] -= 1
        elif x == 'R': pos[1] += 1
        elif x == 'D': pos[0] += 1
        elif x == 'L': pos[1] -= 1

def last_move(arr):
    if arr[2] == 'U': arr[1] += 1
    elif arr[2] == 'R': arr[0] -= 1
    elif arr[2] == 'D': arr[1] -= 1
    elif arr[2] == 'L': arr[0] += 1

# Retrieve starting position
def startPos():
    for idn, s in enumerate(area):
        idm = s.find('5')
        if (idm == -1):
            continue
        else:
            return idn, idm

def randMove(n, m, area):
    moves = ['U', 'D', 'R', 'L']
    while moves != []:
        move = random.choice(moves)
        if (move == 'U'):             # Up
            if checkMove(n+1, m, area):
                return n+1, m
            else:
                moves.remove(move)
        elif (move == 'R'):           # Right
            if checkMove(n, m+1, area):
                return n, m+1
            else:
                moves.remove(move)
        elif (move == 'D'):           # Down
            if checkMove(n-1, m, area):
                return n-1, m
            else:
                moves.remove(move)
        else:                       # Left
            if checkMove(n, m-1, area):
                return n, m-1
            else:
                moves.remove(move)
    if moves == []:
        return False
    
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

def rc(area, n, m, num):
    str1 = area[n]
    list1 = list(str1)
    list1[m] = num
    str1 = ''.join(list1)
    area[n] = str1
    return area

def printMap(area):
    print('_'*len(area))
    for a in area:
        print(a)
    print('_'*len(area))

def first(method):
    # Ending Node = Starting Node
    n, m = startPos()
    iteration = 0
    move_limit = (sizeN*sizeM)/3
    answ = []
    new_area = copy.deepcopy(area)

    # LookAround returns false if no win spot is around the player
    while (lookAround(n, m) == False) and (iteration <= move_limit):
        iteration += 1
        # First let's make a random guess about direction we'll face
        if randMove(n, m, new_area) == False:
            # print("Dead End. Needs a restart.")
            return False

        nn, mm = randMove(n, m, new_area)
        direction = whereDidMove(n, m, nn, mm)
        answ.append(direction)
        n, m = nn, mm

        # Update map (mark as visited)
        new_area = rc(new_area, n, m, '9')
        # printMap(new_area)
        
        if lookAround(n, m) != False:
            # print("Found Exit! At:", lookAround(n, m))
            nn, mm = lookAround(n, m)
            direction = whereDidMove(n, m, nn, mm)
            answ.append(direction)
            break

        # Move in line until wallhit
        while (moveStraight(direction, n, m, new_area) != False) and (iteration <= move_limit):

            iteration += 1

            # Maybe there's exit?
            if lookAround(n, m) != False:
                # print("Found Exit! At:", lookAround(n, m))
                nn, mm = lookAround(n, m)
                direction = whereDidMove(n, m, nn, mm)
                answ.append(direction)
                break

            # Keep moving

            # --- Update ---
            if method == True:
                if randMove(n, m, new_area) == False:
                    print("Dead End. Needs a restart.")
                    return False
                nn, mm = randMove(n, m, new_area)
             # --- ----- ---
            else:
                nn, mm = moveStraight(direction, n, m, new_area)
            direction = whereDidMove(n, m, nn, mm)
            answ.append(direction)
            n, m = nn, mm

            # Update map (mark as visited)
            new_area = rc(new_area, n, m, '9')
            # printMap(new_area)

    if iteration > move_limit:
        return False

    return answ, len(answ)

def testPath(moves, area):
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

def better_test(state1, state2, es):
    val1 = value(state1, es)
    val2 = value(state2, es)
    if val1 == val2:
        return state1[0] > state2[0]
    return bool(val1 < val2)

def probability(dE, T):
    k = 1e-2
    exp = - (dE / (k * T))
    return math.e ** exp

delta_E = lambda E1, E2: E1 - E2

def simulatedAnnealing(iters=15000, n=sizeN, m=sizeM):
    # Prepare first solution with it's Cost
    cs_n, cs_m = startPos()
    currentstate = [cs_n, cs_m]
    es = currentstate.copy()

    # Method False: old pathfind / Method True: new pathfind
    method = True
    first_answ = first(method)
    while first_answ == False:
        first_answ = first(method)
        method != method
    best_answ_ever, best_cost = first_answ
    prep(es, best_answ_ever)

    # Iteration Counter and Timer
    count = 1
    timeout = time.time() + float(tIn)
    
    # Best Ever is the cost we just found (because nothing started yet)
    best_cost_ever = best_cost
    restart = 0

    while count <= iters and time.time() < timeout:
        # print(f"({count}) Distance: {best_cost}, Time left: {timeout - time.time()}. Best Ever: {best_cost_ever}. Restart: {restart}")
        finished = False
        cs_n, cs_m = startPos()
        currentstate = [cs_n, cs_m]

        if restart == 10:
            es = currentstate.copy()
            first_answ = False
            while first_answ == False:
                method != method
                first_answ = first(method)
            solution, best_cost = first_answ

            if best_cost < best_cost_ever:
                best_cost_ever = best_cost
            
            prep(es, solution)
            restart = 0

        # Arrays to hold new answers and kinda "wrong" moves
        fin_path = []
        test_path = []

        # Temperature to allow for "maybe wrong but maybe good" moves
        # Prev to check if we're not making stupid moves though
        T = 10000
        prev = None

        # while currentstate != es:
        while currentstate != es:
            E1 = value(currentstate, es)
            
            check = testPath(fin_path, area)
            if check != False:
                restart = 0
                # print("Found New Solution! Len:", len(check), "Answ: ", check)
                if len(check) < best_cost_ever:
                    # print("It's new best solution!")
                    best_cost_ever = len(check)
                    best_answ_ever = check
                    last_move(currentstate)
                    
                # Change Values for moves
                if es[0] != currentstate[0] and es[1] != currentstate[1]:
                    es[0] = currentstate[0]
                    es[1] = currentstate[1]
                break
            
            for state in neighbor(currentstate[0], currentstate[1]):
                if state == prev: continue
                E2 = value(state, es)

                if better_test(state, currentstate, es):
                    for a in test_path:
                        fin_path.append(a[2])
                    fin_path.append(state[2])
                    test_path = []
                    prev = currentstate
                    currentstate = state
                    break

                else:
                    p = probability(delta_E(E2, E1), T)
                    if p < random.random():
                        test_path.append(state)
                        prev = currentstate
                        currentstate = state
                        break
                    
            if finished or T <= 10:
                break
            T = 0.99 * T
        count += 1
        restart += 1
    return best_answ_ever, best_cost_ever

answ = simulatedAnnealing()
print(answ[1])
final_moves = (" ".join(map(str, answ[0])))
print(final_moves, file=sys.stderr)