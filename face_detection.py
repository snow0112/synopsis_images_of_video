import cv2
import sys
import imagetool

def detect_face(image):
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=4,
        minSize=(30, 30)
    )
    return len(faces)
    # for (x, y, w, h) in faces:
    #     print(x, y, w, h)
    #     cv2.rectangle(image, (int(x), int(y)), (int(x+w), int(y+h)), (255, 0, 0), 2)
    # # Display the output
    # cv2.imshow('img', image)
    # cv2.waitKey()
