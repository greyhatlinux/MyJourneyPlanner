import tkinter as tk
import tkinter.messagebox as tkmsg
import datetime as dt
import time

def ui():
    root = tk.Tk()
    root.title("My Journey Planner")
    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()
    x = w/4
    y = h/4
    root.geometry('%dx%d+%d+%d' % (w/2, h/2, x, y))
    # date = "Time Now: " + str(dt.datetime.now())
    # myLabel = tk.Label(root, text=date)
    # myLabel.pack()

    curr_time = time.strftime('%H:%M:%S %p')
    clock_label = tk.Label(root, padx=20, text=curr_time, bg="green", fg="black")
    clock_label.pack()

    def update_time():
        curr_time = time.strftime('%H:%M:%S %p')
        clock_label.config(text="Time Now: " + str(curr_time))
        clock_label.after(1000, update_time)



    def show():
        label = tk.Label(root, text="From: " + str(from_var.get()) + " To: " + str(to_var.get()) + ", at: " + str(at_var.get())).pack()

    def howToPopup():
        tkmsg.showinfo(title="How to Guide is here!", message="1. Fill the 'from' station \n2. Fill the 'to' station \n3. Fill the 'at' section in 24 hour format.\nEx: 14:10, if it is 2:10 pm\n4. Click the 'Submit' button")

    from_var = tk.StringVar()
    from_var.set("A")
    from_station = tk.OptionMenu(root, from_var, "A", "B", "C", "D", "E")
    from_station.pack()
    from_label = tk.Label(root, text="From", pady=10).pack()

    to_var = tk.StringVar()
    to_var.set("A")
    to_station = tk.OptionMenu(root, to_var, "A", "B", "C", "D", "E")
    to_station.pack()
    to_label = tk.Label(root, text="To", pady=10).pack()

    at_var = tk.Entry(root, width=10)
    at_var.pack()
    at_label = tk.Label(root, text="At", pady=10).pack()
    
    submit_btn = tk.Button(root, text="Submit", command=show)
    submit_btn.pack()

    howTo_btn = tk.Button(root, text="How to use this window", pady=15, command=howToPopup)
    howTo_btn.pack()

    btn = tk.Button(root, text="Close", width=10, command=root.quit)
    btn.pack()
    update_time()
    root.mainloop()