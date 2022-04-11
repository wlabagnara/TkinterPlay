"""
    Tkinter command and event binding
    references:
        https://www.pythontutorial.net/tkinter/tkinter-command/
        https://www.pythontutorial.net/tkinter/tkinter-event-binding/


"""

import tkinter as tk
from tkinter import ttk


root = tk.Tk()

def btn_clicked_noargs():
    print('Button clicked')

def btn_clicked_args(*args):
    print(args[0])
    print(args[1])

def callback1(event):
    print('callback #1 for event...')
    print(event)

def callback2(event):
    print('callback #2 for event...')
    print(event)
    
def time_event(event): # event handler for 'custom' event demo
    timeVar.set(timeVar.get() + 1)
    print(event) # uses term 'VirtualEvent' when printed

def gen_time_change(): 
    root.event_generate('<<TimeChanged1>>', when='tail') 
    pass

## command binding - uses the 'command' option of widget (not avail for all widgets!)
##  callback has no arguments
btn1 = ttk.Button(root, text='Look Ma - No args!', command=btn_clicked_noargs)
btn1.pack()

##  if callback has arguments - requires 'lambda' expression
ttk.Button(root, text='Look Ma - UP!', command=lambda: btn_clicked_args('UP', 'Pizza')).pack()
ttk.Button(root, text='Look Ma - DN!', command=lambda: btn_clicked_args('DN', 2)).pack()

## event binding - not all widgets have a 'command' option
##  callback executed whenever 'enter' (or 'return') key is pressed
btn2 = ttk.Button(root, text='Press <Enter> for callbacks #1 and #2')
btn2.bind('<Return>', callback1)  # NOTE: single '<' and '>' brackets
btn2.focus() # event needs focus on button as well
btn2.pack(expand=True)

##  bind multiple handlers (callbacks) to same event
btn2.bind('<Return>', callback2, add='+') # adding another handler to existing event

## binding events to root (top-level) window
# root.bind('<Return>', handler)

## binding to all instances of a widget (class level binding)
# root.bind_class('Entry', '<Control-V>', paste) # bind event to all instances of textboxes (Entry widget = textbox)

## unbinding events
# <widget>.unbind(event)
# btn2.unbind('<Return>')

## Roll your own custom events !? --- WORKS!
root.bind('<<TimeChanged1>>', time_event) # my homemade 'custom' (or virtual?) event 'TimeChanged1' - NOTE: '<<' & '>>' brackets
ttk.Button(root, text="Click me for time check!", command=gen_time_change).pack() # the button handler will perform the gen event!
timeVar = tk.IntVar()
timeVar.set(0)
tk.Label(root, textvariable=timeVar ).pack()
# root.unbind('<<TimeChanged1>>') # c/i to see you can 'disable' event!

## Event GENERATE with timer thread and queue
##   <widget>.event_generate(sequence, when='tail')
import threading as th
import time as t
from collections import deque

data = deque()

def timer_thread():
    p_time = 0

    while True:
        data.append(p_time)
        try:
            root.event_generate('<<BillLabChanged>>', when='tail')
        except tk.TclError:
            break

        t.sleep(1)
        p_time += 1

def time_changed(event):
    a_var.set(data.popleft())

a_var = tk.IntVar()
ttk.Label(root, text="Thread timer counts using queue and gen events:").pack(pady=10)
ttk.Label(root, textvariable=a_var, width=9).pack()

root.bind('<<BillLabChanged>>', time_changed)

task = th.Thread(target=timer_thread)
task.start()

## Event loop  w/ 'time.asctime()'
def swap_text():
    lbl['text'] = t.asctime()
    root.after(1000, swap_text) # run every second - NOTE: good way to 'poll' something as well?!

frm = ttk.Frame(root)
frm.pack(fill='both', expand=True)
lbl = ttk.Label(frm, text='0')
lbl.pack(pady=10)
swap_text()

## Event LISTENER
def modify(*args):
    print("Listening...")

ev_var = tk.StringVar()
ev_var.set("DELETE ME")
ev_var.trace("w", modify)  # NOTE: 'listen' for changes to variable 'ev_var'
text_var = tk.Entry(root, textvariable=ev_var)
text_var.pack()

## Event keysym - set keys in the string for letter, numbers and special characters
##   used to describe keyboard events
def key(e):
    if e.char == e.keysym:
        msg = f'Normal key {e.char}'
    elif len(e.char) == 1:
        msg = f'Punctuation key {e.keysym} {e.char}'
    else:
        msg = f'Special key {e.keysym}'
    lbl2.config(text=msg)

def do_mouse(e_name):
    def mouse_binding(e):
        msg = f'Mouse event {e_name}'
        lbl2.config(text=msg)
    lbl2.bind_all(f'{mouse_binding} {e_name}')

display = 'Press any key for me to detect....'
lbl2 = tk.Label(root, text=display, width=len(display))
lbl2.pack(pady=40)

lbl2.bind_all('<Key>', key)

for i in range(1,4):
    do_mouse(f'Button-{i}')
    do_mouse(f'ButtonRelease-{i}')
    do_mouse(f'Double-Button-{i}')



## main display loop
root.mainloop()