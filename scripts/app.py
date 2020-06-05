""" Tkinter GUI for EasyTranspose app """

# import libraries
from .transpose import Transpose
import tkinter as tk

# initialize transpose object
t = Transpose()

# set up Tkinter
root = tk.Tk()
root.title("Easy Transpose")
canvas1 = tk.Canvas(root, width = 700, height = 350)
canvas1.pack()

# main title
label1 = tk.Label(root, text='Easy Transpose')
label1.config(font=('helvetica', 24))
canvas1.create_window(350, 25, window=label1)

# start note text entry field
label2 = tk.Label(root, text='Start Note')
label2.config(font=('helvetica', 10))
canvas1.create_window(100, 100, window=label2)

entry1 = tk.Entry (root) 
canvas1.create_window(100, 150, window=entry1)

""" Instrument """
# label 
label2 = tk.Label(root, text='Instrument')
label2.config(font=('helvetica', 10))
canvas1.create_window(350, 100, window=label2)

# dropdown menu
OPTIONS = list(t.instruments_IntervalPairs_pitchwise.keys()) #etc
var1 = tk.StringVar(root)
var1.set(OPTIONS[0]) # default value
w = tk.OptionMenu(root, var1, *OPTIONS)
w.pack()
entry2 = w
canvas1.create_window(350, 150, window=entry2)

""" Position """
# label
label3 = tk.Label(root, text='Start Position')
label3.config(font=('helvetica', 10))
canvas1.create_window(600, 100, window=label3)

# dropdown menu
OPTIONS = ['Concert --> Written', 'Written --> Concert' ]
var2 = tk.StringVar(root)
var2.set(OPTIONS[0]) # default value
w = tk.OptionMenu(root, var2, *OPTIONS)
w.pack()
entry3 = w
canvas1.create_window(600, 150, window=entry3)

# transpose button
def TransposeButton ():  
    
    # get data
    user_pitch = entry1.get()
    user_instrument = var1.get()
    user_position = var2.get()
    
    # clean directon data
    if user_position == 'Concert --> Written':
        user_position = 'Concert'
    else:
        user_position = 'Written'
    
    # transpose note
    tranposed_note = t.transpose(user_instrument, user_pitch, user_position)
    
    # display transposed note to user
    label4 = tk.Label(root, text= tranposed_note)
    label4.config(font=('helvetica', 18))
    canvas1.create_window(350, 300, window=label4)

# primary button for transposing notes
button1 = tk.Button(text='Transpose', command=TransposeButton)
canvas1.create_window(350, 225, window=button1)

# main loop
root.mainloop()
        