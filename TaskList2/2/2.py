import copy
import time
import random
import sys
import math

# Reading input
def readInfo(path):
    with open(path, 'r') as f:
        arr = [list(map(int, b)) for b in [line.strip('\n').split(' ') for line in f]]
        return arr

path = sys.argv[1]
data = readInfo(path)

# Save Time & Matrix Size, MinBlockSize, AvailableValues
t_in, size_n, size_m, min_block = data[0][0], data[0][1], data[0][2], data[0][3]
data.pop(0)

morg = copy.deepcopy(data)
m = copy.deepcopy(data)

values = [0, 32, 64, 128, 160, 192, 223, 255]

# print("Time:", t_in, "Size: [", size_n, "x", size_m, "] MinBlock:", min_block)

def calc_dist():
    part1 = (1/(size_n*size_m))
    part2 = 0
    for i in range(size_n):
        for j in range(size_m):
            part2 += (morg[i][j] - m[i][j])**2
    distance = part1 * part2
    return distance

row_b_max = 0
col_b_max = 0
offset_row = []
offset_col = []

def prep():
    row_b_max = int(size_n / min_block)
    col_b_max = int(size_m / min_block)

    offset_row = []
    offset_col = []

    # Offsets
    for row_b in range(row_b_max):
        offset_row.append(row_b*row_b_max)

    for col_b in range(col_b_max):
        offset_col.append(col_b*col_b_max)

    # Filling with Random Numbers, keeping block info
    for row_b in range(row_b_max):
        for col_b in range(col_b_max):
            rand_num = random.choice(values)
            if col_b != col_b_max-1 and row_b != row_b_max-1:
                new_block = {
                    "row" : row_b*min_block,
                    "col" : col_b*min_block,
                    "size_col" : min_block,
                    "size_row" : min_block,
                    "value" : rand_num
                    }
            # Filling reminding space vert / horz
            elif col_b == col_b_max-1 and row_b == row_b_max-1:
                new_block = {
                    "row" : row_b*min_block,
                    "col" : col_b*min_block,
                    "size_col" : size_m-(min_block*col_b),
                    "size_row" : size_n-(min_block*row_b),
                    "value" : rand_num
                    }
            # Filling reminding space vertically
            elif col_b == col_b_max-1:
                new_block = {
                    "row" : row_b*min_block,
                    "col" : col_b*min_block,
                    "size_col" : size_m-(min_block*col_b),
                    "size_row" : min_block,
                    "value" : rand_num
                    }
            # Filling reminding space horizontally
            elif row_b == row_b_max-1:
                new_block = {
                    "row" : row_b*min_block,
                    "col" : col_b*min_block,
                    "size_col" : min_block,
                    "size_row" : size_n-(min_block*row_b),
                    "value" : rand_num
                    }

            block_list.append(new_block)

def neighbors(radius, rowNumber, columnNumber):
    return [[m[i][j] if  i >= 0 and i < len(m) and j >= 0 and j < len(m[0]) else -1
                for j in range(columnNumber-1-radius, columnNumber+radius)]
                    for i in range(rowNumber-1-radius, rowNumber+radius)]

# Row / Column - SizeX / SizeY - Value
block_list = []

def init_max_fill(value):
    for row_b in range(row_b_max):
        for col_b in range(col_b_max):
            block_list.append(row_b*row_b_max, col_b*col_b_max, min_block, min_block, value)

def init_max_fill_rand():
    # block_list = []
    for row_b in range(row_b_max):
        for col_b in range(col_b_max):
            rand_num = random.choice(values)
            block_list.append(row_b*row_b_max, col_b*col_b_max, min_block, min_block, rand_num)

def split_horiz(block):
    # print("[DEV] Splitting Horizontally: ", block)

    new_block = {
        "row" : block["row"]+int(block["size_row"]/2),
        "col" : block["col"],
        "size_row" : int(block["size_row"]/2),
        "size_col" : int(block["size_col"]),
        "value" : random.choice(values)
        }
    block_list.append(new_block)
    block["size_row"] = int(block["size_row"]/2)

def split_verti(block):
    # print("[DEV] Splitting Vertically: ", block)

    new_block = {
        "row" : block["row"],
        "col" : block["col"]+int(block["size_col"]/2),
        "size_row" : int(block["size_row"]),
        "size_col" : int(block["size_col"]/2),
        "value" : random.choice(values)
        }
    block_list.append(new_block)
    block["size_col"] = int(block["size_col"]/2)

def split_logic():
    can_split_list_horiz = [block for block in block_list if block["size_row"] == min_block*2] 
    can_split_list_verti = [block for block in block_list if block["size_col"] == min_block*2] 

    if len(can_split_list_horiz) != 0 and len(can_split_list_verti) != 0:
        if random.choice([True, False]) == True:
            block = random.choice(can_split_list_horiz)
            split_horiz(block)
        else:
            block = random.choice(can_split_list_verti)
            split_verti(block)

    elif len(can_split_list_horiz) != 0:
        block = random.choice(can_split_list_horiz)
        split_horiz(block)

    elif len(can_split_list_verti) != 0:
        block = random.choice(can_split_list_verti)
        split_verti(block)
    # else:
        # print("[DEV] Split: Fail")

def merge_logic():
    can_merge_list_horiz = []
    can_merge_list_verti = []

    for block in block_list:
        for n_b in block_list:
            if block["value"] == n_b["value"]:
                if block["row"] + block["size_row"] == n_b["row"]:
                    if block["col"] + block["size_col"] == n_b["col"] + n_b["size_col"]:
                        can_merge_list_horiz.append([block, n_b])

    for block in block_list:
        for n_b in block_list:
            if block["value"] == n_b["value"]:
                if block["col"] + block["size_col"] == n_b["col"]:
                    if block["row"] + block["size_row"] == n_b["row"] + n_b["size_row"]:
                        can_merge_list_verti.append([block, n_b])

    if len(can_merge_list_horiz) != 0 and len(can_merge_list_verti) != 0:
        if random.choice([True, False]) == True:
            blocks = random.choice(can_merge_list_horiz)
            blocks[0]["size_row"] += blocks[1]["size_row"]
            block_list.remove(blocks[1])
        else:
            blocks = random.choice(can_merge_list_verti)
            blocks[0]["size_col"] += blocks[1]["size_col"]
            block_list.remove(blocks[1])
        # print("[DEV] Merged blocks:", blocks)
            
    elif len(can_merge_list_horiz) != 0:
        blocks = random.choice(can_merge_list_horiz)
        blocks[0]["size_row"] += blocks[1]["size_row"]
        block_list.remove(blocks[1])
        # print("[DEV] Merged blocks:", blocks)

    elif len(can_merge_list_verti) != 0:
        blocks = random.choice(can_merge_list_verti)
        blocks[0]["size_col"] += blocks[1]["size_col"]
        block_list.remove(blocks[1])
        # print("[DEV] Merged blocks:", blocks)
    # else:
        # print("[DEV] Merge: Fail")
    
which = ["hmm"]

def resize_logic():
    can_resize_list_horiz = [block for block in block_list if block["size_row"] > min_block] 
    can_resize_list_verti = [block for block in block_list if block["size_col"] > min_block] 

    # [X X X O O O] -> [X X O O O O]
    if len(can_resize_list_horiz) != 0 and len(can_resize_list_verti) != 0:
        if random.choice([True, False]) == True:
            block = random.choice(can_resize_list_horiz)
            for n_b in block_list:
                if block["row"] + block["size_row"] == n_b["row"]:
                    block["size_row"] -= 1
                    n_b["row"] -= 1
                    which[0] = "#1"
                    break
        else:
            block = random.choice(can_resize_list_verti)
            for n_b in block_list:
                if block["col"] + block["size_col"] == n_b["col"]:
                    block["size_col"] -= 1
                    n_b["col"] -= 1
                    which[0] = "#2"
                    break

    elif len(can_resize_list_horiz) != 0:
        block = random.choice(can_resize_list_horiz)
        for n_b in block_list:
            if block["row"] + block["size_row"] == n_b["row"]:
                block["size_row"] -= 1
                n_b["row"] -= 1
                which[0] = "#3"
                break

    elif len(can_resize_list_verti) != 0:
        block = random.choice(can_resize_list_verti)
        for n_b in block_list:
            if block["col"] + block["size_col"] == n_b["col"]:
                block["size_col"] -= 1
                n_b["col"] -= 1
                which[0] = "#4"
                break

test = ["what"]

def try_improve(hard):

    improvements = ['intensify', 'swap']
    if hard == True:
        improvements = ['intensify', 'swap', 'resize', 'split', 'merge']

    what = random.choice(improvements)
    test[0] = what

    if what == 'intensify':
        block = random.choice(block_list)
        # print("[DEV] Intensify: ", block)
        block["value"] = random.choice([val for val in values if val != block["value"]])

    elif what == 'resize':
        resize_logic()

    elif what == 'split':
        split_logic()

    elif what == 'merge':
        merge_logic() 

    elif what == 'swap':
        b_1 = random.choice(block_list)
        b_2 = random.choice(list(filter(lambda b: b != b_1, block_list)))
        b_1["value"], b_2["value"] = b_2["value"], b_1["value"]
        # print("[DEV] Swap: ", b_1, " with ", b_2)
        
def update_m():
    for block in block_list:
        for x in range(block["size_row"]):
            for y in range(block["size_col"]):
                m[block["row"]+x][block["col"]+y] = block["value"]

def try_better(hard):
    try_improve(hard)
    update_m()

def probability(dE, T):
    k = 1e-2
    exp = (dE / (k * T))
    return math.e ** exp

def blocks_backup(b_backup):
    block_list.clear()
    for entry in b_backup:
        block_list.append(entry)

def debug_test():
    for a in block_list:
        if a["size_col"] < 4 or a["size_row"] < 4:
            print("Error Detected!")
            for b in block_list:
                print(b)
            print(test)
            print(which)
            while True:
                pass

def annealing(iters=5000000):
    # Prepare first solution randomly and get it's cost
    prep()
    update_m()
    best_cost = calc_dist()

    # Save the cost as best_cost_ever, make backups
    best_cost_ever = best_cost
    best_m_ever = copy.deepcopy(m)
    best_b_ever = copy.deepcopy(block_list)
    b_backup = copy.deepcopy(block_list)

    # Iteration Counter and Timer
    hard = False
    optimize = 0
    count = 1
    last_found = 0
    timeout = time.time() + float(t_in)    

    while count <= iters and time.time() < timeout:
        # print(f"({count}) Distance: {best_cost}, Time left: {timeout - time.time()}. Best Ever: {best_cost_ever}. Since Last Found: {last_found}. Hard: {hard}")

        # Temperature and Restarting Indicator
        temp = 50000
        blocks_backup(b_backup)
        best_cost = best_cost_ever

        # Well, we can reinit start pos to rand if nothing was found after x time, why not
        if last_found % 125 == 0:
            if hard == False:
                block_list.clear()
                prep()
                b_backup = copy.deepcopy(block_list)
            else:
                b_backup = copy.deepcopy(best_b_ever)

        if last_found == 300:
            b_backup = copy.deepcopy(best_b_ever)
            optimize += 1
            last_found = 0
        
        if optimize == 30:
            hard = True

        while temp >= 10**(-4):

            # Change Matrix a bit and Analyze
            try_better(hard)
            new_cost = calc_dist()
            delta = best_cost - new_cost

            # debug_test()

            # Well it's just better, save
            if delta > 0 or math.exp((best_cost - new_cost) / temp) > random.random():
                best_cost = new_cost
                b_backup = copy.deepcopy(block_list)
                if best_cost < best_cost_ever:
                    best_b_ever = copy.deepcopy(block_list)
                    best_m_ever = copy.deepcopy(m)
                    b_backup = copy.deepcopy(block_list)
                    best_cost_ever = best_cost
                    last_found = 0
            else:
                blocks_backup(b_backup)

            temp = 0.5 * temp

        last_found += 1
        count += 1

    return best_cost_ever, best_m_ever, best_b_ever
result = annealing()
print(result[0])
for a in result[1]:
    print(a, file=sys.stderr)

# print("Best Distance Ever:", result[0])
