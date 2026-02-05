from tkinter import *
from tkinter import ttk
import speedtest
import threading

def check_speed():
    status_lbl.config(text="Testing speed...", fg="#facc15")
    download_lbl.config(text="-- Mbps")
    upload_lbl.config(text="-- Mbps")

    def run_test():
        try:
            st = speedtest.Speedtest()
            st.get_best_server()
            download_speed = st.download() / 1_000_000
            upload_speed = st.upload() / 1_000_000

            download_lbl.config(text=f"{download_speed:.2f} Mbps")
            upload_lbl.config(text=f"{upload_speed:.2f} Mbps")
            status_lbl.config(text="Test completed ✔", fg="#22c55e")

        except Exception as e:
            status_lbl.config(text="Error checking speed ❌", fg="#ef4444")

    threading.Thread(target=run_test).start()


# Window
sp = Tk()
sp.title("Quantiva Speed Test")
sp.geometry("520x420")
sp.configure(bg="#0f172a")
sp.resizable(False, False)

# Title
title = Label(sp, text="Internet Speed Tester", font=("Segoe UI", 22, "bold"),
              bg="#0f172a", fg="white")
title.pack(pady=15)

# Card
card = Frame(sp, bg="#020617", bd=0)
card.pack(padx=20, pady=10, fill=BOTH, expand=True)

# Download
Label(card, text="Download Speed", font=("Segoe UI", 14, "bold"),
      bg="#020617", fg="#38bdf8").pack(pady=(20, 5))
download_lbl = Label(card, text="-- Mbps", font=("Segoe UI", 20, "bold"),
                     bg="#020617", fg="white")
download_lbl.pack()

# Upload
Label(card, text="Upload Speed", font=("Segoe UI", 14, "bold"),
      bg="#020617", fg="#38bdf8").pack(pady=(20, 5))
upload_lbl = Label(card, text="-- Mbps", font=("Segoe UI", 20, "bold"),
                   bg="#020617", fg="white")
upload_lbl.pack()

# Status
status_lbl = Label(card, text="Click button to test speed",
                   font=("Segoe UI", 11),
                   bg="#020617", fg="#94a3b8")
status_lbl.pack(pady=20)

# Button
test_btn = Button(card, text="Check Speed", command=check_speed,
                  font=("Segoe UI", 12, "bold"),
                  bg="#38bdf8", fg="#020617", relief=FLAT)
test_btn.pack(pady=10, ipadx=20, ipady=6)

sp.mainloop()
