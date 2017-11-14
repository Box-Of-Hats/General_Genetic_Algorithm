import itertools
import random

class Population():
    def __init__(self):
        self._chromosomes = None
        self._mutation_chance = 0.2
        self._crossover_chance = 1
        self._fitness_function = lambda x: 0
        self._chromosome_length = 0
        self._cutoff_divider = 2

    def get_fitness(self, chromosome):
        """Get the fitness of a given chromosome based on the population fitness function"""
        return self.fitness_function(chromosome)

    def get_chromosomes_fitness(self):
        """Return a list of chromosome, fitness tuples, sorted in descending order of fitness"""
        return sorted([(chr, self.get_fitness(chr)) for chr in self.chromosomes], key=lambda x: x[1])[::-1]

    def generate_all_possibilities(self, chromosome_length):
        """Return a list of all possible chromosomes of a given length"""
        return ["".join(seq) for seq in itertools.product("01", repeat=chromosome_length)]

    def generate_random_sample(self, number_of_samples, chromosome_length):
        """Generate a random sample of chromosomes of a given length"""
        bit_choices = [0]*chromosome_length + [1]*chromosome_length
        for sample in range(0, number_of_samples):
            yield random.sample(bit_choices, chromosome_length)

    def next_generation(self):
        """Generate a new population from the current one and replaces it."""
        prev_generation_size = len(self.chromosomes)
        cutoff = prev_generation_size//self._cutoff_divider
        new_generation = []
        prev_fitnesses = self.get_chromosomes_fitness()
        prev_sorted_by_fitness = sorted(prev_fitnesses, key=lambda x: x[1])
        new_generation = [x[0] for x in prev_sorted_by_fitness[cutoff::]]

        while len(new_generation) < prev_generation_size:
            chr1 = new_generation[random.randrange(0, len(new_generation))]
            chr2 = new_generation[random.randrange(0, len(new_generation))]
            chr3, chr4 = self._random_crossover(chr1, chr2)
            new_generation.append(chr3)
            new_generation.append(chr4)

        new_population = [self._mutate(chromosome) for chromosome in new_generation]

        self.chromosomes = new_population #Update the population

    def _random_crossover(self, chr1, chr2):
        """Yield 2 offspring of 2 parent chromosomes using crossover operator with a random crossover point"""
        return [crossed_chr for crossed_chr in self._crossover(chr1, chr2, random.randrange(0, len(chr1)))]

    def _crossover(self, chr1, chr2, crossover_point):
        """Yield 2 offspring of 2 parent chromosomes using crossover operator"""
        if random.random() <= self._crossover_chance:
            yield chr1[:crossover_point] + chr2[crossover_point::]
            yield chr2[:crossover_point] + chr1[crossover_point::]
        else:
            yield chr1
            yield chr2

    def _mutate(self, chromosome):
        """Flip a random bit of a chromosome with a given probability"""
        if random.random() <= self.mutation_chance:
            flip_index = random.randrange(0, len(chromosome))
            chromosome[flip_index] = (chromosome[flip_index] + 1) % 2
        return chromosome

    def simulate(self, number_of_generations, echo=True, plot=True):
        """Simulate a given number of generations and return the final population"""
        max_fitnesses = []
        avg_fitnesses = []
        gen_step = number_of_generations//100

        for generation_no in range(0, number_of_generations):
            self.next_generation()

            if (echo and generation_no % gen_step == 0):
                print("{}\t/\t{}".format(generation_no, number_of_generations), end="\r")

            if plot:
                max_fitnesses.append(self.fittest_chromosome[1])
                avg_fitnesses.append(self.average_fitness)

        if echo:
            print("After {number_of_generations} generations:".format(number_of_generations=number_of_generations))
            print("Current Average Fitness: {avg_fitness}".format(avg_fitness=self.average_fitness))
            print("Current Max Fitness: {maxes}".format(maxes=self.fittest_chromosome[1]))
            print("Current Fittest: {fittest}".format(fittest=self.fittest_chromosome[0]))

        if plot:
            #Plot the results in a nice graph
            import matplotlib.pyplot as plt
            max_fitness_plot = plt.plot(max_fitnesses)
            avg_fitness_plot = plt.plot(avg_fitnesses)
            plt.setp(max_fitness_plot, linewidth=3, color='c', label="Max Fitness")
            plt.setp(avg_fitness_plot, linewidth=3, color='b', label="Avg Fitness")
            plt.legend(loc=0)
            plt.rcParams.update({'font.size': 18})
            plt.ylabel("Fitness")
            plt.xlabel("Generation")
            plt.show()
        #return max_fitnesses

    """
        Getters and setters:
    """

    def _set_mutation_chance(self, chance):
        if chance > 1 or chance < 0:
            raise ValueError("Mutation chance must be between 0 - 1.")
        else:
            self._mutation_chance = chance
    
    def _get_mutation_chance(self):
        return self._mutation_chance

    def _set_crossover_chance(self, chance):
        if chance > 1 or chance < 0:
            raise ValueError("Crossover chance must be between 0 - 1.")
        else:
            self._crossover_chance = chance
    
    def _get_crossover_chance(self):
        return self._crossover_chance

    def _set_chromosome_lenth(self, length):
        if isinstance(length, int): 
            self._chromosome_length = length
        else:
            raise TypeError("Chromosome length must be int.")

    def _get_chromosome_length(self):
        return self._chromosome_length

    def _get_average_fitness(self):
        return sum([self.get_fitness(chromosome) for chromosome in self.chromosomes]) / len(self.chromosomes)

    def _set_chromosomes(self, chromosome_list):
        self._chromosomes = [[int(chr) for chr in chromosome] for chromosome in chromosome_list]
        self._set_chromosome_lenth(len(self._chromosomes))

    def _get_chromosomes(self):
        return self._chromosomes

    def _set_cutoff_divider(self, divider):
        self._cutoff_divider = divider

    def _get_cutoff_divider(self):
        return self._cutoff_divider
        
    def _set_fitness_function(self, fitness_function):
        self._fitness_function = fitness_function

    def _get_fitness_function(self):
        return self._fitness_function

    def _get_fittest_chromosome(self):
        """Get the fittest chromosome of a population. Returns tup(chromosome, score)"""
        return self.get_chromosomes_fitness()[0]

    chromosome_lenth = property(_get_chromosome_length, _set_chromosome_lenth)
    average_fitness = property(_get_average_fitness, None)
    mutation_chance = property(_get_mutation_chance, _set_mutation_chance)
    crossover_chance = property(_get_crossover_chance, _set_crossover_chance)
    chromosomes = property(_get_chromosomes, _set_chromosomes)
    fitness_function = property(_get_fitness_function, _set_fitness_function)
    cutoff_divider = property(_get_cutoff_divider, _set_cutoff_divider)
    fittest_chromosome = property(_get_fittest_chromosome)