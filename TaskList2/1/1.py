import math
import random
import time
import sys

# Functions
def salomon(x):
    part_loop = 0
    for xi in x:
        part_loop += xi**2

    part1 = math.cos((2*math.pi)*math.sqrt(part_loop))
    part2 = 0.1 * math.sqrt(part_loop)

    return 1 - part1 + part2

# Boltzman - but actually I decided to not use it...
def probability(dE, T):
    k = 1e-2
    exp = - (dE / (k * T))
    return math.e ** exp

def simulatedAnnealing(t_in, xs):
    # Let's start by init the time we have to analysise
    timeout = time.time() + float(t_in)

    # See the way I understand Simulated Annealing
    # First I declare my own 'Very High' temperature
    temp = 10**10

    # I define it as time left in seconds times amp
    # ---
    # It's like brute-forcing for answer
    # As time passes by, the temperature decreases
    # ---
    # So at first we end up with 'a answer' that we don't
    # really care that much about how good it really is
    # ---
    # But as our temperature goes down, we will be more precise
    # and at the very end we will be very selective for next answers

    # Let's start by initializing the first answer
    best_answ = xs
    xc = xs

    while time.time() < timeout:
        # Refreshing temp, to hatch for any other answer maybe
        temp = 10**10

        while time.time() < timeout and temp > 0:
            
            # Roll for new answer
            n = [xi * random.gauss(1, 0.1) for xi in xc]

            # Calculate the difference 
            delta = salomon(xc) - salomon(n)

            # If this answer is just better -> accept it, let's go!
            if delta > 0:
                xc = n

            # Well, the answer isn't better but let's check it with temperature
            #   const^(negative_num / something huge) ---> ~ 1.0
            #   the closer the negative_num to 0
            #   and the bigger temp implies the bigger chance to try that answer
            elif math.exp(delta/temp) > random.random():
                xc = n

            if salomon(xc) < salomon(best_answ):
                best_answ = xc

            # Calculate the temperature
            # The less time we get, the more precise we are
            # temp = ((timeout - time.time())*temp)/2
            temp = temp*0.5

    return best_answ

# I think that's alright and that's quite good in comparision to
# Hill Climbing -> where we can be stuck in local minima
# Random Walk -> probably never gett_ing best solution (it doesn't converge, right?)

# Outputs
def taskListOutput():
    x = [x1, x2, x3, x4]
    answer = simulatedAnnealing(t_in, x)
    print(" ".join(map(str, answer)), salomon(answer))

def myOutput():
    x = [x1, x2, x3, x4]
    print("Timeout Set to:", t_in)
    print("Analysing: Salomon")
    print("______")
    print("Start_ing X's: [", x1, "|", x2, "|", x3, "|", x4, "]")
    print("Result:", salomon(x))
    print("Smelt_ing the answer...")
    answer = simulatedAnnealing(t_in, x)
    print("______")
    print("Output X:", answer)
    print("Result:", salomon(answer))

# Standard Input
t_in, x1, x2, x3, x4 = list(map(float, input().split()))

# Preparing stuff based on stdin
# print("Inputs: ", t_in, x1, x2, x3, x4)
# myOutput()
taskListOutput()
