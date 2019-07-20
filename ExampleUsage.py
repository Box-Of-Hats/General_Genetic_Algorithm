from Genetic import Population, SelectionMethod, CrossoverMethod, BreakCondition
import math
import random


class ExampleProblems():
    """Object containing some example problems for the genetic algorithm."""

    def __init__(self, number_of_items=500):
        self.knapsack_items = self._randomise_knapsack_items(number_of_items)
        self.knapsack_allowance = number_of_items * 30

        self.problems = {"none": lambda c: 1,
                         "knapsack": lambda c: self.knapsack(c),
                         "1010": lambda c: self.alternating_ones_and_zeroes(c),
                         "1111": lambda c: self.list_of_ones(c),
                         "weird_factors": lambda c: self.weird_factors(c),
                         "shops": lambda c: self.shop_problem(c),
                         "furthest_cannonball": lambda c: self.furthest_cannonball(c),


                         }

    def _get_problems(self):
        return [problem_name for problem_name in self.problems]

    problem_names = property(_get_problems)

    def _randomise_knapsack_items(self, number_of_values=10):
        """Generate items for knapsack problem with random values/weights"""
        items = []
        # print("-\tValue\tWeight")
        for i in range(0, number_of_values):
            value = random.randrange(0, 100)
            weight = random.randrange(0, 100)
            items.append({"value": value, "weight": weight})
            #print("Item {}:\t{}\t{}".format(i, value, weight))
        return items

    def alternating_ones_and_zeroes(self, chromosome):
        """
        A problem where we want a string to contain alternating 0s and 1s.
        e.g 10101010101...
        """
        fitness = 0
        for index, c in enumerate(chromosome):
            if index % 2 == 0:
                fitness -= c
            else:
                fitness += c
        return fitness

    def list_of_ones(self, chromosome):
        """
        A problem where we want to have a string containing as many 1s as
        possible. This function calculates fitness but summing the bits
        of a chromosome.
        """
        fitness = 0
        for i in chromosome:
            fitness += i
        return fitness

    def weird_factors(self, chromosome):
        """
        A somewhat random problem.
        An example of how problems can be more complex and non-trivial.
        """
        fitness = 0
        for c, i in enumerate(chromosome):
            if c % 2 == 0:
                fitness += c * i
            elif c % 3 == 0:
                fitness -= c * i * i
            elif c % 5 == 0:
                fitness = fitness * c * i
            elif c % 7 == 0:
                fitness = fitness//2
            elif c % 9 == 1:
                fitness += c*2
            else:
                fitness -= c
        return fitness

    def shop_problem(self, chromosome):
        """
        Chromosome length must be 8
        A fictional example of 8 shops, each with different rules on
        thier profits, based on other shops being open.

        shop | profit | rules
        A       100     no D
        B       800     no D, no A
        C       600     no B
        D       150     no G, 200 if H is also open
        E       180     260 if G is also open
        F       400     no H
        G       80      220 if D
        H       380     no F, no A
        """
        score = 0
        chromosome = chromosome[0:8]
        a, b, c, d, e, f, g, h = [bool(i) for i in chromosome]

        # A
        if (g and not d):
            score += 400
        elif (not d):
            score += 100
        # B
        if (not d and not a):
            score += 800
        # C
        if (not b):
            score += 600
        # D
        if (not g and h):
            score += 200
        elif (not g):
            score += 150
        # F
        if (not h):
            score += 400
        # G
        if (d):
            score += 220
        else:
            score += 80
        # H
        if (not f and not a):
            score += 380

        return score

    def knapsack(self, chromosome):
        weight = 0
        value = 0
        for item, pickup in zip(self.knapsack_items, chromosome):
            value += item["value"] * pickup
            weight += item["weight"] * pickup
            if weight > self.knapsack_allowance:
                return 0
        return value

    def furthest_cannonball(self, chromosome):
        """
        Try to launch a cannon ball as far as possible.
        Minimum chromosome length of 8.
        First 7 bits are a binary value, which is taken as the angle of launch. (range 0-127 degrees)
        All following bits are taken as a binary value, which is the velocity of the launch

        With these values, expected best is: [0,1,0,1,1,0,1, | 1*]
         which represents a 45 degree launch at max velocity.

        """
        g = 9.8  # gravity

        angle = 0

        angle = int("".join([str(x) for x in chromosome[0:7]]), 2)
        velocity = int("".join([str(x) for x in chromosome[7::]]), 2)
        #print("Angle = {}".format(angle))
        #print("Velocity = {}".format(velocity))

        angle = math.radians(angle)

        distance_launched = (velocity*velocity * math.sin(2 * angle)) / g
        #print("Distance = {}".format(distance_launched))
        if distance_launched <= 0:
            return 0
        else:
            return distance_launched


def main():
    # An object containing some sample problems that
    # the genetic algorithm can attempt to solve.
    problems = ExampleProblems()

    # Initialise the Population object
    pop = Population()

    # Generate a random sample of x chromosomes to be our starting population,
    # each with a length of y bits.
    pop.chromosomes = pop.generate_random_sample(50, 500)

    # Define our fitness function. This will be what we're trying to maximise and will
    # be specific to any problem that we are trying to solve.
    pop.fitness_function = problems.knapsack

    # Some basic options for our simulation:

    # The chance for a random bit to mutate when generating new children.
    pop.mutation_chance = 0.1
    # The chance that a crossover will take place between 2 random chromosomes
    pop.crossover_chance = 0.8
    # Selection method to use for crossover
    pop.selection_method = SelectionMethod.TOURNAMENT
    # Crossover method to use for crossover
    pop.crossover_method = CrossoverMethod.TWO_POINT
    # Choose a break condition:
    pop.set_break_condition(BreakCondition.GENERATION, 100)

    # Carry out the simulation
    pop.simulate(echo=True, plot=True)


if __name__ == "__main__":
    main()
