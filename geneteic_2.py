import random
import string
import numpy as np

PASSWORD = "Unicorn"
POPULATION_SIZE = 1000


def generate_initial_population(password_length, population_size):
    """
    Function takes as input length of the guess to generate, and quantity
    of them. Returns a list of randomly generated guesses
    """
    population = []
    letters = string.ascii_letters + string.digits + " "

    for i in range(population_size):
        guess = ""
        for i in range(password_length):
            guess += random.choice(letters)

        population.append(guess)

    return population


def match_score(password, guess):  # +
    """
    Function takes two strings, and counts how many characters matched.
    Returns an integer
    """
    score = 0
    for i in range(len(password)):
        if password[i] == guess[i]:
            score += 1
    return score


def score_for_population(password, population):  # +
    """
    Functions uses match_score() and iterates through whole population
    returns list of integers representing score of every population member
    """
    scores = []
    for i in population:
        scores.append(match_score(password, i))
    return scores


def choose_parents(population, scores):
    """
    Function takes list of population members and list of their corresponding
    scores, and returns 2 members with the highest scores
    """
    father_index = np.array(scores).argmax()
    father = population[father_index]

    # we are removing the biggest elements from list,
    # than doing the same thing above to find second biggest.
    population.remove(father)
    scores.remove(scores[father_index])

    mother_index = np.array(scores).argmax()
    mother = population[mother_index]

    return [father, mother]


def generate_new_member(parent, parent_score):
    """
    Takes as input string which we will, pick letters from(parent),
    and quantity of letters to pick(parent_score)
    Returns a newly generated string"""

    new_guess = ""

    letters = string.ascii_letters + string.digits + " "
    random_indexes = random.sample(range(len(parent)), parent_score)

    for i in range(len(parent)):
        if i in random_indexes:
            new_guess += parent[i]
        else:
            new_guess += random.choice(letters)

    return new_guess


def generate_new_population(father, mother):
    """
    Takes as input parents and reproduces new population from them, using
    generate_new_member() function with alternatively father and mother.
    Returns list with new population members
    """
    population = []
    father_score = match_score(PASSWORD, father)
    mother_score = match_score(PASSWORD, mother)

    for i in range(POPULATION_SIZE):
        if i % 2 == 0:
            new_member = generate_new_member(father, father_score)
        else:
            new_member = generate_new_member(mother, mother_score)
        population.append(new_member)
    return population


def main():
    """
    better way of doing would be using a class.
    """
    generation_number = 0

    initial_population = generate_initial_population(
        len(PASSWORD), POPULATION_SIZE)
    scores = score_for_population(PASSWORD, initial_population)

    father, mother = choose_parents(initial_population, scores)

    for i in range(10_000):
        generation_number += 1
        new_population = generate_new_population(father, mother)
        new_scores = score_for_population(PASSWORD, new_population)

        father, mother = choose_parents(new_population, new_scores)
        father_score = match_score(father, PASSWORD)
        mother_score = match_score(mother, PASSWORD)

        if max(father_score, mother_score) == len(PASSWORD):
            print(generation_number, father, mother)
            print("TOOK {} generations to finish".format(generation_number))
            break

        print(generation_number, father, mother, father_score)

    return generation_number


if __name__ == "__main__":
    main()
