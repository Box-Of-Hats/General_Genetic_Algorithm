from Genetic import Population

class ExampleProblems():
    """Object containing some example problems for the genetic algorithm."""
    def __init__(self):
        pass

    def oddsy_evensy(self, chromosome):
        """
        A problem where we want a string to contain alternating 0s and 1s.
        e.g 10101010101...
        """
        fitness = 0
        for c, i in enumerate(chromosome):
            if c % 2 == 0:
                fitness += c * i
            else:
                fitness -= c * i
        return fitness

    def summer(self, chromosome):
        """
        A problem where we want to have a string containing as many 1s as
        possible. This function calculates fitness but summing the bits
        of a chromosome.
        """
        fitness = 0
        for i in chromosome:
            fitness += i
        return fitness

    def weird_oddsy_evensy(self, chromosome):
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
        a,b,c,d,e,f,g,h = [bool(i) for i in chromosome]

        #A
        if (g and not d):
            score += 400
        elif (not d):
            score += 100
        #B
        if (not d and not a):
            score += 800
        #C
        if (not b):
            score += 600
        #D
        if (not g and h):
            score += 200
        elif (not g):
            score += 150
        #F
        if (not h):
            score += 400
        #G
        if (d):
            score += 220
        else:
            score += 80
        #H
        if (not f and not a):
            score += 380

        return score


def main():
    #An object containing some sample problems that
    # the genetic algorithm can attempt to solve.
    problems = ExampleProblems()

    #Initialise the Population object
    pop = Population()

    #Generate a random sample of 10 chromosomes to be our starting population,
    # each with a length of 100 bits.
    pop.chromosomes = pop.generate_random_sample(10, 100)

    #Define our fitness function. This will be what we're trying to maximise and will
    # be specific to any problem that we are trying to solve.
    pop.fitness_function = problems.oddsy_evensy

    #Some basic options for our simulation:

    #The number of generations our simulation should go through
    number_of_generations = 1000
    #When we select the fittest candidates during the next generation creation, this is the fraction
    # of the top amount we want to keep. E.g cutoff_divider of 4 means that we keep the top 1/4
    # of the population
    pop.cutoff_divider = 2
    #The chance for a random bit to mutate when generating new children.
    pop.mutation_chance = 0.1
    #The chance that a crossover will take place between 2 random chromosomes
    pop.crossover_chance = 1

    #Carry out the simulation
    pop.simulate(number_of_generations=number_of_generations, echo=True, plot=True)


if __name__ == "__main__":
    main()
