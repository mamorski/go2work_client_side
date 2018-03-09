import tkinter as tk


def raise_frame(frame):
    frame.tkraise()


root = tk.Tk()
root.geometry('300x200')

Home = tk.Frame(root)
PageOne = tk.Frame(root)
PageTwo = tk.Frame(root)

for frame in (Home, PageOne, PageTwo):
    frame.grid(row = 0, column = 0, sticky = 'news')

lbl = tk.Label(Home, text = 'Home')  # .pack(fill = tk.BOTH, expand = tk.YES, side = tk.TOP)
lbl.grid(row=10, column=50, columnspan=4, rowspan=10, sticky=tk.S+tk.N+tk.W+tk.E)
#tk.Button(Home, text = 'Go to Page1', command = lambda: raise_frame(PageOne)).pack(fill = tk.BOTH, expand = tk.YES,side = tk.RIGHT)
# lbl1.grid(row=0, column=1, sticky='n')
# btn1.grid(row=2, column=10, sticky='n')

# tk.Label(PageOne, text = 'Page 1').pack()
# tk.Button(PageOne, text = 'Go to Page 2', command = lambda: raise_frame(PageTwo)).pack()

# tk.Label(PageTwo, text = 'Page 2').pack()
# tk.Button(PageTwo, text = 'Go Home', command = lambda: raise_frame(Home)).pack()

raise_frame(Home)
root.mainloop()
