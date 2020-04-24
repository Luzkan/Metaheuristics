import copy
import time
import sys

# Reading input
def readInfo(path):
    with open(path, 'r') as f:
        arr = [list(map(int, b)) for b in [line.strip('\n').split(' ') for line in f]]
        return arr

path = sys.argv[1]
data = readInfo(path)

# Save Time & Number of Cities, then remove to create a matrix of distances between cities
tIn = data[0][0]
cities = data[0][1]
data.pop(0)

def first():
    # Ending Node = Starting Node
    end, visiting, distance = 0, 0, 0
    min_dist = 50000
    answ = []

    # Visit all cities sequentially selecting the smallest distance available atm
    while visiting not in answ:
        min_dist = 50000
        for city, k in enumerate(data[visiting]):
            if (k < min_dist) and (city not in answ) and (city != visiting):
                min_dist = k
                best_city = city
        answ.append(visiting)
        distance += min_dist
        visiting = best_city

    # Get back to starting node and calculate distance of that travel
    answ.append(end)
    distance += data[answ[-2]][answ[-1]] - min_dist
    return answ, distance

def neighborhoodSearch(solution):
    neigh_answ_list = []

    # Iterate on all cities (besides first/end node city)
    # Get indexes of two cities "n" and "k"
    # Version: "Vertices Swap"
    for n in solution[1:-1]:
        idx1 = solution.index(n)
        for k in solution[1:-1]:
            idx2 = solution.index(k)

            # Skip travelling from the city to itself
            if n == k:
                continue

            # On new list perform swap of n and k
            new_answ = copy.deepcopy(solution)
            new_answ[idx1], new_answ[idx2], distance = k, n, 0

            # Traverse new city list without cycle (last element removed)
            #   and check the total distance of it
            for k in new_answ[:-1]:
                nextCity = new_answ[new_answ.index(k) + 1]
                for city, dist in enumerate(data[k]):
                    if city == nextCity:
                        distance = distance + dist
            new_answ.append(distance)

            # Add it, if it's not present 
            if new_answ not in neigh_answ_list:
                neigh_answ_list.append(new_answ)

    # Sort List based on the distance
    last_idx = len(neigh_answ_list[0]) - 1
    neigh_answ_list.sort(key=lambda x: x[last_idx])
    return neigh_answ_list

def tabu(iters=500, size=cities):
    # Prepare first solution & final solution + iteratior counter
    solution, best_cost = first()
    tabu_list, best_answ_ever, count = list(), solution, 1

    timeout = time.time() + float(tIn)
    while count <= iters and time.time() < timeout:
        # print(f"({count}) Distance: {best_cost}, Time left: {timeout - time.time()}.")

        # Neighborhood of solutions is sorted
        # so it has best probable solution at idx 0
        neighborhood = neighborhoodSearch(solution)
        best_answ_cur_idx = 0
        best_answ_cur = neighborhood[best_answ_cur_idx]
        best_cost_idx = len(best_answ_cur)-1

        found = False
        while found is False:
            i = 0
            
            # Swap best city with city from (first/current) solution 
            while i < len(best_answ_cur):
                if best_answ_cur[i] != solution[i]:
                    city_best = best_answ_cur[i]
                    city_answ = solution[i]
                    break
                i = i + 1

            # Check if they are tabu by now, if not - swap and tabu'd them
            if [city_best, city_answ] not in tabu_list and [city_answ, city_best] not in tabu_list:
                tabu_list.append([city_best, city_answ])
                found = True

                # Solution w/o distance (stored at last element)
                solution = best_answ_cur[:-1]
                cost = neighborhood[best_answ_cur_idx][best_cost_idx]

                # Compare new cost with best cost, if pass - save new best answer
                if cost < best_cost:
                    best_cost = cost
                    best_answ_ever = solution
            else:
                # Checking next best option
                best_answ_cur_idx = best_answ_cur_idx + 1
                best_answ_cur = neighborhood[best_answ_cur_idx]

        # Maximum length of tabu list set to the amount of cities
        if len(tabu_list) >= size:
            tabu_list.pop(0)
        count = count + 1
    return best_answ_ever, best_cost

answ = tabu()
print(answ[1])
print(" ".join(map(str, answ[0])))