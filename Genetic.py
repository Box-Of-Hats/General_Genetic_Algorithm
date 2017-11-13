import itertools
import random

class Population():
    def __init__(self):
        self.fitness_function = lambda x: None
        self.chromosomes = None

    def set_chromosomes(self, chromosome_list):
        """Set the population chromosome list to be another list"""
        self.chromosomes = [[int(chr) for chr in chromosome] for chromosome in chromosome_list]
        
    def set_fitness_function(self, fitness_function):
        self.fitness_function = fitness_function

    def get_fitness(self, chromosome):
        return self.fitness_function(chromosome)

    def get_chromosomes_fitness(self):
        """Return a list of chromosome, fitness tuples, sorted in descending order of fitness"""
        return sorted([(chr, self.get_fitness(chr)) for chr in self.chromosomes], key=lambda x: x[1])[::-1]

    def get_fittest(self):
        return self.get_chromosomes_fitness()[0]

    def generate_all_possibilities(self, chromosome_length):
        """Return a list of all possible chromosomes of a given length"""
        return ["".join(seq) for seq in itertools.product("01", repeat=chromosome_length)]

    def generate_random_sample(self, number_of_samples, chromosome_length):
        """Generate a random sample of chromosomes of a given length"""
        bit_choices = [0]*chromosome_length + [1]*chromosome_length
        for s in range(0, number_of_samples):
            yield random.sample(bit_choices, chromosome_length)

    def next_generation(self, mutation_chance = 0.2, cutoff_divider=2): #TO-DO: Implement this properly
        """Generate a new population from the current one"""
        prev_generation_size = len(self.chromosomes)
        cutoff = prev_generation_size//cutoff_divider
        new_generation = []
        prev_fitnesses = self.get_chromosomes_fitness()
        prev_sorted_by_fitness = sorted(prev_fitnesses, key=lambda x: x[1])
        new_generation = [x[0] for x in prev_sorted_by_fitness[cutoff::] ]

        while len(new_generation) < prev_generation_size:
            chr1 = new_generation[random.randrange(0, len(new_generation))]
            chr2 = new_generation[random.randrange(0, len(new_generation))]
            chr3, chr4 = self._random_crossover(chr1, chr2)
            new_generation.append(chr3)
            new_generation.append(chr4)

        new_population = [self._mutate(chromosome, mutation_chance) for chromosome in new_generation]

        self.set_chromosomes(new_population) #Update the population

    def _random_crossover(self, chr1, chr2):
        """Yield 2 offspring of 2 parent chromosomes using crossover operator. Using a random crossover point"""
        return [crossed_chr for crossed_chr in self._crossover(chr1, chr2, random.randrange(0, len(chr1)))]
            

    def _crossover(self, chr1, chr2, crossover_point):
        """Yield 2 offspring of 2 parent chromosomes using crossover operator"""
        yield chr1[:crossover_point] + chr2[crossover_point::]
        yield chr2[:crossover_point] + chr1[crossover_point::]

    def _mutate(self, chromosome, chance):
        """Flip a random bit of a chromosome with a given probability"""
        if random.random() <= chance:
            flip_index = random.randrange(0, len(chromosome))
            chromosome[flip_index] = (chromosome[flip_index] + 1) % 2
        return chromosome

    def simulate(self, number_of_generations, mutation_chance=0.2, cutoff_divider=None, echo=True, plot=True):
        """Simulate a given number of generations and return the final population"""
        max_fitnesses = []
        for g in range(0, number_of_generations):
            self.next_generation(mutation_chance=mutation_chance, cutoff_divider=cutoff_divider)
            max_fitnesses.append(self.get_chromosomes_fitness()[0][1])

        if echo:
            print("Max fitness after {number_of_generations} generations: {maxes}".format(maxes=self.get_fittest()[1], number_of_generations=number_of_generations))
            print("Current Fittest: {fittest}".format(fittest=self.get_fittest()[0]))

        if plot:
            #Plot the results in a nice graph
            import matplotlib.pyplot as plt
            plotted_results = plt.plot(max_fitnesses)
            plt.setp(plotted_results, linewidth=4, color='c')
            plt.rcParams.update({'font.size': 18})
            plt.ylabel("Fitness")
            plt.xlabel("Generation")
            plt.show()
        return max_fitnesses
    

def main():
    pop = Population()
    
if __name__ == "__main__":
    main()
