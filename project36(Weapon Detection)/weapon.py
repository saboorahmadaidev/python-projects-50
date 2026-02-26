import cv2
import imutils
import datetime

cascade = cv2.CascadeClassifier('cascade.xml')

# IP camera URL (replace with your own)
url = "your ip webcam stream url here"

camera = cv2.VideoCapture(url)

if not camera.isOpened():
    print("❌ Error: Could not open video stream.")
    exit()

print("✅ Security feed started. Press 'Q' to exit.")

while True:
    ret, frame = camera.read()

    if not ret:
        print("❌ Failed to grab frame.")
        break

    frame = imutils.resize(frame, width=600)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    detections = cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(100, 100)
    )

    object_exists = False

    for (x, y, w, h) in detections:
        object_exists = True
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, "Object Detected",
                    (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2)

    if object_exists:
        print("⚠️ Object detected at:", datetime.datetime.now())
    else:
        print("No object detected at:", datetime.datetime.now())

    cv2.imshow("Security Feed", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
print("🔴 Security feed stopped.")