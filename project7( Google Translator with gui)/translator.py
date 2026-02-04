from tkinter import *
from tkinter import ttk

root = Tk()
root.title("Quantiva Translator")
root.geometry("500x700")
root.configure(bg="#0012B3")

lab_txt = Label(
    root,
    text="Quantiva Translator",
    font=("Arial", 24),
    bg="#0012B3",
    fg="white"
)
lab_txt.place(x=100, y=40, height=50, width=300)

# Create a frame at the bottom
frame = Frame(root, bg="#0012B3")
frame.place(x=0, y=120, width=500, height=580)

Sor_txt = Text(
    frame,
    font=("Arial", 16),
    bg="white",
    fg="black",
    height=10,
    wrap=WORD
)
Sor_txt.place(x=10, y=10, height=100, width=480)

root.mainloop()
