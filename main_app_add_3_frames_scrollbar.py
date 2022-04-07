"""
    main window application to play with tkinter!
"""
from re import sub
import tkinter as tk
# from unicodedata import category
import hashlib
from pathlib import Path

# methods

def save(): # callback method, will 'bind' this to Save button
    """Save the file"""
    subject = subject_var.get()
    category = cats_var.get()
    private = private_var.get()

    message = msg_inp.get('1.0', tk.END) # get from text box line # '1.0' to end of box.

    if private:
        message = hashlib.md5(message.encode()).hexdigest()

    file = f'{category}-{subject}.txt'
    with open(file, 'w') as fh:
        fh.write(message)

    status_var.set(f'Message was saved to {file}')

def check_filename(*args):  
    """ Check if file exists already """
    subject = subject_var.get()
    category = cats_var.get()
    file = f'{category}-{subject}.txt'
    if Path(file).exists():
        status_var.set(f'WARNING: {file} already exists!')
    else:
        status_var.set('') # clear status


#define and configure main window
root = tk.Tk()
root.title('Play with Me!')
root.geometry('800x600')
root.columnconfigure(0, weight=1)
root.rowconfigure(2, weight=2)

# subject
subj_frame = tk.Frame(root) # frame for 'nesting layouts' - geometry will 'reset'
subj_frame.columnconfigure(1, weight=1) # note: '1' for object in column 1 (column 0 object is the label)
subject_var = tk.StringVar() # control variable for two-way binding!
tk.Label(subj_frame, text='Subject: ').grid(sticky=tk.E+tk.W)  
tk.Entry(subj_frame, textvariable=subject_var).grid(row=0, column=1, sticky=tk.E+tk.W, padx=5, pady=5)
subj_frame.grid(sticky='ew') # each frame can have seperate layout types (grid/pack)

# categories
cat_frame = tk.Frame(root)
cat_frame.columnconfigure(1, weight=1)
cats_var = tk.StringVar() 
cats = ['Work', 'Hobbies', 'Bills', 'Dogs']
cats_lbl = tk.Label(cat_frame, text='Category: ')
cats_inp = tk.OptionMenu(cat_frame, cats_var, *cats) 
cats_lbl.grid(sticky=tk.E+tk.W, padx=5, pady=5) 
cats_inp.grid(row=0, column=1, sticky=tk.E+tk.W, padx=5, pady=5)
cat_frame.grid(sticky='ew') # no col,row args needed b/c we want 'next availlable' display location

# private
private_var = tk.BooleanVar(value=False)
private_inp = tk.Checkbutton(root, variable=private_var, text='Private?')
private_inp.grid(ipadx=5, ipady=5, sticky='w')

# text box (note: no control var option available for this object)
msg_frame = tk.LabelFrame(root, text='Message')
msg_frame.columnconfigure(0, weight=1)
msg_inp = tk.Text(msg_frame)
msg_inp.grid(sticky=tk.N+tk.E+tk.S+tk.W)
msg_frame.grid(sticky='nesw')

# add scroll bar onto above text box
#  note: cannot add scroll bar to Frame, but can add it to text box in the frame
scroll_bar = tk.Scrollbar(msg_frame)
scroll_bar.grid(row=0, column=1, sticky='nse')
scroll_bar.configure(command=msg_inp.yview)      # scrollbar will scroll text
msg_inp.configure(yscrollcommand=scroll_bar.set) # scrollbar will track text vertically

# save button
save_btn = tk.Button(root, text='Save')
save_btn.grid(sticky=tk.E, ipadx=5, ipady=5) # internal padding

# status bar
status_var = tk.StringVar()
status_bar = tk.Label(root, textvariable=status_var)
status_bar.grid(row=100, ipadx=5, ipady=5)

# note: 
# could have done "save_btn = tk.Button(root, text='Save', command=save)" in 
#   the line above, but this is a way to 'bind' our method seperately.
save_btn.configure(command=save) # button event tied/bind to save operation

# add variable traces to force filename check on these variable updates
subject_var.trace_add('write', check_filename) # required '*args' added to check_filename method
cats_var.trace_add('write', check_filename)

# Display Loop
root.mainloop()
