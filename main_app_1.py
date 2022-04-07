"""
    main window application to play with tkinter!
    reference link: https://www.youtube.com/channel/UCj7i-mmOjLV17YTPIrCPkog/videos (Alan D Moore Channel)
"""
import tkinter as tk
from unicodedata import category

root = tk.Tk()

root.title('Play with Me!')
root.geometry('800x600')
root.columnconfigure(1, weight=1)
root.rowconfigure(2, weight=2)

subject_lbl = tk.Label(root, text='Subject: ')
subject_lbl.grid(sticky=tk.E+tk.W)  # grid, pack, or place
subject_inp = tk.Entry(root)
subject_inp.grid(row=0, column=1, sticky=tk.E+tk.W, padx=5, pady=5)

cats = ['Work', 'Hobbies', 'Bills', 'Dogs']
cats_lbl = tk.Label(root, text='Category: ')
cats_inp = tk.Listbox(root, height=1)
cats_lbl.grid(row=1, column=0, sticky=tk.E+tk.W, padx=5, pady=5) # external padding
cats_inp.grid(row=1, column=1, sticky=tk.E+tk.W, padx=5, pady=5)

for cat in cats:
    cats_inp.insert(tk.END, cat)

msg_inp = tk.Text(root)
msg_inp.grid(row=2, column=0, columnspan=2, sticky=tk.N+tk.E+tk.S+tk.W)

save_btn = tk.Button(root, text='Save')
save_btn.grid(row=99, column=1, sticky=tk.E, ipadx=5, ipady=5) # internal padding

status_bar = tk.Label(root, text='')
status_bar.grid(row=100, column=0, columnspan=2, ipadx=5, ipady=5)

def save(): # callback method, will 'bind' this to Save button
    """Save the file"""
    subject = subject_inp.get()
    sel = cats_inp.curselection()
    if not sel:
        category = 'Misc'
    else:
        category = cats[sel[0]]

    message = msg_inp.get('1.0', tk.END) # get from text box line # '1.0' to end of box.

    file = f'{category}-{subject}.txt'
    with open(file, 'w') as fh:
        fh.write(message)

    status_bar.configure(text='File saved')

# note: much cleaner wway to 'bind' method seperate from above line
#   "save_btn = tk.Button(root, text='Save')", 
#   where you could have done,
#   "save_btn = tk.Button(root, text='Save', command=save)",
#   but this would have had a dependency on where you can 
#   place your method!
save_btn.configure(command=save)

# Display Loop
root.mainloop()
