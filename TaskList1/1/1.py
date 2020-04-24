import math
import random
import time
import sys

# Vector Norm
def vn(x):
    return math.sqrt(sum(xi**2 for xi in x))

# Functions
def happycat(x):
    return (((vn(x)**2) - 4)**2)**(1/8) + ((1/4)*((1/2)*((vn(x))**2)+sum(x))) + (1/2)

def griewank(x):
    part1 = 0
    part2 = 1
    for xi in x:
        part1 += (xi**2)/4000
    for i, xi in enumerate(x):
        part2 *= (math.cos(xi/math.sqrt(i+1)))
    return 1 + part1 - part2 

# Local Searches
def localSearchCat(xs, rand=0.05):
    xc = xs
    timeout = time.time() + float(tIn)
    while time.time() < timeout:
        y = [xi+random.uniform(-rand, rand) for xi in xc]
        if happycat(y) <= happycat(xc):
            xc = y
    return xc

def localSearchGriew(xs, rand=0.05):
    xc = xs
    timeout = time.time() + float(tIn)
    while time.time() < timeout:
        y = [xi+random.uniform(-rand, rand) for xi in xc]
        if griewank(y) <= griewank(xc):
            xc = y
    return xc

# Outputs
def taskListOutput():
    if(alg == 'Hypercat'):
        x = [random.uniform(-10, 10), random.uniform(-10, 10), random.uniform(-10, 10), random.uniform(-10, 10)]
        answer = localSearchCat(x, 0.1)
        print(" ".join(map(str, answer)), happycat(answer))
    else:
        x = [random.uniform(-10, 10), random.uniform(-10, 10), random.uniform(-10, 10), random.uniform(-10, 10)]
        answer = localSearchGriew(x, 0.1)
        print(" ".join(map(str, answer)), griewank(answer))

def myOutput():
    x = [random.uniform(-10, 10), random.uniform(-10, 10), random.uniform(-10, 10), random.uniform(-10, 10)]
    print("Timeout Set to:", tIn)
    print("Analysing:", alg)
    print("______")
    print("Starting X:", x)

    if(alg == 'Hypercat'):
        print("Result:", happycat(x))
        print("Performing local search...")
        answer = localSearchCat(x)
        print("______")
        print("Output X:", answer)
        print("Result:", happycat(answer))
    else:
        print("Result:", griewank(x))
        print("Performing local search...")
        answer = localSearchGriew(x)
        print("______")
        print("Output X:", answer)
        print("Result:", griewank(answer))

# Standard Input
tIn = sys.argv[1]
hIn = sys.argv[2]

# Preparing stuff based on stdin
alg = 'Hypercat' if hIn == '0' else 'Griewank'
print("test:", hIn, alg)
taskListOutput()

# =============================
# Below is my own investigation of the range (delta) that is best suited for the algorithm.
#   
# Info:
#   - Performed on 30 loops,
#   - Ranges: [1, 0.1, 0.05, 0.01, 0.005, 0.001, 0.0001, 0.00001]
#   - Time: 15s
#   - Starting X: Random from range (-10, 10) for all xi.
#
# Results:
#   As it turns out:
#       - for the cat, the best interferation range is "0.1"
#       - for griew, all were about as good as each other with a difference of "+/- 0.8"
#           with the best result in "0.1"

# Optimization for random range
def optimize():
    rangeBucket = [1, 0.1, 0.05, 0.01, 0.005, 0.001, 0.0001, 0.00001]
    answerBucketCat = [0, 0, 0, 0, 0, 0, 0, 0]
    answerBucketGriew = [0, 0, 0, 0, 0, 0, 0, 0]

    for i, r in enumerate(rangeBucket):
        print("[Cat] Range Test:", r)
        for x in range(1):
            print("Loop:", x)
            x = [random.uniform(-10, 10), random.uniform(-10, 10), random.uniform(-10, 10), random.uniform(-10, 10)]
            answer = localSearchCat(x, r)
            answerBucketCat[i] += happycat(answer)

    for i, r in enumerate(rangeBucket):
        print("[Griewank] Range Test:", r)
        for x in range(1):
            print("Loop:", x)
            x = [random.uniform(-10, 10), random.uniform(-10, 10), random.uniform(-10, 10), random.uniform(-10, 10)]
            answer = localSearchGriew(x, r)
            answerBucketGriew[i] += griewank(answer)

    print("Optimization Test for Hypercat:")
    print("Ranges:", rangeBucket)
    print("[Cat]", answerBucketCat)
    print("[Grw]", answerBucketGriew)


# optimize()

    # Results for t = 15s (sum of all results, not divided by n repetitions)
    # =======
    # Ranges: [1, 0.1, 0.05, 0.01, 0.005, 0.001, 0.0001, 1e-05]
    # [Cat] [0.8343747616690208, 0.6789672805580174, 2.29321677965921, 5.2544444086956315, 5.061208766480429, 8.902825418425504, 5.708330858625791, 107.56173767392524]
    # [Grw] [0.262530624247313, 0.21194578528789465, 0.40662021567303874, 0.32285161449322697, 0.3795067725438931, 0.349937329885328, 0.4065287299455518, 0.33512308570451566]