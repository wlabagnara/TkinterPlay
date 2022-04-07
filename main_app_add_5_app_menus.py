"""
    main window application to play with tkinter!
"""
from re import sub
import tkinter as tk
# from unicodedata import category
import hashlib
from pathlib import Path
from tkinter import messagebox as tkmb
# from urllib import response
from tkinter import simpledialog as tksd
from tkinter import filedialog as tkfd

# methods

def save(): # callback method, will 'bind' this to Save button
    """Save the file"""
    subject = subject_var.get()
    category = cats_var.get()
    private = private_var.get()

    message = msg_inp.get('1.0', tk.END) # get from text box line # '1.0' to end of box.

    if private:
        passwd = tksd.askstring('Enter password', 'Enter a password to encrypt message')
        message = hashlib.md5(message.encode()).hexdigest()

    file = f'{category}-{subject}.txt'
    with open(file, 'w') as fh:
        fh.write(message)

    status_var.set(f'Message was saved to {file}')
    tkmb.showinfo('Saved', f'Saved that booger!')

def check_filename(*args):  
    """ Check if file exists already """
    subject = subject_var.get()
    category = cats_var.get()
    file = f'{category}-{subject}.txt'
    if Path(file).exists():
        status_var.set(f'WARNING: {file} already exists!')
    else:
        status_var.set('') # clear status

def private_warn(*args):
    private = private_var.get()
    if private:
        ok = tkmb.askokcancel("Are you sure?", "Do you really want to encrypt this message?")
        if ok == False:
            private_var.set(False)  # Something BUGGY with this clearing the checkbox!!!

def open_file():
    """ Open a file """
    file_path = tkfd.askopenfilename(
        title='Select a file to open', 
        filetypes=[('Secret','*.secret'), ('Text', '*.txt'), ('All', '*.*')]
        )

    if not file_path:
        return

    fp = Path(file_path)
    fn = fp.stem
    cat, subj = fn.split('-')
    message = fp.read_text()
    if Path.suffix == '.secret':
        passwd = tksd.askstring('Enter Password', 'Enter the encryption password.')
        # msg = crypto_algorithm(msg, passwd)

    cats_var.set(cat)
    subject_var.set(subj)
    msg_inp.delete('1.0', tk.END)
    msg_inp.insert('1.0', message)
    pass

def set_font_size(*args):  # with 'dummy' args - for use in a trace
    """ Set the size of the text widget font """
    size = font_size.get()
    msg_inp.configure(font=f'TKDefault {size}')


#define and configure main window
root = tk.Tk()
root.title('Play with Me!')
root.geometry('800x600')
root.columnconfigure(0, weight=1)
root.rowconfigure(2, weight=1)

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
#  tk.Checkbutton(root, variable=private_var, text='Private?').grid(ipadx=5, ipady=5, sticky='w')
#  add variable trace for 'private' checkbox changes
private_var.trace_add('write', private_warn)

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
# save_btn = tk.Button(root, text='Save')
# save_btn.grid(sticky=tk.E, ipadx=5, ipady=5) # internal padding

# open button (stack open button under save button)
# open_btn = tk.Button(root, text='Open')
# open_btn.grid(sticky=tk.E, ipadx=5, ipady=5)
# open_btn.configure(command=open_file)

# status bar (last row of view is status bar!)
status_var = tk.StringVar()
tk.Label(root, textvariable=status_var).grid(ipadx=5, ipady=5)

# note: 
# could have done "save_btn = tk.Button(root, text='Save', command=save)" in 
#   the line above, but this is a way to 'bind' our method seperately.
# save_btn.configure(command=save) # button event tied/bind to save operation

# add variable traces to force filename check on these variable updates
subject_var.trace_add('write', check_filename) # required '*args' added to check_filename method
cats_var.trace_add('write', check_filename)

# Menu
menu = tk.Menu(root)
root.configure(menu=menu)

file_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='Open', command=open_file)
file_menu.add_command(label='Save', command=save)
file_menu.add_separator()
file_menu.add_command(label='Quit', command=root.destroy)

options_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label='Options', menu=options_menu)
options_menu.add_checkbutton(label='Private', variable=private_var)

help_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label='Help', menu=help_menu)
help_menu.add_command(
    label = 'About',
    command=lambda: tkmb.showinfo('About', 'V1.0 - My time to play with Tkinter')
)

# radial buttons to adjust the font size
font_size = tk.IntVar(value=12)
set_font_size()
font_size.trace_add('write', set_font_size)  # adding trace

size_menu = tk.Menu(options_menu, tearoff=0) # submenu of options menu!
for size in range(6, 33, 2):
    size_menu.add_radiobutton(label=size, value=size, variable=font_size)

options_menu.add_cascade(menu=size_menu, label='Font Size')


# Display Loop
root.mainloop()
