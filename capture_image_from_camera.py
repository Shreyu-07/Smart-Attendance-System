from cv2 import *
from cv2 import VideoCapture
from cv2 import imshow
import cv2
from cv2 import imwrite
cam_port = 0
cam = VideoCapture(cam_port)
# reading the input using the camera

inp = input('Enter person name')


while(1): 
        result,image = cam.read()
        imshow(inp, image)
        if cv2.waitKey(0):
         imwrite(inp+".png", image)
         print("image taken")

# If captured image is not working
else:
	print("No image detected. Please! try again")
