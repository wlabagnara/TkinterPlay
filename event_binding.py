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
btn2.bind('<Return>', callback1)
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
root.bind('<<TimeChanged1>>', time_event) # my homemade 'custom' (or virtual?) event 'TimeChanged1'
ttk.Button(root, text="Click me for time check!", command=gen_time_change).pack() # the button handler will perform the gen event!
timeVar = tk.IntVar()
timeVar.set(0)
tk.Label(root, textvariable=timeVar ).pack()
# root.unbind('<<TimeChanged1>>') # c/i to see you can 'disable' event!

## main display loop
root.mainloop()