# USAGE
# python webcam.py --face cascades/haarcascade_frontalface_default.xml

# import the necessary packages
from pyimagesearch.facedetector import FaceDetector
from pyimagesearch import imutils
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import time
import cv2
import sys
import paho.mqtt.publish as pulish


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--face", required = True,
        help = "path to where the face cascade resides")
ap.add_argument("-v", "--video",
        help = "path to the (optional) video file")
args = vars(ap.parse_args())

# initialize the camera and grab a reference to the raw camera
# capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

# construct the face detector and allow the camera to warm
# up
fd = FaceDetector(args["face"])
time.sleep(0.1)
#print("invoke")
# capture frames from the camera
for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image
        frame = f.array
        # resize the frame and convert it to grayscale
        frame = imutils.resize(frame, width = 300)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # detect faces in the image and then clone the frame
        # so that we can draw on it
        faceRects = fd.detect(gray, scaleFactor = 1.1, minNeighbors = 5,
                minSize = (30, 30))
        frameClone = frame.copy()

        # faceRects is a list, if no face detected, the length will be 0
        
       	state1 = "OCCUPIED"
       	state2 = "FREE"
       	if len(faceRects) > 0:

       		f1 = open('/home/pi/codes/camera/state.txt') 
       		str1 = f1.read()
       		f1.close()
       		f = open('/home/pi/codes/camera/state.txt','w') 
       		if str1 == '':
       			print("Now the state is: ", state1)
       			f.write(str(state1))
       		elif str1 == state1:
       			print("The state hasn't changed.")
        	else:
        		print("The state has changed.")
       			f.write(str(state2))   
       		f.close()        	
       	else:
       		f2 = open('/home/pi/codes/camera/state.txt') 
       		str2 = f2.read()
       		f2.close()
       		f = open('/home/pi/codes/camera/state.txt','w') 
       		if str2 == '':
       			print("Now the state is: ", state2)
   				f.write(str(state2))
			elif str2 == state2:
   				print("The state hasn't changed.")
        	else:
        		print("The state has changed.")
       			f.write(str(state1)) 
       		f.close()      
            	
            	
        	
           	
           	
        # loop over the face bounding boxes and draw them
        for (fX, fY, fW, fH) in faceRects:
            cv2.rectangle(frameClone, (fX, fY), (fX + fW, fY + fH), (0, 255, 0), 2)

        # show our detected faces, then clear the frame in
        # preparation for the next frame
        cv2.imshow("Face", frameClone)
        rawCapture.truncate(0)

        # if the 'q' key is pressed, stop the loop
        if cv2.waitKey(1) & 0xFF == ord("q"):
                break
