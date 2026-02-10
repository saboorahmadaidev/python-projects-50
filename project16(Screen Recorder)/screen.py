import cv2
import pyautogui
import numpy as np
from win32api import GetSystemMetrics
import time

width = GetSystemMetrics(0)
height = GetSystemMetrics(1)
dim = (width, height)

f = cv2.VideoWriter_fourcc(*"XVID")
output = cv2.VideoWriter("test.mp4", f, 30.0, dim)

now_time = time.time()
dur = 10+4
end_time = now_time + dur
while True:
    img = pyautogui.screenshot()
    frame = np.array(img)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output.write(frame)

    c_time = time.time()
    if c_time > end_time:
        break   

output.release()
print("Done")
                                                                                                                                                                                                           
