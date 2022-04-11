""" 
Event class ?
Just encapsulating your view in your app via a class, but looks like a very good idea!
"""

import tkinter as tk
from tkinter import ttk

## 
class myguiapp: # no inherentance
    def __init__(self, view):
        self.view = view
        view.title("My GUI App!")
        self.lbl = ttk.Label(view, text="GUI APP")
        self.lbl.pack()
        self.btn1 = ttk.Button(view, text="Click her to enter", command=self.click_here)
        self.btn1.pack()
        self.btn2 = ttk.Button(view, text="Exit", command=view.quit)
        self.btn2.pack()

    def click_here(self):
        print("Welcome!")

class winguiapp(tk.Frame):  # inherit from tkinter Frame object!
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)  # should use super init?!
        self.master = master
        self.init_win()

    def init_win(self):
        self.master.title("My GUI App w/ Frame!")
        self.pack(fill=tk.BOTH, expand=1)
        btn1 = ttk.Button(self, text="quit", command=self.client_quit)
        btn1.place(x=0, y=0)

    def client_quit(self):
        exit()


## Main
root = tk.Tk()
root.geometry("300x300")
# my_app = myguiapp(root) # my app gui is in a class
my_app = winguiapp(root) 

root.mainloop()


    