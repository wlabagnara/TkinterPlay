import tkinter as tk
from tkinter import ttk

from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


from math import sin

from matplotlib.figure import Figure

# class globals
t = []
[t.append(x/15.87) for x in list(range(0,101))]


class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sine Wave Plot")
        self.geometry('1024x768')
        # self.minsize(640, 400)

        # y = A sin(wt + b) + c
        self.amplitude = 1
        self.frequency = 1
        self.phase_shift = 0
        self.vertical_shift = 0

        # entry display frame
        self.frm = ttk.Frame(self)
        self.frm.grid(column=0, row=0, sticky=tk.NSEW, padx=10, pady=10)

        # graph display frame
        self.frm2 = ttk.Frame(self)
        self.frm2.grid(column=0, row=1, sticky=tk.NSEW, padx=10, pady=10)

        ttk.Label(self.frm, text = "Amplitude").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.amplitude_entry = ttk.Entry(self.frm, width=10)
        self.amplitude_entry.grid(row=0, column=1, sticky='w')

        ttk.Label(self.frm, text="Frequency").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.frequency_entry = ttk.Entry(self.frm, width=10)
        self.frequency_entry.grid(row=1, column=1, sticky='w')

        ttk.Label(self.frm, text="Vertical Shift").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.vertical_shift_entry = ttk.Entry(self.frm, width=10)
        self.vertical_shift_entry.grid(row=2, column=1, sticky='w')

        ttk.Label(self.frm, text="Phase Shift").grid(row=3, column=0, sticky='w', padx=5, pady=5)
        self.phase_shift_entry = ttk.Entry(self.frm, width=10)
        self.phase_shift_entry.grid(row=3, column=1, sticky='w')

        btn1 = ttk.Button(self.frm, text="Calculate", command=self.update_values)
        btn1.grid(row=4, column=0, padx=5, pady=5, sticky='w')

        self.fig, self.ax = plt.subplots() 
        self.bind("<Return>", self.update_values)
        self.plot_values()

    def update_values(self, event=None):
        self.amplitude = float(self.amplitude_entry.get())
        self.phase_shift = float(self.phase_shift_entry.get())
        self.vertical_shift = float(self.vertical_shift_entry.get())
        self.frequency = float(self.frequency_entry.get())
        self.plot_values()

    def plot_values(self):
        y = []
        [y.append(self.amplitude * sin(self.frequency * x + self.phase_shift) + self.vertical_shift) for x in t]

        plt.cla() 
        plt.grid() # adds grid lines to graph 
        # plt.style.use('seaborn')
        # plt.style.use('ggplot')
        # plt.style.use('fivethirtyeight')        

        self.ax.plot(t, y, color='#444444', linestyle='--', label='signal')  
        self.ax.legend()
        self.ax.set_title('Sine Wave') 
        self.ax.set_xlabel('time')                      
        self.ax.set_ylabel('amplitude')        
        self.ax.set_xlim([0, 6.3]) # 0 to ~2Pi
        self.ax.set_ylim([-3, 3])

        chart = FigureCanvasTkAgg(self.fig, self.frm2)
        chart.get_tk_widget().grid(row=0, column=0, padx=10, pady=10, sticky=tk.NSEW)

        toobar = NavigationToolbar2Tk(chart, self.frm2, pack_toolbar=False)
        toobar.grid(row=1, column=0, padx=10, pady=10, sticky=tk.NSEW)
        # plt.tight_layout()

if __name__ == "__main__":
    """ Starting point for running the main application."""
 
    app = Window() 
    app.mainloop()