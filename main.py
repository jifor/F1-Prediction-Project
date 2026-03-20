import tkinter as tk 
from tkinter import ttk
import fastf1 as ff1
from cache_path import cache_path

root = tk.Tk()
root.title('F1 Prediction')

ff1.Cache.enable_cache(cache_path)

def function(event=None):
    session = ff1.get_session(2025, 1, 'R')
    lbl.config(text='Getting race winner...')
    session.load()
    winner = session.results.loc['1', 'FullName']
    lbl.config(text=f'The winner of the {session.event['OfficialEventName']} was {winner}')


root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

frame = ttk.Frame(root)
frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

frame.columnconfigure(0, weight=1)
frame.rowconfigure(1, weight=1)

btn = ttk.Button(frame, text='Add', command=function)
btn.grid(row=0, column=0)

lbl = ttk.Label(frame, text='Label Text')
lbl.grid(row=1, column=0)

root.mainloop()