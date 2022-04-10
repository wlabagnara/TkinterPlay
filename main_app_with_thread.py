""" 
Tkinter GUI and Threads
reference: https://groups.google.com/g/comp.lang.python/c/gNSCyxqBpJU?pli=1

Very good reference, but had to be updated to python 3 in order to work.

"""

import threading
import time
from collections import deque
import tkinter as tk
import atexit as ae


## Threads
def timeThread1():
    curTime = 0
    while 1:
        ## Each time the time increases, put the new value in the queue...
        commQueue1.append(curTime)
        ## ... and generate a custom event on the main window
        try:
            root.event_generate('<<TimeChanged1>>', when='tail')
        ## If it failed, the window has been destoyed: over
        except tk.TclError:
            break
        
        time.sleep(.01) # this thread will sleep every 10 ms
        curTime += 1

def timeThread2():
    curTime = 0
    while 1:
        commQueue2.append(curTime)

        try:
            root.event_generate('<<TimeChanged2>>', when='tail')
        except tk.TclError:
            break

        time.sleep(5) # this thread will sleep every 5 seconds
        curTime += 1

## Methods 

def timeChanged1(event):
    timeVar1.set(commQueue1.popleft())

def timeChanged2(event):
    timeVar2.set(commQueue2.popleft())

## Main GUI

root = tk.Tk()
root.title('Play with GUI and threads!')

## Communication queue
commQueue1 = deque()
commQueue2 = deque()

tk.Label(root, text='** Two timer threads run while their tick counts are displayed in the GUI **').pack()

tk.Label(root, text='Timer 1: ').pack()
timeVar1 = tk.IntVar()
tk.Label(root, textvariable=timeVar1, width=8, fg='blue').pack()

tk.Label(root, text='Timer 2: ').pack()
timeVar2 = tk.IntVar()
tk.Label(root, textvariable=timeVar2, width=8, fg='blue').pack()

## Bind to associated control var changes
root.bind('<<TimeChanged1>>', timeChanged1) 
root.bind('<<TimeChanged2>>', timeChanged2)

## Init and run threads
th1=threading.Thread(target=timeThread1)    
th2=threading.Thread(target=timeThread2)
th1.start()
th2.start()

## GUI display loop
ae.register(lambda root=root: root.destroy()) # main window kill to avoid nasty thread messages and zombie procs?
root.mainloop()