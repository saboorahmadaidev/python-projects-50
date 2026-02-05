from tkinter import *
from tkinter import messagebox
import os

def restart():
    if messagebox.askyesno("Confirm Restart", "Are you sure you want to restart your PC?"):
        os.system("shutdown /r /t 1")

def restart_timer():
    if messagebox.askyesno("Confirm Restart", "Restart after 20 seconds?"):
        os.system("shutdown /r /t 20")

def logout():
    if messagebox.askyesno("Confirm Logout", "Are you sure you want to log out?"):
        os.system("shutdown -l")

def shutdown_pc():
    if messagebox.askyesno("Confirm Shutdown", "Are you sure you want to shutdown your PC?"):
        os.system("shutdown /s /t 1")


st = Tk()
st.title("Power Control")
st.geometry("420x320")
st.configure(bg="#0f172a")
st.resizable(False, False)

title = Label(st, text="⚡ Power Control Panel", 
              font=("Segoe UI", 18, "bold"), 
              bg="#0f172a", fg="white")
title.pack(pady=15)

subtitle = Label(st, text="Manage your system power safely", 
                 font=("Segoe UI", 10), 
                 bg="#0f172a", fg="#94a3b8")
subtitle.pack(pady=5)

frame = Frame(st, bg="#0f172a")
frame.pack(pady=20)

restart_btn = Button(frame, text="🔄 Restart Now", 
                     font=("Segoe UI", 12, "bold"),
                     bg="#3b82f6", fg="white", bd=0, padx=20, pady=10,
                     command=restart)
restart_btn.grid(row=0, column=0, padx=10, pady=10)

timer_btn = Button(frame, text="⏳ Restart in 20s", 
                   font=("Segoe UI", 12, "bold"),
                   bg="#6366f1", fg="white", bd=0, padx=20, pady=10,
                   command=restart_timer)
timer_btn.grid(row=0, column=1, padx=10, pady=10)

shutdown_btn = Button(frame, text="⏻ Shutdown", 
                      font=("Segoe UI", 12, "bold"),
                      bg="#ef4444", fg="white", bd=0, padx=20, pady=10,
                      command=shutdown_pc)
shutdown_btn.grid(row=1, column=0, padx=10, pady=10)

logout_btn = Button(frame, text="🚪 Log Out", 
                    font=("Segoe UI", 12, "bold"),
                    bg="#f59e0b", fg="white", bd=0, padx=20, pady=10,
                    command=logout)
logout_btn.grid(row=1, column=1, padx=10, pady=10)


footer = Label(st, text="⚠ Use carefully. Actions are irreversible.", 
               font=("Segoe UI", 9),
               bg="#0f172a", fg="#94a3b8")
footer.pack(side=BOTTOM, pady=10)

st.mainloop()
