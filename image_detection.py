import cv2 as cv
import requests
import time

ESP32_URL = "xxx"
API_URL = "xxx"

print("Connecting to camera stream...")

# Open the stream
cap = cv.VideoCapture(ESP32_URL)
if not cap.isOpened():
    print("Failed to connect to camera stream")
    exit()

while True:
    # capture frame by frame
    ret, frame = cap.read()
    if not ret:
        print("Failed to read a frame from the stream")
        break

    cv.imshow("ESP32-CAM Stream", frame)

    # wait for keypress
    key = cv.waitKey(1) & 0xFF

    # get the frame and send to apu by pressing 's'
    if key == ord('s'):
        # unique filename using timestamp
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"captured_{timestamp}.jpg"
        print(f"Capturing image: {filename}")
        cv.imwrite(filename, frame)

        # send image to FastAPI
        with open(filename, "rb") as f:
            response = requests.post(API_URL, files={"file": (filename, f, "image/jpeg")})

        if response.ok:
            print("Detected Ingredient:", response.json()["ingredient"])
        else:
            print("Error:", response.text)

    # Press 'q' to quit
    if key == ord('q'):
        break

cap.release()
cv.destroyAllWindows()