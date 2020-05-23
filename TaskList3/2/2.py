import copy
import time
import random
import sys
import math
from collections import Counter

# == DICTIONARY PATH - PLACED IN THE SAME FOLDER AS THIS FILE == 
dictionary = 'dict.txt'

# === Processing Input ===

# Reading Input File
# Out:
#   - [Time, Letters Length, Example Worlds]
#   - [[Letter, Points], (...)]
#   - [WordEx, (...)]
def readInfo(path):
    with open(path, 'r') as f:
        info = []
        letters_scores = []
        words_example = []
        arr = [line.strip('\n').split(' ') for line in f]
        for w in arr:
            if len(w) == 3:
                info.append(int(w[0]))
                info.append(int(w[1]))
                info.append(int(w[2]))
            if len(w) == 2:
                letters_scores.append([w[0], int(w[1])])
            if len(w) == 1:
                words_example.append(w[0])
        return info, letters_scores, words_example

# Reading Dictionary
# Out:
#   - [Word, Word, Word, (...)]
def readDict(path):
    with open(path, 'r') as f:
        arr = [line.strip('\n').split(' ') for line in f]
        # words_arr = []
        # for w in arr:
        #     words.append(w[0])
        # return words_arr

        words_dict = {}
        for w in arr:
            words_dict[w[0]] = True
        return words_dict

def getLetterScores(letter_scores):
    scores = {}
    for bucket in letter_scores:
        if bucket[0] not in scores:
            scores[bucket[0]] = bucket[1]
    return scores

path = sys.argv[1]
info, letters_scr, words_example = readInfo(path)
words = readDict(dictionary)
let_scores = getLetterScores(letters_scr)
t_in, letters_len, words_in_len = info[0], info[1], info[2]

# === Assisting Functions ===

ALL_LETTERS = ''.join([buck[0] for buck in letters_scr])

# Check if the word is legit in terms of used letters
def legalWord(word):
    letters = Counter(ALL_LETTERS)
    letters.subtract(Counter(word))
    return all(v >= 0 for v in letters.values())

def availableLetters(word):
    letters = Counter(ALL_LETTERS)
    letters.subtract(Counter(word))
    available_letters = []
    for let in letters:
        if letters[let] > 0:
            available_letters.append(let)
    return available_letters


# Performance boost from ~3050 to ~34000 generations in given time
def isInDict(word):
    try:
        return words[word]
    except:
        return False

# def isInDict(word):
#     return word in words

# Getting score of the word (returns 0 if word is not valid)
def fitness(word):
    score = 0
    if legalWord(word):
        for l in word:
            score += let_scores[l]
        # I'll keep some score for words that meet letter criteria
        # but add penalty if it's not a real world (in dict)
        if isInDict(word) == False:
            score = math.floor(score / 6)
        return score
    else:
        return score

# Parents decide to meet each other and create a new_gen child
def crossover(a, b): 
    break_point = random.randint(0, len(ALL_LETTERS))
    child_one = a[0:break_point] + b[break_point:len(ALL_LETTERS)]
    child_two = b[0:break_point] + a[break_point:len(ALL_LETTERS)]
    return (child_one, child_two)

# Modify the gene (split and paste)
def mutate(word, probability):
    new_word = copy.deepcopy(word)
    for _ in range(0, len(new_word)):
        if random.random() < (probability/30):

            low_cut = random.randint(0, len(word))
            up_cut = random.randint(low_cut, len(word))

            subset_individual = list(new_word[low_cut:up_cut])
            random.shuffle(subset_individual)

            new_word = word[0:low_cut] + ''.join(subset_individual) + word[up_cut:len(ALL_LETTERS)]

        if random.random() < probability:
            low_cut = random.randint(0, len(word))
            up_cut = random.randint(low_cut, len(word)) 

            # print(availableLetters(new_word))
            av_letters = availableLetters(new_word)
            new_letter = ""
            if len(av_letters) != 0:
                new_letter = random.choice(av_letters)

            new_word = word[0:low_cut] + new_letter + word[up_cut:len(ALL_LETTERS)]

    return new_word

# Picking Mate based on their scores
# Reminder: Illegal words are big nums 
def pickMate(scores):

    # Monte Carlo
    normalized_values = [int(v/sum(scores)*100+.5) for v in scores]
    accum = 0
    selection_weights = []
    for w in normalized_values:
        accum += w
        selection_weights.append(accum)

    selection = random.randint(0,selection_weights[-1])
    for i,w in enumerate(selection_weights):
        if selection <= w:
            return i    

# Gets all scores in a array and best word with its score
def scorePopulation(population):
    scores = []

    best = ""
    best_score = 0

    for i in range(0, len(population)):
        current = fitness(population[i])
        scores += [current]

        if current > best_score:
            best = population[i]
            best_score = current

    return scores, best, best_score

# === Genetic Algorithm ===

def geneticAlgorithm(iters=99999999):
    inputPopulation = words_example
    population = inputPopulation   

    # Variables
    number_of_couples = 6
    mutation_chance = 0.9
    keep_best = True
    keep_past = True
    use_motivation = False
    add_noise = True
    mumble_word = True
    motivation_fresh = 5000
    motivation = motivation_fresh

    # Iteration Counter (Generations) and Timer
    gen = 1
    timeout = time.time() + float(t_in)
    timenow = time.time()
    
    # Best Ever is the cost we just found (because nothing started yet)
    print("Population: ", population)
    scores, best_answ, best_score = scorePopulation(population)
    best_answ_ever = best_answ
    best_score_ever = best_score

    while gen <= iters and time.time() < timeout:
        print(f"[Dev] ({gen}) Costs: ({best_score}/{best_score_ever}), Time left: {timeout - time.time()}")

        new_population = []

        scores, best_answ, best_score = scorePopulation(population)
        # print(f"[Dev] ({gen}) Pop: {population}")
        # print(f"[Dev] ({gen}) Scr: {scores}")

        # Update new best score if found
        if best_score > best_score_ever:
            print(f"[Dev] ({gen}) New best! ({best_score_ever} -> {best_score}) Time: {time.time() - timenow} ({best_answ_ever} -> {best_answ}), Timeleft: {timeout - time.time()}")
            best_score_ever = best_score
            best_answ_ever = best_answ
            motivation = motivation_fresh  

        # Start breeding new population
        # Breed based on relative score (better individuals are more likelly to breed with eac other)
        for _ in range(0, number_of_couples):
            new_1, new_2 = crossover(population[pickMate(scores)], population[pickMate(scores)])
            new_population += [new_1, new_2]

        # Mutate a bit the gene pool
        for i in range(0, len(new_population)):
            new_population[i] = mutate(new_population[i], mutation_chance)

        # Add Random Word from dict
        if add_noise:
            new_population.pop(0)
            if type(words) == list:
                new_word = random.choice(words)
            elif type(words) == dict:
                new_word = random.choice(list(words.keys()))
            new_population += [new_word]

        # Create random word
        if mumble_word:
            new_population.pop(0)
            new_word = ""
            for _ in range(len(ALL_LETTERS)):
                if random.random() < 0.8:

                    av_letters = availableLetters(new_word)
                    if len(av_letters) != 0:
                        new_word += random.choice(av_letters)

            new_population += [new_word]

        # Remember input ancestor
        if keep_past:
            new_population.pop(0)
            ancestor = random.choice(inputPopulation)
            new_population += [ancestor]


        # Keep the best route in the population
        if keep_best:
            new_population.pop(0)
            new_population += [best_answ_ever]

        # New Population replaces the current one
        population = copy.deepcopy(new_population)
        gen += 1

        # Not used anymore as it finds global optimum too fast :3
        if use_motivation:
            mutation_chance = random.choice([0.1, 0.3, 0.5, 0.7, 0.9])
            motivation -= 1

    return best_score_ever, best_answ_ever

# === Main ===

def main():
    # print("[Dev] Info: ", info)
    # print("[Dev] Letters: ", ALL_LETTERS)
    # print("[Dev] Letter Scores: ", let_scores)
    # print("[Dev] Words Example: ", words_example)

    answ = geneticAlgorithm()
    print(answ[0])
    print(answ[1], file=sys.stderr)

if __name__ == "__main__":
    main()
