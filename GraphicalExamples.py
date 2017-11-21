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
        self.master.geometry("1000x600")
        self.problems = ExampleProblems()
        self.chosen_problem = StringVar(self.master)
        self.chosen_problem.set(self.problems.problem_names[0].title())

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
        self.chromosome_count_entry = Entry(self.options_container )
        self.chromosome_count_entry.grid(row=2, column=1)
        self.chromosome_count_entry.insert(END, 100)

        Label(self.options_container, text="Generations").grid(row=3, column=0)
        self.generation_entry = Entry(self.options_container)
        self.generation_entry.grid(row=3, column=1)
        self.generation_entry.insert(END, 200)

        self.calc = Button(self.options_container, command=self._threaded_single_graph, text="Show Graphs")
        self.calc.grid(row=0, column=10)

        self.loading_label = Label(self.options_container, text="")
        self.loading_label.grid(row=0, column=11)

    def _threaded_single_graph(self):
        self.calc.config(state='disabled')
        t = Thread(target=self.single_graph, daemon=True)
        t.start()

    def single_graph(self):
        pop = Population()
        start_sample = list(pop.generate_random_sample(int(self.pop_size_entry.get()), int(self.chromosome_count_entry.get())))

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

def main():
    root = Tk()
    app = Window(root)
    root.mainloop() 

if __name__ == "__main__":
    main()
