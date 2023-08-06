import tkinter as tk
from tkinter import filedialog, Text
from twilio.rest import Client
import os
from run import *

root = tk.Tk()
root.title('twilioSMS')

canvas = tk.Canvas(root, height=150, width=300)
canvas.pack()

frame = tk.Frame(root, bg='#6B5A00')
frame.place(relheight=1, relwidth=1)

client = Client(account_sid, auth_token)

message = tk.Entry(frame, width=50, bg='#6B5A00', fg='#FFFFFF')
message.pack()
message.insert(0, 'message')

cell = tk.Entry(frame, width=50, bg='#6B5A00', fg='#FFFFFF')
cell.pack()
cell.insert(0, my_cell)


fsms = lambda: client.messages.create(
    to=cell.get(), from_=my_twilio, body=message.get())


def fspam():
    i = 0
    while i < 5:
        fsms()
        i += 1


Send = tk.Button(frame, text='Send', padx=10,
                 pady=5, fg='#FFFFFF', bg='#6B5A00',
                 command=fsms)
Send.pack()

Spam = tk.Button(frame, text='SPAM!', padx=10,
                 pady=5, fg='#FFFFFF', bg='#6B5A00',
                 command=fspam)
Spam.pack()

Quit = tk.Button(frame, text='Quit', padx=10,
                 pady=5, fg='#FFFFFF', bg='#6B5A00',
                 command=root.destroy)
Quit.pack()

root.mainloop()
