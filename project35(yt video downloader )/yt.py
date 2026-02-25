import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import yt_dlp
import shutil
from pathlib import Path

# ---------------- Utility functions ---------------- #
def human_size(bytesize):
    if bytesize is None:
        return "Unknown"
    for unit in ["B", "KB", "MB", "GB"]:
        if bytesize < 1024:
            return f"{bytesize:.2f} {unit}"
        bytesize /= 1024
    return f"{bytesize:.2f} TB"

def ffmpeg_available():
    return shutil.which("ffmpeg") is not None

# ---------------- Main App ---------------- #
class AutolevateDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("Autolevate Downloader")
        self.root.geometry("700x480")
        self.root.resizable(False, False)

        # theme / style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#0f172a")
        style.configure("Title.TLabel", background="#0f172a", foreground="white", font=("Segoe UI", 18, "bold"))
        style.configure("TLabel", background="#0f172a", foreground="#e6eef8", font=("Segoe UI", 10))
        style.configure("Card.TFrame", background="#071129")
        style.configure("Accent.TButton", font=("Segoe UI", 11, "bold"))
        style.configure("TCombobox", font=("Segoe UI", 10))

        self.url_var = tk.StringVar()
        self.folder_path = ""
        self.formats = {}  # label -> format_spec
        self.format_meta = {}  # label -> metadata dict (filesize etc.)

        self.create_ui()
        self.check_ffmpeg()

    def create_ui(self):
        root = self.root

        header = ttk.Label(root, text="Autolevate Downloader", style="Title.TLabel")
        header.pack(pady=(12, 6))

        outer = ttk.Frame(root, style="TFrame")
        outer.pack(fill="both", expand=True, padx=12, pady=8)

        card = ttk.Frame(outer, style="Card.TFrame", padding=(14, 14))
        card.pack(fill="both", expand=True)

        # URL row
        ttk.Label(card, text="YouTube URL:").grid(row=0, column=0, sticky="w")
        url_entry = ttk.Entry(card, textvariable=self.url_var, width=60)
        url_entry.grid(row=0, column=1, columnspan=3, sticky="w", pady=6)

        # Folder choose
        choose_btn = ttk.Button(card, text="Choose Folder", style="Accent.TButton", command=self.choose_folder)
        choose_btn.grid(row=1, column=0, pady=6, sticky="w")

        self.folder_label = ttk.Label(card, text="No folder selected", style="TLabel")
        self.folder_label.grid(row=1, column=1, columnspan=3, sticky="w")

        # Fetch formats
        self.fetch_btn = ttk.Button(card, text="Fetch Qualities", command=self.fetch_formats_thread, style="Accent.TButton")
        self.fetch_btn.grid(row=2, column=0, pady=(12, 6), sticky="w")

        ttk.Label(card, text="Select Quality:").grid(row=3, column=0, sticky="w", pady=(6, 0))

        self.quality_combo = ttk.Combobox(card, state="readonly", width=48)
        self.quality_combo.grid(row=3, column=1, columnspan=2, sticky="w", pady=(6, 0))
        self.quality_combo.bind("<<ComboboxSelected>>", self.on_quality_select)

        # Show format info (size, type)
        self.info_label = ttk.Label(card, text="Size: --    Type: --", style="TLabel")
        self.info_label.grid(row=4, column=1, columnspan=2, sticky="w", pady=(6, 0))

        # Download / Auto
        self.download_btn = ttk.Button(card, text="Download", command=self.start_download_thread, style="Accent.TButton")
        self.download_btn.grid(row=5, column=1, pady=12, sticky="w")

        self.auto_btn = ttk.Button(card, text="Download Auto (bestvideo+bestaudio)", command=self.start_auto_download_thread)
        self.auto_btn.grid(row=5, column=2, pady=12, sticky="w")

        # Progress bar
        self.progress = ttk.Progressbar(card, length=520, mode="determinate")
        self.progress.grid(row=6, column=0, columnspan=4, pady=(8, 6))

        # Status
        self.status_label = ttk.Label(card, text="Status: Idle", style="TLabel")
        self.status_label.grid(row=7, column=0, columnspan=4, sticky="w", pady=(6, 0))

        # column sizing
        card.columnconfigure(1, weight=1)

    def check_ffmpeg(self):
        if not ffmpeg_available():
            messagebox.showwarning("FFmpeg Missing", "FFmpeg is not found in PATH. Merging video+audio (720p+) will fail without ffmpeg.\nInstall FFmpeg and add to PATH for best results.")

    def choose_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path = folder
            self.folder_label.config(text=folder)

    def set_ui_busy(self, busy=True):
        state = "disabled" if busy else "normal"
        self.fetch_btn.state([ "disabled" ]) if busy else self.fetch_btn.state([ "!disabled" ])
        self.download_btn.state([ "disabled" ]) if busy else self.download_btn.state([ "!disabled" ])
        self.auto_btn.state([ "disabled" ]) if busy else self.auto_btn.state([ "!disabled" ])

    # ---------- Fetch formats (threaded) ---------- #
    def fetch_formats_thread(self):
        t = threading.Thread(target=self.fetch_formats)
        t.daemon = True
        t.start()

    def fetch_formats(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL.")
            return
        if not self.folder_path:
            # folder optional for fetching; not required
            pass

        try:
            self.set_ui_busy(True)
            self.status_label.config(text="Status: Fetching formats...")
            ydl_opts = {"quiet": True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)

            # Build format list
            self.formats.clear()
            self.format_meta.clear()
            quality_list = []

            # Add an Auto option (bestvideo+bestaudio fallback to best)
            auto_label = "Auto: bestvideo+bestaudio / best"
            self.formats[auto_label] = "bestvideo+bestaudio/best"
            self.format_meta[auto_label] = {"filesize": info.get("filesize_approx") or info.get("size") or None, "type": "auto"}
            quality_list.append(auto_label)

            # iterate formats
            # we want: progressive streams (video+audio) and video-only with height info
            seen = set()
            for f in info.get("formats", []):
                # we'll present video-only streams and progressive streams
                vcodec = f.get("vcodec")
                acodec = f.get("acodec")
                height = f.get("height")
                fm_id = f.get("format_id")
                ext = f.get("ext")
                note = f.get("format_note") or ""
                # prefer showing height if available
                if vcodec and vcodec != "none":
                    if acodec and acodec != "none":
                        # progressive
                        label = f"{height or note}p (progressive) - {ext} - id:{fm_id}"
                        if label not in seen:
                            self.formats[label] = fm_id  # direct format id
                            self.format_meta[label] = {"filesize": f.get("filesize_approx") or f.get("filesize") or None, "type": "progressive"}
                            quality_list.append(label)
                            seen.add(label)
                    else:
                        # video only
                        if height:
                            label = f"{height}p (video-only) - {ext} - id:{fm_id}"
                            if label not in seen:
                                # format spec will be format_id + bestaudio (so merging will happen)
                                self.formats[label] = f"{fm_id}+bestaudio/best"
                                self.format_meta[label] = {"filesize": f.get("filesize_approx") or f.get("filesize") or None, "type": "video-only"}
                                quality_list.append(label)
                                seen.add(label)

            # sort quality_list: put auto first, then descending by resolution if possible
            def sort_key(lbl):
                if lbl == auto_label:
                    return 10_000
                # extract digits at start
                import re
                m = re.match(r"(\d+)", lbl)
                if m:
                    return int(m.group(1))
                return 0

            # reverse sort so highest resolution first, but keep auto at top
            quality_list = sorted(quality_list[1:], key=sort_key, reverse=True)
            quality_list.insert(0, auto_label)

            # update UI on main thread
            self.quality_combo['values'] = quality_list
            if quality_list:
                self.quality_combo.current(0)
                self.on_quality_select()  # update info label

            self.status_label.config(text="Status: Qualities loaded ✅")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch formats:\n{e}")
            self.status_label.config(text="Status: Idle")
        finally:
            self.set_ui_busy(False)

    # ---------- progress hook ---------- #
    def progress_hook(self, d):
        # d may contain keys: status, downloaded_bytes, total_bytes, _percent_str, percent
        status = d.get("status")
        if status == "downloading":
            # try multiple ways to parse percent
            percent = d.get("_percent_str") or (f"{d.get('percent', 0):.2f}%")
            try:
                p = float(str(percent).replace("%", "").strip())
                self.progress['value'] = p
            except Exception:
                pass
            self.status_label.config(text=f"Status: Downloading... {percent}")
        elif status == "finished":
            self.progress['value'] = 100
            self.status_label.config(text="Status: Download finished. Merging if needed...")

    # ---------- download ---------- #
    def start_download_thread(self):
        t = threading.Thread(target=self.download_video)
        t.daemon = True
        t.start()

    def start_auto_download_thread(self):
        t = threading.Thread(target=self.download_auto)
        t.daemon = True
        t.start()

    def download_auto(self):
        if not self.folder_path:
            messagebox.showerror("Error", "Choose a destination folder first.")
            return
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Enter a YouTube URL first.")
            return

        self.set_ui_busy(True)
        self.progress['value'] = 0
        self.status_label.config(text="Status: Starting Auto download...")

        ydl_opts = {
            "format": "bestvideo+bestaudio/best",
            "merge_output_format": "mp4",
            "outtmpl": f"{self.folder_path}/%(title)s.%(ext)s",
            "progress_hooks": [self.progress_hook],
            "noplaylist": True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.status_label.config(text="Status: Download complete ✅")
        except Exception as e:
            messagebox.showerror("Error", f"Download failed:\n{e}")
            self.status_label.config(text="Status: Error")
        finally:
            self.set_ui_busy(False)

    def download_video(self):
        if not self.folder_path:
            messagebox.showerror("Error", "Choose a destination folder first.")
            return
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Enter a YouTube URL first.")
            return

        selected = self.quality_combo.get()
        if not selected:
            messagebox.showerror("Error", "Choose a quality first.")
            return

        format_spec = self.formats.get(selected)
        if not format_spec:
            messagebox.showerror("Error", "Invalid format chosen.")
            return

        self.set_ui_busy(True)
        self.progress['value'] = 0
        self.status_label.config(text=f"Status: Starting download ({selected})...")

        ydl_opts = {
            "format": format_spec,
            "merge_output_format": "mp4",
            "outtmpl": f"{self.folder_path}/%(title)s.%(ext)s",
            "progress_hooks": [self.progress_hook],
            "noplaylist": True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.status_label.config(text="Status: Download complete ✅")
        except Exception as e:
            messagebox.showerror("Error", f"Download failed:\n{e}")
            self.status_label.config(text="Status: Error")
        finally:
            self.set_ui_busy(False)

    def on_quality_select(self, event=None):
        sel = self.quality_combo.get()
        if not sel:
            self.info_label.config(text="Size: --    Type: --")
            return
        meta = self.format_meta.get(sel, {})
        size = human_size(meta.get("filesize"))
        ftype = meta.get("type", "--")
        self.info_label.config(text=f"Size: {size}    Type: {ftype}")

# ---------------- Run ---------------- #
if __name__ == "__main__":
    root = tk.Tk()
    app = AutolevateDownloader(root)
    root.mainloop()