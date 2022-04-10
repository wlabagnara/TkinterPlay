""" 
Tkinter GUI updates widget from thread that is encapsulated in a Class method
   Queue and event used to pass widget value from Class to GUI 
   and GUI widget value to Class object.

"""

import tkinter as tk
import atexit as ae
import threading
from collections import deque
import time as t

## Classes

class TimeSimulator:

    def __init__(self, display, comms_queue, comms_queue2):
        self.curTime = 0
        self.display = display
        self.comms_queue = comms_queue
        self.comms_queue2 = comms_queue2

    def timeThread1(self): # THREAD METHOD: test method to see if GUI <---> Thread are behaving

        while 1:            

            if self.comms_queue2 and self.comms_queue2.popleft() == 'RESET':
                    self.curTime = 0

            self.comms_queue.append(self.curTime)

            try:
                self.display.event_generate('<<TimeChanged1>>', when='tail')
            except: # tk.TclError:
                break
        
            t.sleep(5) # this thread will sleep every x seconds
            self.curTime += 1

## Methods

def timeChanged1(event): # event handler for comms with GUI
    timeVar1.set(commQueue1.popleft())

def resetCount():
    commQueue2.append('RESET')
    timeVar1.set(0)
    

## Main GUI

root = tk.Tk()
root.title('Play with GUI - Class threads!')

commQueue1 = deque() # Communication queue between GUI <---> thread
commQueue2 = deque() 

timeVar1 = tk.IntVar() # Control variable to update widget value from queuing between GUI <---> thread

sim = TimeSimulator(root, commQueue1, commQueue2) # Init class with display and queue objects

tk.Label(root, text='** A Class timer thread runs while its tick counts are displayed in the GUI **').pack()

tk.Label(root, text='Tick Counts (5s/tick): ').pack()
tk.Label(root, textvariable=timeVar1, width=8, fg='blue').pack()

root.bind('<<TimeChanged1>>', timeChanged1) # bind specific display widget control variable to specific event

tk.Button(text='Reset Count', command=resetCount).pack()

## Init and start thread
th1=threading.Thread(target=sim.timeThread1) # run class method as thread    
th1.start()

## GUI display loop
ae.register(lambda root=root: root.destroy()) # main window kill to avoid nasty thread messages and zombie procs?
root.mainloop()
