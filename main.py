import tkinter as tk 
from tkinter import ttk
import fastf1 as ff1
from cache_path import cache_path

root = tk.Tk()
root.title('F1 Prediction')

ff1.Cache.enable_cache(cache_path)

def retrain_model():
 pass

def predict_winner():
 pass


root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

frame = ttk.Frame(root)
frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)

frame.columnconfigure(0, weight=1)
frame.rowconfigure(1, weight=1)

retrain_btn = ttk.Button(frame, text='Retrain Model', command=retrain_model)
retrain_btn.grid(row=0, column=0)

predict_btn = ttk.Button(frame, text='Predict Race Winner', command=predict_winner)
predict_btn.grid(row=0, column=1)

lbl = ttk.Label(frame, text='Label Text')
lbl.grid(row=1, column=0, columnspan=2, sticky='nsew')

root.mainloop()