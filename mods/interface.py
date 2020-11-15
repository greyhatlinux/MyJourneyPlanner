import tkinter as tk
import datetime as dt

def ui():
    root = tk.Tk()
    root.title("My Journey Planner")
    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()
    x = w/4
    y = h/4
    root.geometry('%dx%d+%d+%d' % (w/2, h/2, x, y))
    date = "Time Now: " + str(dt.datetime.now())
    myLabel = tk.Label(root, text=date)
    myLabel.pack()
    btn = tk.Button(root, text="Close", width=10, command=root.destroy)
    btn.pack()
    root.mainloop()