import itertools
import random

"""
TODO:
    
"""

class Population():
    def __init__(self):
        self._chromosomes = None
        self._mutation_chance = 0.2
        self._crossover_chance = 1
        self._fitness_function = lambda x: 0
        self._chromosome_length = 0
        self._break_condition = "generation"
        self._break_value = 1000
        self._generation_count = 0

        self._selection_method = "cutoff"
        self._crossover_method = "1_point"
        self._selection_methods = {
            "cutoff": self._cutoff_selection,
            "roulette": self._roulette_selection,
        }
        self._crossover_methods = {
            "1_point": self._random_single_point_crossover,
            "2_point": self._random_two_point_crossover,
            "fixed_common": self._fixed_common_feature_crossover,
        }
        self._break_conditions = {
            "generation": {"func": lambda: self._generation_count >= self._break_value,
                           "var": lambda: self._generation_count},
            "fitness": {"func": lambda: self._get_fittest_chromosome()[1] >= self._break_value,
                        "var": lambda: self._get_fittest_chromosome()[1]},
        }

    def _cutoff_selection(self, num_to_select=2):
        """Return x number of chromosomes from current population, using cutoff selection"""
        prev_generation_size = len(self.chromosomes)
        cutoff = prev_generation_size//2
        prev_fitnesses = self.get_chromosomes_fitness()
        prev_sorted_by_fitness = sorted(prev_fitnesses, key=lambda x: x[1])
        new_generation = [x[0] for x in prev_sorted_by_fitness[cutoff::]]
        for c in range(0, num_to_select):
            yield random.choice(new_generation)

    def _roulette_selection(self, num_to_select=2):
        """Return x number of chromosomes from current population, using roulette selection"""
        prev_fitnesses = self.get_chromosomes_fitness()
        prev_sorted_by_fitness = [x[0] for x in sorted(prev_fitnesses, key=lambda x: x[1])]
        total_fitness = sum(x[1] for x in prev_fitnesses)
        p_values = []
        q_values = []

        for x in prev_sorted_by_fitness:
            f = self.get_fitness(x)
            px = f/total_fitness
            p_values.append(px)

        cum_p = 0
        for index, p  in enumerate(p_values):
            cum_p += p_values[index]
            qx = cum_p
            q_values.append(qx)

        for c in range(0, num_to_select):
            r = random.random()
            for index, q in enumerate(q_values):
                if index == 0:
                    if r <= q:
                        yield prev_sorted_by_fitness[index]
                else:
                    if (r <= q and r > q_values[index-1]):
                        yield prev_sorted_by_fitness[index]

    def get_fitness(self, chromosome):
        """Get the fitness of a given chromosome based on the population fitness function"""
        f = self.fitness_function(chromosome) 
        if f <= 0:
            return 0
        else:
            return f 

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

    def crossover(self, chr1, chr2):
        """Do the selected crossover with the selected crossover chance"""
        if random.random() <= self._crossover_chance:
            for crossover_chr in self._crossover_methods[self._crossover_method](chr1, chr2):
                yield crossover_chr
        else:
            yield chr1
            yield chr2

    def _random_single_point_crossover(self, chr1, chr2):
        """Yield 2 offspring of 2 parent chromosomes using crossover operator with a random crossover point"""
        return [crossed_chr for crossed_chr in self._single_point_crossover(chr1, chr2, random.randrange(0, len(chr1)))]

    def _single_point_crossover(self, chr1, chr2, crossover_point):
        """Yield 2 offspring of 2 parent chromosomes using crossover operator"""
        yield chr1[:crossover_point] + chr2[crossover_point::]
        yield chr2[:crossover_point] + chr1[crossover_point::]

    def _random_two_point_crossover(self, chr1, chr2):
        rand_index_a = random.randrange(0, len(chr1))
        rand_index_b = random.randrange(0, len(chr1))
        crossover_a = min(rand_index_a, rand_index_b)
        crossover_b = max(rand_index_a, rand_index_b)
        return [crossed_chr for crossed_chr in self._two_point_crossover(chr1, chr2, crossover_a, crossover_b)]

    def _two_point_crossover(self, chr1, chr2, crossover_1, crossover_2):
        keep_chr1_s = chr1[:crossover_1]
        chr1_swap = chr1[crossover_1:crossover_2]
        keep_chr1_e = chr1[crossover_2::]

        keep_chr2_s = chr2[:crossover_1]
        chr2_swap = chr2[crossover_1:crossover_2]
        keep_chr2_e = chr2[crossover_2::]
        
        chr3 = keep_chr1_s + chr2_swap + keep_chr1_e
        chr4 = keep_chr2_s + chr1_swap + keep_chr2_e

        yield chr3
        yield chr4

    def _fixed_common_feature_crossover(self, chr1, chr2):
        chr3 = []
        chr4 = []
        for c1, c2 in zip(chr1, chr2):
            if c1 == c2:
                chr3.append(c1)
                chr4.append(c1)
            else:
                chr3.append(random.choice([0,1]))
                chr4.append(random.choice([0,1]))
        yield chr3
        yield chr4

    def _mutate(self, chromosome):
        """Flip a random bit of a chromosome with a given probability"""
        if random.random() <= self.mutation_chance:
            flip_index = random.randrange(0, len(chromosome))
            chromosome[flip_index] = (chromosome[flip_index] + 1) % 2
        return chromosome

    def _has_reached_break_generation(self, echo=False):
        """Check if the current generation fulfils a stopping criteria"""
        if echo:
            print("{name}\t{current_value} / {break_value}".format(name=self._break_condition,
                                                                   current_value=self._break_conditions[self._break_condition]["var"](),
                                                                   break_value=self._break_value),
                                                                   end="\r")

        return self._break_conditions[self._break_condition]["func"]()


    def next_generation(self):
        """Generate a new population from the current one and replaces it."""
        prev_generation_size = len(self.chromosomes)
        new_generation = []

        while len(new_generation) < prev_generation_size:
            #Select 2 chromosomes from current generation:
            chr1, chr2 = self._selection_methods[self._selection_method](2)
            #Crossover these chromosomes (using a set chance):
            chr3, chr4 = self.crossover(chr1, chr2)
            new_generation.append(chr3)
            new_generation.append(chr4)
        #Mutate the new population with a given chance:
        new_population = [self._mutate(chromosome) for chromosome in new_generation]

        self.chromosomes = new_population #Update the population

    def simulate(self, echo=True, plot=True):
        """Simulate a given number of generations and return the final population"""
        max_fitnesses = []
        avg_fitnesses = []
        self._generation_count = 0
        while(not self._has_reached_break_generation(echo=echo)):
            self._generation_count += 1
            self.next_generation()

            if plot:
                max_fitnesses.append(self.fittest_chromosome[1])
                avg_fitnesses.append(self.average_fitness)

        if echo:
            print("After {number_of_generations} generations:".format(number_of_generations=self._generation_count))
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

        if plot:
            return [max_fitnesses, avg_fitnesses]

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
        self._set_chromosome_lenth(len(self._chromosomes[0]))

    def _get_chromosomes(self):
        return self._chromosomes
     
    def _set_fitness_function(self, fitness_function):
        self._fitness_function = fitness_function

    def _get_fitness_function(self):
        return self._fitness_function

    def _get_fittest_chromosome(self):
        """Get the fittest chromosome of a population. Returns tup(chromosome, score)"""
        return self.get_chromosomes_fitness()[0]

    def _get_crossover_method(self):
        return self._crossover_method

    def _get_selection_method(self):
        return self._selection_method

    def _set_crossover_method(self, new_method):
        if new_method in self._crossover_methods:
            self._crossover_method = new_method
        else:
            raise TypeError("Crossover method is not recognised.\n\tMust be in {}".format(list(self._crossover_methods.keys())))

    def _set_selection_method(self, new_method):
        if new_method in self._selection_methods:
            self._selection_method = new_method
        else:
            raise TypeError("Selection method is not recognised.\n\tMust be in {}".format(list(self._selection_methods.keys())))

    def set_break_condition(self, condition_name, condition_value):
        if condition_name in self._break_conditions:
            #self._break_conditions[condition_name]["var"] = condition_value
            self._break_value = condition_value
            self._break_condition = condition_name
        else:
            raise KeyError("Invalid condition name.\n\tMust be in {}".format(list(self._break_conditions.keys())))

    chromosome_lenth = property(_get_chromosome_length, _set_chromosome_lenth)
    average_fitness = property(_get_average_fitness, None)
    mutation_chance = property(_get_mutation_chance, _set_mutation_chance)
    crossover_chance = property(_get_crossover_chance, _set_crossover_chance)
    chromosomes = property(_get_chromosomes, _set_chromosomes)
    fitness_function = property(_get_fitness_function, _set_fitness_function)
    fittest_chromosome = property(_get_fittest_chromosome)
    crossover_method = property(_get_crossover_method, _set_crossover_method)
    selection_method = property(_get_selection_method, _set_selection_method)
