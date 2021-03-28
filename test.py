from tkinter import *
root = Tk()

e = Entry(root, width=50)
e.pack()

def click():
    hello = "hello " + e.get()
    label = Label(root, text = hello)
    label.pack()

mybutton = Button(root, text = "enter name", command = click)
mybutton.pack()

root.mainloop()