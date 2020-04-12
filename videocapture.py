
import cv2
import numpy as np
 
# Opens the Video file
cap= cv2.VideoCapture("video_1.avi")
i=0
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == False:
        break
    cv2.imwrite('./test/test'+str(i//300)+'.jpg',frame)
    i+=1
 
cap.release()
cv2.destroyAllWindows()

im1 = cv2.imread('./test/test'+str(0)+'.jpg')

for i in range(1,9):
	im2 = cv2.imread('./test/test'+str(i)+'.jpg')
	im1 = cv2.hconcat([im1, im2])

cv2.imwrite('./test/testcombine.jpg', im1)