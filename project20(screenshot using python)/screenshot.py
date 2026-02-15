from tkinter import *
from tkinter import messagebox
import pyautogui
import os


def take_screenshot():
    folder_path = entry.get().strip()

    if not folder_path:
        messagebox.showerror("Error", "Please enter a folder path!")
        return

    if not os.path.exists(folder_path):
        messagebox.showerror("Error", "Folder does not exist!")
        return

    file_path = os.path.join(folder_path, "screenshot.png")

    screenshot = pyautogui.screenshot()
    screenshot.save(file_path)

    messagebox.showinfo("Success", "Screenshot saved successfully!")


# Window
win = Tk()
win.title("Screenshot App")
win.geometry("350x220")
win.configure(bg="#dff6ff")
win.resizable(False, False)

# Title Label
Label(win, text="Screenshot App",
      font=("Arial", 16, "bold"),
      bg="#dff6ff").pack(pady=10)

# Entry
entry = Entry(win, width=35)
entry.pack(pady=10)

# Button
btn = Button(win,
             text="Take Screenshot",
             command=take_screenshot,
             bg="#4CAF50",
             fg="white",
             font=("Arial", 10, "bold"))
btn.pack(pady=15)

win.mainloop()
