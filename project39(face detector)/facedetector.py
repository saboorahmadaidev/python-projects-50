import cv2
import time

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

if face_cascade.empty():
    print(" Error loading cascade file")
    exit()


url = "your ip webcam stream url here"

camera = cv2.VideoCapture(url)

if not camera.isOpened():
    print(" Could not open video stream")
    exit()

print(" Camera started")
print("Press Q to quit")

frame_count = 0
start_time = time.time()

while True:
    ret, frame = camera.read()

    if not ret:
        print("⚠️ Failed to receive frame")
        break

    
    frame = cv2.resize(frame, (640, 480))

   
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

   
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(30, 30)
    )

    
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.putText(
            frame,
            "Face Detected",
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 0, 0),
            2
        )

   
    frame_count += 1
    elapsed_time = time.time() - start_time
    fps = frame_count / elapsed_time

    cv2.putText(
        frame,
        f"FPS: {fps:.2f}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2
    )

   
    cv2.putText(
        frame,
        f"Faces: {len(faces)}",
        (10, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2
    )

    
    cv2.imshow("Face Detector", frame)


    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        print("🔴 Exiting...")
        break

camera.release()
cv2.destroyAllWindows()
print("Program closed cleanly")