import tkinter as tk
from tkinter import filedialog, Text
from twilio.rest import Client
import os
from run import *
from sms import *
from back import *

root = tk.Tk()
root.title('twilioSMS')
rgbl = '#6B5A00'

canvas = tk.Canvas(root, height=150, width=300)
canvas.pack()

frame = tk.Frame(root, bg='#6B5A00')
frame.place(relheight=1, relwidth=1)

message = tk.Entry(frame, width=50, bg='#6B5A00', fg='#FFFFFF')
message.pack()
message.insert(0, 'message')

cell = tk.Entry(frame, width=50, bg='#6B5A00', fg='#FFFFFF')
cell.pack()
cell.insert(0, my_cell)

Send = tk.Button(frame, text='Send', padx=10,
                 pady=5, fg='#FFFFFF', bg='#6B5A00',
                 command=lambda: fsms(cell.get(), message.get()))
Send.pack()

Spam = tk.Button(frame, text='SPAM!', padx=10,
                 pady=5, fg='#FFFFFF', bg='#6B5A00',
                 command=lambda: fspam(cell.get(), message.get()))
Spam.pack()

# Color = tk.Button(frame, text='Change Color', padx=10,
#                  pady=5, fg='#FFFFFF', bg='#6B5A00',
#                  command=lambda: fcolor())

Quit = tk.Button(frame, text='Quit', padx=10,
                 pady=5, fg='#FFFFFF', bg='#6B5A00',
                 command=root.destroy)
Quit.pack()

root.mainloop()
