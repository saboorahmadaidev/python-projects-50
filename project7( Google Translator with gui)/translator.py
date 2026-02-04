from tkinter import *
from tkinter import ttk
from googletrans import Translator, LANGUAGES

def change(text="type", src="en", dest="ur"):
    translator = Translator()
    result = translator.translate(text, src=src, dest=dest)
    return result.text

def data():
    src_lang_name = comb_sor.get()
    dest_lang_name = comb_dest.get()

    src_code = lang_map.get(src_lang_name, "en")
    dest_code = lang_map.get(dest_lang_name, "ur")

    msg = src_txt.get("1.0", END).strip()
    if msg:
        translated_text = change(text=msg, src=src_code, dest=dest_code)
        dest_txt.delete("1.0", END)
        dest_txt.insert(END, translated_text)

def swap_langs():
    a = comb_sor.get()
    b = comb_dest.get()
    comb_sor.set(b)
    comb_dest.set(a)

# Window
root = Tk()
root.title("Quantiva Translator")
root.geometry("520x720")
root.configure(bg="#0f172a")  

# Styles 
style = ttk.Style()
style.theme_use("clam")
style.configure("Card.TFrame", background="#0b1220")
style.configure("Title.TLabel", background="#0f172a", foreground="white", font=("Segoe UI", 22, "bold"))
style.configure("Sec.TLabel", background="#0b1220", foreground="#e5e7eb", font=("Segoe UI", 12, "bold"))
style.configure("TCombobox", font=("Segoe UI", 11))
style.configure("Accent.TButton", font=("Segoe UI", 11, "bold"))

#  Header 
title = ttk.Label(root, text="Quantiva Translator", style="Title.TLabel")
title.pack(pady=16)

#  Card Container 
card = ttk.Frame(root, style="Card.TFrame", padding=16)
card.pack(padx=16, pady=10, fill=BOTH, expand=True)

#  Source 
ttk.Label(card, text="Source Text", style="Sec.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 6))
src_txt = Text(card, font=("Segoe UI", 12), height=7, wrap=WORD, bd=0, highlightthickness=1)
src_txt.grid(row=1, column=0, columnspan=3, sticky="nsew", pady=(0, 12))

# Destination
ttk.Label(card, text="Translated Text", style="Sec.TLabel").grid(row=2, column=0, sticky="w", pady=(8, 6))
dest_txt = Text(card, font=("Segoe UI", 12), height=7, wrap=WORD, bd=0, highlightthickness=1)
dest_txt.grid(row=3, column=0, columnspan=3, sticky="nsew", pady=(0, 12))

#  Languages
lang_map = {v.title(): k for k, v in LANGUAGES.items()}
langs = sorted(lang_map.keys())

comb_sor = ttk.Combobox(card, values=langs, state="readonly")
comb_sor.grid(row=4, column=0, sticky="ew", padx=(0, 8))
comb_sor.set("English")

swap_btn = ttk.Button(card, text="⇄ Swap", command=swap_langs)
swap_btn.grid(row=4, column=1, sticky="ew")

comb_dest = ttk.Combobox(card, values=langs, state="readonly")
comb_dest.grid(row=4, column=2, sticky="ew", padx=(8, 0))
comb_dest.set("Urdu")

#  Action 
translate_btn = ttk.Button(card, text="Translate", style="Accent.TButton", command=data)
translate_btn.grid(row=5, column=0, columnspan=3, sticky="ew", pady=(14, 4))

#  Layout behavior 
card.columnconfigure(0, weight=1)
card.columnconfigure(1, weight=0)
card.columnconfigure(2, weight=1)
card.rowconfigure(1, weight=1)
card.rowconfigure(3, weight=1)

root.mainloop()
