import copy
import time
import sys
import random

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


def first():
    # Ending Node = Starting Node
    n, m = startPos()
    iteration = 0
    move_limit = sizeN + sizeM
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


def neighborhoodSearch(solution):
    neigh_answ_list = []

    # Iterate on all moves (besides ending move - there's one way to get into the wall)
    # Get indexes of two moves "n" and "k"
    # Version: "Vertices Swap"
    for idn, n in enumerate(solution[:-1]):
        for idk, k in enumerate(solution[:-1]):

            # Skip when interchaning move with itself
            if n == k:
                continue

            # On new list perform swap of n and k
            new_answ = copy.deepcopy(solution)
            new_answ[idn], new_answ[idk] = k, n

            # Add it, if it's not present in the list
            if new_answ not in neigh_answ_list:
                neigh_answ_list.append(new_answ)

    # Sort List based on the distance
    neigh_answ_list_sorted = sorted(neigh_answ_list, key=len)
    return neigh_answ_list_sorted

# The way the guy can not move. [not used]
def makeTabuList(answ):
    answ = [w.replace('R', 'temp') for w in answ]
    answ = [w.replace('L', 'R') for w in answ]
    answ = [w.replace('temp', 'L') for w in answ]
    answ = [w.replace('U', 'temp') for w in answ]
    answ = [w.replace('D', 'U') for w in answ]
    answ = [w.replace('temp', 'D') for w in answ]
    return answ

def tabu(iters=2000, n=sizeN, m=sizeM):
    # Prepare first solution & final solution + iteratior counter
    first_answ = first()
    while first_answ == False:
        first_answ = first()
    
    solution, best_cost = first_answ
    print(solution, best_cost)

    tabu_list, best_answ_ever, count = list(), solution, 1
    timeout = time.time() + float(tIn)
    
    while count <= iters and time.time() < timeout:
        print(f"({count}) Distance: {best_cost}, Time left: {timeout - time.time()}.")
        # Neighborhood of solutions is sorted so it has best probable solution at idx 0
        neighborhood = neighborhoodSearch(solution)
        best_answ_cur_idx = 0
        best_answ_cur = neighborhood[best_answ_cur_idx]

        found = False
        while found is False:
            i = 0
            
            # Check for logic sieve for shortcuts
            if len(best_answ_cur) < len(best_answ_ever):
                best_answ_ever = best_answ_cur

                # Check if there was any better result
                if len(neighborhood) < 2:
                    continue
                else:
                    best_answ_cur_idx += 1
                    best_answ_cur = neighborhood[best_answ_cur_idx]

            # Swap best path with path from (first/current) solution 
            while i < len(best_answ_cur):
                if best_answ_cur[i] != solution[i]:
                    path_best = best_answ_cur[i]
                    path_answ = solution[i]
                    path_idx = i
                    break
                i = i + 1

            # Check if they are tabu by now, if not - swap and tabu'd them
            if [path_best, path_answ, path_idx] not in tabu_list and [path_answ, path_best, path_idx] not in tabu_list:
                tabu_list.append([path_best, path_answ, path_idx])
                tabu_list.append([path_answ, path_best, path_idx])
                found = True

                # Solution w/o distance (stored at last element)
                solution = best_answ_cur
                new_path = testPath(solution, area)
                if new_path != False:
                    if len(new_path) < len(best_answ_ever):
                        best_answ_ever = new_path
                        best_cost = len(new_path)
            else:
                new_path = testPath(best_answ_cur, area)
                if new_path != False:
                    if len(new_path) < len(best_answ_ever):
                        best_answ_ever = new_path
                        best_cost = len(new_path)
                        solution = best_answ_ever
                        tabu_list.clear()
                        found = True

                # Checking next best option
                best_answ_cur_idx = best_answ_cur_idx + 1
                if(best_answ_cur_idx > len(neighborhood)-1):
                    # print("CUR_IDX", best_answ_cur_idx, "NEIGH:", len(neighborhood))
                    break
                best_answ_cur = neighborhood[best_answ_cur_idx]

        # Maximum length of tabu list set to fixed '20'.
        if len(tabu_list) >= 20:
            tabu_list.pop(0)
        count = count + 1
    return best_answ_ever, best_cost

answ = tabu()
print(answ[1])
print(" ".join(map(str, answ[0])))