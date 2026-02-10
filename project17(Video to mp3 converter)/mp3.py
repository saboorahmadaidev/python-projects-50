import moviepy
from tkinter.filedialog import *

vid = askopenfilename()

video = moviepy.editor.VideoFileClip(vid)
audio = video.audio
audio.write_audiofile("demo.mp3")
print("Done")