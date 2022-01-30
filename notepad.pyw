import re
import tkinter as tk
import tkinter.ttk as ttk
from datetime import datetime
from tkinter import messagebox
from tkinter import filedialog,simpledialog
from tkinter.scrolledtext import ScrolledText
import os
color = { 
    'black1': '#323232',
    'black2': '#505050',
    'red1': '#FF3232',
    'red2': '#FF7878',
    'yellow': '#FFDC32',
    'green': '#78FF78',
    'blue1': '#00DCFF',
    'blue2': '#78B4FF',
    'purple1': '#7850FF',
    'purple2': '#9678FF',
    'orange1': '#FF9600',
    'orange2': '#FFB450',
    'white': '#F0F0F0'
}
btn_font = ('Lucidia-console 10')
window = tk.Tk()
window.update()
window.option_add('*font', 'Lucidia-console 10')
w_window = window.winfo_screenwidth()-100
h_window = window.winfo_screenheight()-100
pos_right = round(window.winfo_screenwidth() / 2 - w_window / 2)
pos_down = round(window.winfo_screenheight() / 2 - h_window / 2)
window.geometry('{}x{}+{}+{}'.format(w_window, h_window, pos_right, pos_down))
window['background'] = color['black1']
fade = True
title_bar_h = round(window.winfo_screenheight()/ 40)
dir_name = str(os.path.realpath(__file__))
dir_name = dir_name[:-11]
icon_img= tk.PhotoImage(file=dir_name+"\\assets\\icon.png")
window.iconphoto(False,icon_img)
def exiting():
    if fade:
        alpha = window.attributes("-alpha")
        if alpha > 0:
            alpha -= .05
            window.attributes("-alpha", alpha)
            window.after(5, exiting)
        else:
            quit()
    else:
        quit()
def startup():
    alpha = window.attributes("-alpha")
    if alpha < 1:
        alpha += .05
        window.attributes("-alpha", alpha)
        window.after(5, startup)
    else:
        return

if fade:
    window.attributes('-alpha', 0.0)
    startup()
notepad = ScrolledText(window, width = window.winfo_width(), height = window.winfo_height(),background=color['black1'],foreground=color['white'],insertbackground=color['white'])
fileName = ' '
def cmdNew():     
    global fileName
    if len(notepad.get('1.0', tk.END+'-1c'))>0:
        if messagebox.askyesno("Notepad", "Do you want to save changes?"):
            cmdSave()
        else:
            notepad.delete(0.0, tk.END)
def cmdOpen(): 
    fd = filedialog.askopenfile(parent = window, mode = 'r')
    t = fd.read() 
    notepad.delete(0.0, tk.END)
    notepad.insert(0.0, t)
def cmdSave(): 
    fd = filedialog.asksaveasfile(mode = 'w', defaultextension = '.txt')
    if fd!= None:
        data = notepad.get('1.0', tk.END)
    try:
        fd.write(data)
    except:
        messagebox.showerror(title="Error", message = "Not able to save file!")
def cmdSaveAs():
    fd = filedialog.asksaveasfile(mode='w', defaultextension = '.txt')
    t = notepad.get(0.0, tk.END)
    try:
        fd.write(t.rstrip())
    except:
        messagebox.showerror(title="Error", message = "Not able to save file!")
def cmdExit(): 
    if messagebox.askyesno("Notepad", "Are you sure you want to exit?"):
        exiting()
def cmdCut():
    notepad.event_generate("<<Cut>>")
def cmdCopy():
    notepad.event_generate("<<Copy>>")
def cmdPaste():
    notepad.event_generate("<<Paste>>")
def cmdClear():
    notepad.event_generate("<<Clear>>")
       
def cmdFind():
    notepad.tag_remove("Found",'1.0', tk.END)
    find = simpledialog.askstring("Find", "Find what:")
    if find:
        idx = '1.0'
    while 1:
        idx = notepad.search(find, idx, nocase = 1, stopindex = tk.END)
        if not idx:
            break
        lastidx = '%s+%dc' %(idx, len(find))
        notepad.tag_add('Found', idx, lastidx)
        idx = lastidx
    notepad.tag_config('Found', foreground = 'white', background = 'blue')
    notepad.bind("<1>", click)
def click(event):
    notepad.tag_config('Found',background='white',foreground='black')
def cmdSelectAll():
    notepad.event_generate("<<SelectAll>>")
    
def cmdTimeDate():
    now = datetime.now()
    dtString = now.strftime("%d/%m/%Y %H:%M:%S")
    label = messagebox.showinfo("Time/Date", dtString)
def cmdAbout():
    label = messagebox.showinfo("About Notepad", "Author\nJaivardhan Bhola\n")         
notepadMenu = tk.Menu(window)
window.configure(menu=notepadMenu)
fileMenu = tk.Menu(notepadMenu, tearoff = False,background=color['black2'],foreground=color['white'])
notepadMenu.add_cascade(label='File', menu = fileMenu)
fileMenu.add_command(label='New', command = cmdNew)
fileMenu.add_command(label='Open...', command = cmdOpen)
fileMenu.add_command(label='Save', command = cmdSave)
fileMenu.add_command(label='Save As...', command = cmdSaveAs)
fileMenu.add_separator()
fileMenu.add_command(label='Exit', command = cmdExit)
editMenu = tk.Menu(notepadMenu, tearoff = False,background=color['black2'],foreground=color['white'])
notepadMenu.add_cascade(label='Edit', menu = editMenu)
editMenu.add_command(label='Cut', command = cmdCut)
editMenu.add_command(label='Copy', command = cmdCopy)
editMenu.add_command(label='Paste', command = cmdPaste)
editMenu.add_command(label='Delete', command = cmdClear)
editMenu.add_separator()
editMenu.add_command(label='Find...', command = cmdFind)
editMenu.add_separator()
editMenu.add_command(label='Select All', command = cmdSelectAll)
editMenu.add_command(label='Time/Date', command = cmdTimeDate)
helpMenu = tk.Menu(notepadMenu, tearoff = False,background=color['black2'],foreground=color['white'])
notepadMenu.add_cascade(label='Help', menu = helpMenu)
helpMenu.add_command(label='About Notepad', command = cmdAbout)
notepad.pack()
window.title("Notepad")
window.mainloop()