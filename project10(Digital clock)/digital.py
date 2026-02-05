from tkinter import *
import datetime

def date_time():
    now = datetime.datetime.now()

    hr = now.strftime("%I")
    minute = now.strftime("%M")
    sec = now.strftime("%S")
    am_pm = now.strftime("%p")
    date = now.strftime("%d %B %Y")

    lab_hr.config(text=hr)
    lab_min.config(text=minute)
    lab_sec.config(text=sec)
    lab_am.config(text=am_pm)
    lab_date.config(text=date)

    clock.after(1000, date_time)   # update every 1 second


clock = Tk()
clock.title("Quantiva Digital Clock")
clock.geometry("600x350")
clock.configure(bg="#0f172a")
clock.resizable(False, False)

title = Label(clock, text="Digital Clock", font=("Segoe UI", 24, "bold"),
              bg="#0f172a", fg="white")
title.pack(pady=10)

card = Frame(clock, bg="#020617", bd=0)
card.pack(pady=10, padx=20, fill=BOTH, expand=True)

time_frame = Frame(card, bg="#020617")
time_frame.pack(pady=30)

lab_hr = Label(time_frame, text="00", font=("Segoe UI", 48, "bold"), bg="#020617", fg="#38bdf8")
lab_hr.grid(row=0, column=0, padx=10)

Label(time_frame, text=":", font=("Segoe UI", 48, "bold"), bg="#020617", fg="white").grid(row=0, column=1)

lab_min = Label(time_frame, text="00", font=("Segoe UI", 48, "bold"), bg="#020617", fg="#38bdf8")
lab_min.grid(row=0, column=2, padx=10)

Label(time_frame, text=":", font=("Segoe UI", 48, "bold"), bg="#020617", fg="white").grid(row=0, column=3)

lab_sec = Label(time_frame, text="00", font=("Segoe UI", 48, "bold"), bg="#020617", fg="#38bdf8")
lab_sec.grid(row=0, column=4, padx=10)

lab_am = Label(time_frame, text="AM", font=("Segoe UI", 18, "bold"), bg="#020617", fg="#facc15")
lab_am.grid(row=0, column=5, padx=10, pady=20)

lab_date = Label(card, text="01 January 2026", font=("Segoe UI", 16),
                 bg="#020617", fg="#e5e7eb")
lab_date.pack(pady=10)

date_time()
clock.mainloop()
