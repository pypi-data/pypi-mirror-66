import tkinter as tk
from tkinter import filedialog, Text
from twilio.rest import Client
import os
from run import *

root = tk.Tk()

canvas = tk.Canvas(root, height=300, width=300,  bg='#6B5A00')
canvas.pack()

client = Client(account_sid, auth_token)

message = tk.Entry(canvas, width=50, bg='#6B5A00', fg='#FFFFFF')
message.pack()
message.insert(0, 'message')

cell = tk.Entry(canvas, width=50, bg='#6B5A00', fg='#FFFFFF')
cell.pack()
cell.insert(0, my_cell)


def fsms():
    client.messages.create(
        to=cell.get(),
        from_=my_twilio,
        body=message.get()
    )


Send = tk.Button(canvas, text='Send', padx=10,
                 pady=5, fg='#FFFFFF', bg='#6B5A00',
                 command=fsms)
Send.pack()

quit = tk.Button(canvas, text='Quit', padx=10,
                 pady=5, fg='#FFFFFF', bg='#6B5A00',
                 command=root.destroy)
quit.pack()

root.title('twilioSMS')
root.mainloop()

