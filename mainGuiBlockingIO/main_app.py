"""
GUI application combining tkinter and async I/O threads.
reference: https://www.oreilly.com/library/view/python-cookbook/0596001673/ch09s07.html
           (reference code had to be updated to python 3)

Use case: Dealing with blocking operations (from sockets, serial I/O, etc. type comms) while running your GUI.

"""

import threading as th
import tkinter as tk
import time as t
import random as ran
from collections import deque

class GuiPart:
    def __init__(self, view, queue, endCommand):
        self.queue = queue

        view.title('GUI with thread')
        view.geometry('680x430')
        view.resizable(0,0)
        view.columnconfigure(0, weight=1)
        view.rowconfigure(1, weight=1)

        done_btn = tk.Button(view, text='Done', command=endCommand)
        self.msg_box = tk.Text(view)
        scroll_bar = tk.Scrollbar(self.msg_box)

        done_btn.grid(row=0, column=0, sticky=tk.W)

        self.msg_box.rowconfigure(0, weight=1)
        self.msg_box.columnconfigure(0, weight=1)
        self.msg_box.configure(yscrollcommand=scroll_bar.set)
        self.msg_box.insert('1.0', "No Data")
        self.msg_box.grid(row=1, sticky='nesw', padx=2, pady=2)

        scroll_bar.columnconfigure(0, weight=1)
        scroll_bar.configure(command=self.msg_box.yview)
        scroll_bar.grid(row=0, sticky='nse')

    def processIncoming(self):
        while self.queue:
            try:
                msg_str = str(self.queue.popleft())  + '\n'
                # print(f' {msg_str} ')
                self.msg_box.insert('1.0', msg_str)
            except:
                pass

class ThreadedClient:
    def __init__(self, view):
        self.view = view
        self.queue = deque()
        self.gui = GuiPart(view, self.queue, self.endApplication)
        self.running = 1
        self.thread1 = th.Thread(target=self.workerThread1)
        self.thread1.start()
        self.periodicCall()

    def periodicCall(self):
        """ Check every 200 ms if there is something in the queue """
        self.gui.processIncoming()
        if not self.running:
            self.view.destroy()
            # import sys
            # sys.exit(1) # brutal stop!
        self.view.after(200, self.periodicCall)

    def workerThread1(self):
        """ Handle the asynch blocking I/O """
        while self.running:
            t.sleep(ran.random() * 1.5)
            msg = ran.random()
            self.queue.append(msg)

    def endApplication(self):
        self.running = 0

## Main application

if __name__ == "__main__":
    rand = ran.Random()
    root = tk.Tk()
    client = ThreadedClient(root)
    root.mainloop()