from Genetic import Population

class Problems():
    def __init__(self):
        pass

    def oddsy_evensy(self, chromosome):
        s = 0
        for c, i in enumerate(chromosome):
            if c % 2 == 0:
                s += c * i
            else:
                s -= c * i
        return s 

    def summer(self, chromosome):
        sum = 0
        for i in chromosome:
            sum += i
        return sum

    def weird_oddsy_evensy(self, chromosome):
        s = 0
        for c, i in enumerate(chromosome):
            if c % 2 == 0:
                s += c * i
            elif c % 3 == 0:
                s -= c * i * i
            elif c % 5 == 0:
                s = s * c * i
            elif c % 7 == 0:
                s = s//2
            elif c % 9 == 1:
                s += c*2
            else:
                s -= c 
        return s 



def main():
    problems = Problems()
    pop = Population()

    #pop.set_chromosomes(["00110101", "01010101"])
    #pop.set_chromosomes(pop.all_possibilities(16))
    pop.set_chromosomes(pop.generate_random_sample(4, 100))

    pop.set_fitness_function(problems.summer)

    #print(pop.chromosomes)
    #print(pop.get_chromosomes_fitness()[0])

    #pop.next_generation(0.2)

    #print(pop.chromosomes)
    #print(pop.get_chromosomes_fitness()[0])

    pop.simulate(1000, mutation_chance=0.1)

if __name__ == "__main__":
    main()