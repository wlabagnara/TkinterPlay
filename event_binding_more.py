"""
    Tkinter command and event binding
    references:
        https://pythonguides.com/python-tkinter-events/#Python_Tkinter_event_and_bind

"""

import tkinter as tk
from tkinter import ttk

def task(event):
    print("PYTHON!!!")

def quit_stop(event):
    print("Double click to stop")
    import sys; sys.exit() # NOTE: multiple statement per line ';' delimeter!

def show_label(event):
    lbl.configure(text="Here I am!", font=('Helvetica 14 bold'))

def hide_label(event):
    lbl.configure(text="")

## Main
root = tk.Tk()
root.title("Events are binding!")
root.geometry("300x300")

# btn = tk.Button(root, text="QUIT", command=root.quit)  # NOTE: simple way to quit window 
btn = tk.Button(root, text="Click me to quit")
btn.focus()
btn.pack()
btn.bind('<Button-1>', task)      # on single-click - run the handler 'task'
btn.bind('<Double-1>', quit_stop) # on double-click - run handler 'quit_stop'

## making label text 'appear' when button is pressed
lbl = tk.Label(root, text=" ")
lbl.pack(pady=50)
root.bind('<Motion>', show_label)
root.bind('<Leave>', hide_label)

##
def click1(event):
    print(f"you clicked on {event.widget}")
    event.widget.config(text="Thank You")

def click2(event, Obj):
    print(f"you clicked on {Obj}")
    Obj.config(text="Thank You!")

a1 = tk.Label(root, text="Press")
a2 = tk.Label(root, text="No, Press!")
a1.pack(pady=10)
a2.pack(padx=10)
a1.bind("<1>", click1)
a2.bind("<1>", lambda event, obj=a2: click2(event, obj))



root.mainloop()