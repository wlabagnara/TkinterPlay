"""
    main window application to play with tkinter submodule ttk!
    reference: https://youtu.be/SYbfBajIsSw (Alan D Moore Codes)

"""
# from atexit import unregister
# import imp
# from re import sub
import tkinter as tk
# from unicodedata import category
import hashlib
from pathlib import Path
from tkinter import messagebox as tkmb
# from urllib import response
from tkinter import simpledialog as tksd
from tkinter import filedialog as tkfd
from tkinter import ttk # adding ttk --> replace your 'tk's w/ 'ttk's - where applicable !
import datetime
from turtle import back, bgcolor

import time as t

# methods

def save(): # callback method, will 'bind' this to Save button
    """Save the file"""
    subject = subject_var.get()
    category = cats_var.get()
    private = private_var.get()
    ftype = 'txt'
    message = msg_inp.get('1.0', tk.END) # get from text box line # '1.0' to end of box.

    if private:
        passwd = tksd.askstring('Enter password', 'Enter a password to encrypt message')
        message = hashlib.md5(message.encode()).hexdigest()
        ftype = 'secret'

    file = f'{category}-{subject}.{ftype}'
    with open(file, 'w') as fh:
        fh.write(message)

    status_var.set(f'Message was saved to {file}')
    tkmb.showinfo('Saved', f'Saved that booger!')
    pop_treeview() # add your new file to file view tab

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

def set_font_size(*args):  # with 'dummy' args - for use in a trace
    """ Set the size of the text widget font """
    size = font_size.get()
    msg_inp.configure(font=f'TKDefault {size}')

def pop_treeview(*args):
    """Look for text and secret files to populate the treeview"""

    # avoid error or problem of not adding newly saved file - clear out list first
    children = file_tree.get_children()
    if children:
        file_tree.delete(*children)

    txt_files = list(Path('.').rglob('*.txt'))    # unencrypted file extension - (using 'generator' list!)
    sec_files = list(Path('.').rglob('*.secret')) # encrypted file extension
    for f in (txt_files + sec_files):
        created = datetime.date.fromtimestamp(f.stat().st_mtime).strftime('%Y-%m-%d')
        file_tree.insert('', tk.END, iid=f.name, values=(f.stem,f.suffix, created))

def treeview_sort_column(treeview, col, reverse):
    """ Sort a treeview column when clicked """
    data = [
        (treeview.set(iid, col), iid)        # set will actually 'get' value needed!
        for iid in treeview.get_children('')
    ]

    data.sort(reverse=reverse)

    for index, (sort_val, iid) in enumerate(data):
        treeview.move(iid, '', index)
    
    # if click column again, then reverse sort order
    treeview.heading(
        col,
        command=lambda c=col: treeview_sort_column(treeview, c, not reverse)
    )

def set_theme(*args):
    theme = theme_var.get()
    style.theme_use(theme)


#define and configure main window
root = tk.Tk()
root.title('Play with Me --- TTK !')
root.geometry('860x660')
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.configure(bg='#888')

# ttk themes and styles - create once and use reference to it where used
# make a 'theme switcher'
theme_var = tk.StringVar()
theme_var.trace_add('write', set_theme)
theme_var.set('default')

# styles are more 'granular' than themes
style = ttk.Style()
# print(style.theme_names()) # see the list of available themse
style.configure('TLabel', font='Arial 18 bold') # 'T<widget class name>' - Every Label's font will change!
style.configure('TCheckbutton', font='Arial 16 bold', background='silver') 
style.configure('TRadiobutton', font='Arial 16', background='light blue')
style.configure('TLabelframe', font='Arial 18 bold', background='light pink')
style.configure('TLabelframe.Label', font='Arial 18 bold', background='light blue') # 'T<widget.subclass' 
# what if you don't want all T<widget>'s to change - just some of them? - A: Custom style
style.configure('Status.TLabel', font='Arial 12', background='green') 
# note: 'Status' part can be anything, but must end with widget class name, 'TLabel' in this case.
#       Now go, ~ line 225, and add 'style='Status.TLabel' field to the specific widget constructor
#       i.e. - ttk.Label( ...., style='Status.TLabel', ...)
# also, this applies to TTK widgets only.

# dynamic styling - how the widget behaves during 'states' - does this with 'map' function
style.map( 'TRadiobutton', font=[('selected', 'Arial 16 bold')])  # the radiobutton 'selected' state
style.map('TCheckbutton', background=[('selected', 'green'), ('active', 'purple'), ('disabled', 'black')])



# ttk offers 'notebook' widget - gives you tabs
#  previously added sub-frames for our widgets to make 
#   adding our notebook easier.
nb = ttk.Notebook(root)
nb.grid(sticky=tk.N+tk.E+tk.W+tk.S, padx=5, pady=5)
nb.enable_traversal() # can use arrow keys to switch tabs

# sub-frame for form
form_frm = ttk.Frame(nb)  # adding this frame to our new notebook
form_frm.grid(sticky=tk.N+tk.E+tk.W+tk.S, padx=5, pady=5)
form_frm.columnconfigure(0, weight=1)
form_frm.rowconfigure(5, weight=1)
nb.add(form_frm, text='Notebook Entry', underline=0) # underline first letter of tab text (ALT+char to switch)

# to add another notebook tab...
# dummy_frm = ttk.Frame(nb)
# nb.add(dummy_frm, text='Dummy Entry', underline=1) # underline second letter of tab text (ALT+char to switch)

# subject
subj_frame = ttk.Frame(form_frm) # frame for 'nesting layouts' - geometry will 'reset'
subj_frame.columnconfigure(1, weight=1) # note: '1' for object in column 1 (column 0 object is the label)
subject_var = tk.StringVar() # control variable for two-way binding!
ttk.Label(subj_frame, text='Subject: ').grid(sticky=tk.W+tk.E)  
ttk.Entry(subj_frame, textvariable=subject_var).grid(row=0, column=1, sticky=tk.E+tk.W)
subj_frame.grid(sticky='ew') # each frame can have seperate layout types (grid/pack)

# categories
cat_frame = ttk.Frame(form_frm)
cat_frame.columnconfigure(1, weight=1)
cats_var = tk.StringVar() 
cats = ['Work', 'Hobbies', 'Bills', 'Dogs']
ttk.Label(cat_frame, text='Category: ').grid(sticky=tk.E+tk.W, padx=5, pady=5) 
# ttk.OptionMenu(cat_frame, cats_var, cats[0], *cats).grid(row=0, column=1, sticky=tk.E+tk.W, padx=5) # note: ttk needed 3rd arg.
ttk.Combobox(cat_frame, textvariable=cats_var, values=cats).grid(row=0, column=1, sticky=tk.E+tk.W, padx=5) # ttk upgrade OptionMenu to ComboBox
cat_frame.grid(sticky='ew') # no col,row args needed b/c we want 'next availlable' display location
ttk.Separator(form_frm, orient=tk.HORIZONTAL).grid(sticky='ew') # ttk supports separators

# private indication menu item and checkbox
private_var = tk.BooleanVar(value=False)
ttk.Checkbutton(form_frm, variable=private_var, text='Private?').grid(ipadx=5, ipady=2, sticky='w')

# Datestamp selection radio button
datestamp_var = tk.StringVar(value='none')
datestamp_frm = tk.Frame(form_frm)
for value in ('None', 'Date', 'Date+Time'):
    ttk.Radiobutton(
        datestamp_frm,
        text=value,
        value=value,
        variable=datestamp_var
    ).pack(side=tk.LEFT)
datestamp_frm.grid(row=2, sticky='e')

# text box message (note: no control var option available for this object)
msg_frame = ttk.LabelFrame(form_frm, text='Message')
msg_frame.columnconfigure(0, weight=1)
msg_frame.rowconfigure(0, weight=1)
msg_inp = tk.Text(msg_frame, foreground='navy', background='khaki') # adding theme/style to 'tk' widget
msg_inp.grid(sticky=tk.N+tk.E+tk.S+tk.W)
msg_frame.grid(sticky='nesw')

# add scroll bar onto above text box
#  note: cannot add scroll bar to Frame, but can add it to text box in the frame
scroll_bar = ttk.Scrollbar(msg_frame)
scroll_bar.grid(row=0, column=1, sticky='nse')
scroll_bar.configure(command=msg_inp.yview)      # scrollbar will scroll text
msg_inp.configure(yscrollcommand=scroll_bar.set) # scrollbar will track text vertically

# status bar (last row of view is status bar!)
status_var = tk.StringVar()
ttk.Label(root, textvariable=status_var, style='Status.TLabel').grid(row=100, ipadx=5, ipady=5, pady=5, sticky='we')

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

#  add variable trace for 'private' changes
private_var.trace_add('write', private_warn)
options_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label='Options', menu=options_menu)
options_menu.add_checkbutton(label='Private', variable=private_var)

help_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label='Help', menu=help_menu)
help_menu.add_command(
    label = 'About',
    command=lambda: tkmb.showinfo('About', 'V1.0 - My time to play with Tkinter')
)

# save button
save_btn = ttk.Button(form_frm, text='Save')
save_btn.grid(sticky=tk.E, ipadx=5, ipady=5) # internal padding
save_btn.configure(command=save) # button event tied/bind to save operation

# radial buttons to adjust the font size
font_size = tk.IntVar(value=12)
set_font_size()
font_size.trace_add('write', set_font_size)  # adding trace

size_menu = tk.Menu(options_menu, tearoff=0) # submenu of options menu!
for size in range(6, 33, 2):
    size_menu.add_radiobutton(label=size, value=size, variable=font_size)

options_menu.add_cascade(menu=size_menu, label='Font Size')

# Files view (using Treeview)
files_frm = ttk.Frame(nb)
nb.add(files_frm, text='Files', underline=0)
files_frm.columnconfigure(0, weight=1)
files_frm.rowconfigure(0, weight=1)
file_tree = ttk.Treeview(files_frm)
file_tree.grid(sticky='news')

ft_cols = ('Name', 'Type', 'Created')
file_tree.configure(columns=ft_cols)
[file_tree.heading(heading, text=heading) for heading in ft_cols]
file_tree.configure(show='headings') # to get rid of 'icon' column (that first blank heading)
pop_treeview()

# ability sort file view (treeview) when column clicked
for col in ft_cols:
    file_tree.heading(
        col,
        command=lambda c=col: treeview_sort_column(file_tree, c, False)
    )

theme_menu = tk.Menu(options_menu, tearoff=0)
options_menu.add_cascade(menu=theme_menu, label='Theme')
[theme_menu.add_radiobutton(label=theme, value=theme, variable=theme_var) for theme in style.theme_names()]

count = 0

# *** Display Loop ***

# root.mainloop()

# OR call update in while loop!...

while True:
    
    root.update()
    count = count+1
    # print( f' Count is: {count}' )
    t.sleep(.200)