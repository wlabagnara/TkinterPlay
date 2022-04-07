"""
    main window application to play with tkinter!
"""
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
root.columnconfigure(1, weight=1)
root.rowconfigure(2, weight=2)

# subject
subject_var = tk.StringVar() # control variable for two-way binding!
subject_lbl = tk.Label(root, text='Subject: ')
subject_lbl.grid(sticky=tk.E+tk.W)  # grid, pack, or place
# subject_inp = tk.Entry(root, textvariable=subject_var) # bind input to subject control var
# subject_inp.grid(row=0, column=1, sticky=tk.E+tk.W, padx=5, pady=5)
#  OR, don't need the reference 'subject_inp' so can replace above two lines with...
tk.Entry(root, textvariable=subject_var).grid(row=0, column=1, sticky=tk.E+tk.W, padx=5, pady=5)

# categories
cats_var = tk.StringVar() 
cats = ['Work', 'Hobbies', 'Bills', 'Dogs']
cats_lbl = tk.Label(root, text='Category: ')
cats_inp = tk.OptionMenu(root, cats_var, *cats) # bind input to cats control var, pecify '*' to cover any required args
cats_lbl.grid(row=1, column=0, sticky=tk.E+tk.W, padx=5, pady=5) # external padding
cats_inp.grid(row=1, column=1, sticky=tk.E+tk.W, padx=5, pady=5)

# private
private_var = tk.BooleanVar(value=False)
private_inp = tk.Checkbutton(root, variable=private_var, text='Private?')
private_inp.grid(row=2, column=0, ipadx=5, ipady=5)

# text box (note: no control var option available for this object)
msg_inp = tk.Text(root)
msg_inp.grid(row=3, column=0, columnspan=2, sticky=tk.N+tk.E+tk.S+tk.W)

# save button
save_btn = tk.Button(root, text='Save')
save_btn.grid(row=99, column=1, sticky=tk.E, ipadx=5, ipady=5) # internal padding

# status bar
status_var = tk.StringVar()
status_bar = tk.Label(root, textvariable=status_var)
status_bar.grid(row=100, column=0, columnspan=2, ipadx=5, ipady=5)

# note: 
# could have done "save_btn = tk.Button(root, text='Save', command=save)" in 
#   the line above, but this is a way to 'bind' our method seperately.
save_btn.configure(command=save) # button event tied/bind to save operation

# add variable traces to force filename check on these variable updates
subject_var.trace_add('write', check_filename) # required '*args' added to check_filename method
cats_var.trace_add('write', check_filename)

# Display Loop
root.mainloop()
