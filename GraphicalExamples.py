from Genetic import Population
from ExampleUsage import ExampleProblems
from threading import Thread
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use("TkAgg")

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("GA Examples")
        self.problems = ExampleProblems()
        self.chosen_problem = StringVar(self.master)
        self.chosen_problem.set("none")

        self.options_container = Frame()
        self.options_container.grid(row=0, column=0, sticky='nw', padx=5, pady=5)
        self.options_container.grid_columnconfigure(0, weight=1)

        Label(self.options_container, text="Problem").grid(row=0, column=0)
        self.problems_dropdown = OptionMenu(self.options_container, self.chosen_problem, *list(x.title() for x in sorted(self.problems.problem_names)))
        self.problems_dropdown.grid(row=0, column=1)

        Label(self.options_container, text="Population Size").grid(row=1, column=0)
        self.pop_size_entry = Entry(self.options_container)
        self.pop_size_entry.grid(row=1, column=1)
        self.pop_size_entry.insert(END, 10)

        Label(self.options_container, text="Chr length").grid(row=2, column=0)
        self.chromosome_length_entry = Entry(self.options_container )
        self.chromosome_length_entry.grid(row=2, column=1)
        self.chromosome_length_entry.insert(END, 100)

        Label(self.options_container, text="Generations").grid(row=3, column=0)
        self.generation_entry = Entry(self.options_container)
        self.generation_entry.grid(row=3, column=1)
        self.generation_entry.insert(END, 200)

        self.calc = Button(self.options_container, command=self._threaded_single_graph, text="Show Graphs")
        self.calc.grid(row=0, column=10)

        self.loading_label = Label(self.options_container, text="")
        self.loading_label.grid(row=0, column=11)

        self._threaded_single_graph()

    def _threaded_single_graph(self):
        self.calc.config(state='disabled')
        t = Thread(target=self.single_graph, daemon=True)
        t.start()

    def single_graph(self):
        pop = Population()
        start_sample = list(pop.generate_random_sample(int(self.pop_size_entry.get()), int(self.chromosome_length_entry.get())))

        f = Figure(figsize=(10,5), dpi=100)
        a = f.add_subplot(1, 1, 1)
        a.set_xlabel('Generation')
        a.set_ylabel('Max Fitness')
        # Shrink current axis by 40% to fit legend on right side
        box = a.get_position()
        a.set_position([box.x0, box.y0, box.width * 0.6, box.height])

        total_methods = len(pop.selection_methods) * len(pop.crossover_methods)
        current_method_count = 0
        for sm in pop.selection_methods:
            for cm in pop.crossover_methods:
                self._update_loading_label("{:.0f}%".format(current_method_count/total_methods*100))
                pop = Population()
                pop.chromosomes = start_sample
                pop.fitness_function = self.problems.problems[self.chosen_problem.get().lower()]
                pop.selection_method = sm
                pop.crossover_method = cm
                pop.set_break_condition("generation", int(self.generation_entry.get()))
                pmax, pavg =pop.simulate(plot=False, echo=True)

                a.plot(pmax, linewidth=2, label="{}, {} [{:.0f}]".format(sm, cm, pop.fittest_chromosome[1]))

                current_method_count += 1
                

        a.set_title("{}".format(self.chosen_problem.get()))
        handles, labels = a.get_legend_handles_labels()
        # sort both labels and handles by labels
        labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[1].get_xydata()[-1][1])[::-1])

        a.legend(handles, labels, loc='center left', bbox_to_anchor=(1, 0.5))
        a.set_xlim(xmin=0)

        for h in handles:
            a.plot([0, 1], [h.get_xydata()[-1][1]]*2, h.get_color(), linewidth=5,)
        canvas = FigureCanvasTkAgg(f, self.master)
        canvas.show()
        canvas.get_tk_widget().grid(row=10, column=0)

        #All finished:
        self.calc.config(state='normal')
        self._update_loading_label("")

    def _update_loading_label(self, value):
        self.loading_label.config(text=str(value))


class GenerationStepThroughWindow(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("GA Stepthrough")
        self.problems = ExampleProblems()

        self.population = Population()

        self.selection_method = StringVar(self.master)
        self.selection_method.set(self.population.selection_methods[0])

        self.crossover_method = StringVar(self.master)
        self.crossover_method.set(self.population.crossover_methods[0])

        self.chosen_problem = StringVar(self.master)
        self.chosen_problem.set("none")

        self.options_container = Frame()
        self.options_container.grid(row=0, column=0, sticky='nw', padx=5, pady=5)
        self.options_container.grid_columnconfigure(0, weight=1)

        self.fitness_graph_container = Frame(self.master)
        self.fitness_graph_container.grid(row=1, column=0)

        self.chromosome_graph_container = Frame(self.master)
        self.chromosome_graph_container.grid(row=2, column=0)

        Label(self.options_container, text="Problem").grid(row=0, column=0)
        self.problems_dropdown = OptionMenu(self.options_container, self.chosen_problem, *list(x.title() for x in sorted(self.problems.problem_names)))
        self.problems_dropdown.grid(row=0, column=1)

        Label(self.options_container, text="Population Size").grid(row=1, column=0)
        self.pop_size_entry = Entry(self.options_container)
        self.pop_size_entry.grid(row=1, column=1)
        self.pop_size_entry.insert(END, 10)

        Label(self.options_container, text="Chr length").grid(row=2, column=0)
        self.chromosome_length_entry = Entry(self.options_container )
        self.chromosome_length_entry.grid(row=2, column=1)
        self.chromosome_length_entry.insert(END, 100)

        Label(self.options_container, text="Selection Method").grid(row=3, column=0)
        selection_method_menu = OptionMenu(self.options_container, self.selection_method, *list(x for x in sorted(self.population.selection_methods)))
        selection_method_menu.grid(row=3, column=1)

        Label(self.options_container, text="Crossover Method").grid(row=4, column=0)
        crossover_method_menu = OptionMenu(self.options_container, self.crossover_method, *list(x for x in sorted(self.population.crossover_methods)))
        crossover_method_menu.grid(row=4, column=1)

        self.new_pop_button = Button(self.options_container, command=self.generate_new_population, text="New Population")
        self.new_pop_button.grid(row=0, column=10)

        self.new_gen_button = Button(self.options_container, command=self.generate_next, text="Next Generation", state='disabled')
        self.new_gen_button.grid(row=0, column=11)

        self.next_10_gen = Button(self.options_container, command= lambda: self.generate_x_generations(10), text="Next 10", state='disabled')
        self.next_10_gen.grid(row=0, column=12)

        self.next_100_gen = Button(self.options_container, command= lambda: self.generate_x_generations(100), text="Next 100", state='disabled')
        self.next_100_gen.grid(row=0, column=13)

        Button(self.options_container, command = self.kill_population, text="kill", bg="brown", state="disabled").grid(row=0, column=14)


    def toggle_input(self, status="disabled", widgets=False, container=False):
        if not widgets:
            widgets = [Button, Entry, OptionMenu]
        if not container:
            container = self.options_container
        for associated_widget in container.winfo_children():
            for t in widgets:
                if isinstance(associated_widget, t):
                    associated_widget.config(state=status)

    def kill_population(self):
        self.population = Population()
        self.toggle_input(status="disabled", widgets=[Button])
        self.toggle_input(status="normal", widgets=[Entry, OptionMenu])
        self.new_pop_button.config(state="normal")

    def generate_new_population(self, threaded=True):
        if threaded:
            t = Thread(target=self.generate_new_population, kwargs={"threaded": False,}, daemon=True)
            t.start()
            return 1
        print("Generating fresh population.")

        self.population = Population()
        self.average_fitnesses = []
        self.max_fitnesses = []
        self.population.fitness_function = self.problems.problems[self.chosen_problem.get().lower()]
        self.population.selection_method = self.selection_method.get()
        self.population.crossover_method = self.crossover_method.get()
        self.population.chromosomes = self.population.generate_random_sample(int(self.pop_size_entry.get()), int(self.chromosome_length_entry.get()))

        self.toggle_input(status="normal")
        self.toggle_input(status="disabled", widgets=[OptionMenu, Entry])

        self.generate_next()

    def generate_next(self, threaded=True):
        if threaded:
            t = Thread(target=self.generate_next, kwargs={"threaded": False,}, daemon=True)
            t.start()
            return 1
        self.toggle_input(status="disabled")

        self.population.next_generation()
        self.average_fitnesses.append(self.population.average_fitness)
        self.max_fitnesses.append(self.population.fittest_chromosome[1])

        self.make_fitness_graph(self.fitness_graph_container)
        self.make_chromosome_graph(self.chromosome_graph_container)

        self.toggle_input("normal", widgets=[Button])

    def generate_x_generations(self, number_of_generations, threaded=True):
        if threaded:
            t = Thread(target=self.generate_x_generations, kwargs={"threaded": False, "number_of_generations": number_of_generations,}, daemon=True)
            t.start()
            return 1

        self.toggle_input("disabled")

        self.population.set_break_condition("generation", number_of_generations)
        s_max, s_avgs = self.population.simulate(echo=True, plot=False)
        self.max_fitnesses = self.max_fitnesses + s_max
        self.average_fitnesses = self.average_fitnesses + s_avgs

        self.make_fitness_graph(self.fitness_graph_container)
        self.make_chromosome_graph(self.chromosome_graph_container)

        self.toggle_input("normal", [Button])

    def make_fitness_graph(self, container, col=0, row=0, threaded=True):
        if threaded:
            t = Thread(target=self.make_fitness_graph, kwargs={"threaded": False, "col": col, "row": row, "container": container,}, daemon=True)
            t.start()
            return 1

        f = Figure(figsize=(10,5), dpi=100)
        a = f.add_subplot(1, 1, 1)
        a.set_xlabel('Generation')
        a.set_ylabel('Fitness')

        a.plot(self.max_fitnesses, linewidth=2, label="Max Fitness", marker="o")
        a.plot(self.average_fitnesses, linewidth=2, label="Avg Fitness", marker="o")
                

        a.set_title("{}".format(self.chosen_problem.get()))

        a.legend(loc=0)
        a.set_xlim(xmin=0)

        canvas = FigureCanvasTkAgg(f, container)
        canvas.show()
        canvas.get_tk_widget().grid(row=row, column=col)

        self.toggle_input(status="normal", widgets=[Button])

    def make_chromosome_graph(self, container, col=0, row=0, threaded=True):
        if threaded:
            t = Thread(target=self.make_chromosome_graph, kwargs={"threaded": False, "container": container, "col": col, "row": row,}, daemon=True)
            t.start()
            return 1

        f = Figure(figsize=(10, 1), dpi=100)
        a = f.add_subplot(1, 1, 1)

        a.plot(self.population.fittest_chromosome[0], linewidth=1, label="Fittest Chromosome", marker="o")
        a.plot([1] * len(self.population.fittest_chromosome[0]), "--", color='0.4', linewidth=1)
        a.plot([0] * len(self.population.fittest_chromosome[0]), "--", color='0.8', linewidth=1)

        box = a.get_position()
        a.set_position([box.x0, box.y0, box.width, box.height* 0.6])
        a.axis('off')
        a.set_title("Fittest Chromosome")

        canvas = FigureCanvasTkAgg(f, container)
        canvas.show()
        canvas.get_tk_widget().grid(row=row, column=col)

        self.toggle_input(status="normal", widgets=[Button])


def main():
    root = Tk()
    app = GenerationStepThroughWindow(root)
    root.mainloop() 

if __name__ == "__main__":
    main()
