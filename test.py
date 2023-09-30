from tkinter import *
root = Tk()

def button_1():     
    button1.pack(side=TOP)

frame1 = Frame(root)    
button1 = Button(frame1, text="Button 1")

update_button = Button(root, text='Update', command=button_1)
update_button.pack()

def button():
    frame1.pack()
    
    button1.pack(side=LEFT)

    button2 = Button(frame1, text="Button 2")
    button2.pack(side=LEFT)


button()

root.mainloop()