from tkinter import *


def click():
 username = entry.get()

 if not username == "":
     print(f"Hello {username}")
 else:
     print("sup dude")




def delete(): #backspace remove
   # entry.delete(len(entry.get())-1,END)
    entry.delete(0, END)




def window():
    global entry

    window = Tk()
    window.geometry("340x200")
    window.title("my GUI")

    label = Label(window,
                  text = "Warehouse Container",
                  font =('arial',10),
                  fg = "#00ff00",
                  bg = "black",
                  relief = 'raised',
                  bd = 10,
                  padx = 20,
                  )
    label.place(x = 0, y = 0)

    entry = Entry(window,
                  font = ('arial',13),
                  show = "*"
                  )
    entry.place(x=70, y=40)

    deletebutton = Button(window,
                    text = "remove",
                    font = ("arial", 10),
                    fg = "#00ff00",
                    bg = "black",
                    relief = RAISED,
                    bd = 10,
                    activeforeground = '#00ff00',
                    activebackground = "black",
                    command=delete
                    )
    deletebutton.place(x = 10, y = 90)

    button = Button(window,
                    text = "click",
                    font = ("arial", 10),
                    fg = "#00ff00",
                    bg = "black",
                    relief = RAISED,
                    bd = 10,
                    activeforeground = '#00ff00',
                    activebackground = "black",
                    command=click
                    )
    button.place(x = 10, y = 40)



    window.mainloop()


window()