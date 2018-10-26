#!/usr/bin/env python3
import time         # tools to manage time (e.g., sleep)
import io
import picamera     # tools for the Raspberry Pi camera
import numpy as np  # this allows us to create arrays of numbers
from picamera.array import PiRGBArray
# these next few lines import plotting tools
# import matplotlib
# from matplotlib import pyplot as plt
# this last one is openCV
import cv2

verbose = False #True
# set the camera up
if verbose:
    print('Initializing camera...')
camera = picamera.PiCamera()
camera.resolution = (1920,1088)
camera.framerate = 24
time.sleep(2) # sleep for 2 seconds to initialize camera hardware

# grab image, store in image in bgr format
if verbose:
    print('Acquiring feed...')
#cap =cv2.VideoStream(src=0, usePiCamera=True, resolution=camera.resolution, framerate=camera.framerate).start()

#cap = cv2.VideoCapture(0)

window = "Feed"
cv2.namedWindow(window, cv2.WINDOW_NORMAL)

bMin=0
bMax=255
gMin=0
gMax=255
rMin=210
rMax=255
minBGR = np.array([bMin, gMin, rMin])
maxBGR = np.array([bMax, gMax, rMax])

feed = PiRGBArray(camera, camera.resolution)
stream = io.BytesIO()

for rawFrame in camera.capture_continuous(feed, format="bgr", use_video_port=True):
	frame = rawFrame.array
	# empty = np.empty((1088,1920,3), dtype=np.uint8)
	# camera.capture(imageBGR, 'bgr')

	# write raw image to file
	# cv2.imwrite('rawImage.png',imageBGR)

	# convert original image to rgb
	# imageRGB = cv2.cvtColor(imageBGR, cv2.COLOR_BGR2RG
	# print(type(frame))

	if verbose:
    		print('Segmenting image...')
# set color thresholds
# use OpenCV inRange method to create a binary image based on the thresholds above
	
	imageMask = cv2.inRange(frame, minBGR, maxBGR) 

	if verbose:
    		print('Finding contours...')
# use OpenCV findContours method to find the outlines of the segmented blobs
	tmpImage, contours, hierarchy = cv2.findContours(imageMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# loop through all of the contours, if their area is within limits specified
# by areaMin and areaMax, put them on the image and compute their x,y coordinates
	if verbose:
    		print('Filtering contours and computing centroids...')
	areaMin = 400
	areaMax = 20000
	cntAreas = []
	biggestBoy = None
	bigBoy = None
	numContours = len(contours) # number of contours found
	# imageWithContours = imageRGB # make a copy of imageRGB to draw contours on
	centroids = np.empty((numContours,2), dtype=np.uint8) #initialize array to store centroids
	counter = 0 # initialize a counter to count filtered contours
	maxBench = 0
	
	for thisContour in contours:
		area = cv2.contourArea(thisContour) # compute contour area using OpenCV
		cntAreas.append(area)
		if area > areaMin and area < areaMax:
			cv2.drawContours(frame, [thisContour], 0, (255,0,0), 3)
	       		# draw current contour on image in red (255,0,0)
        		# moments and use them to centroid coordinates
        		# google cv2.moments for more informatation
			M = cv2.moments(thisContour)
			cx = int(M['m10']/M['m00'])
			cy = int(M['m01']/M['m00'])
			centroids[counter] = [cx, cy] # add current centroid to the list
#			print('Coordinates of contour #{}: {},{}'.format(counter,cx,cy))
		counter=counter+1
	# cntContours = [biggestBoy, bigBoy]
	# for i in range(len(cntContours)):
	# draw only the biggest ones
	#	cv2.drawContours(frame, cntContours[i], 0, (255,0,0), 3)
		
        # find max contour; first is a dud so moving on
	biggestArea = max(cntAreas)
	biggestBoy = cntAreas.index(biggestArea)
	cntAreas.remove(biggestArea)
	#
	biggestArea = max(cntAreas)
	biggestBoy = cntAreas.index(biggestArea)
	cntAreas.remove(biggestArea)
	
	bigArea = max(cntAreas)
	bigBoy = cntAreas.index(bigArea)

	if biggestBoy is not None and bigBoy is not None:
		
		x1, y1, w1, h1 = cv2.boundingRect(contours[biggestBoy])
		p1 = ((2*x1 + w1) // 2, (2*y1 + h1) // 2)
		x2, y2, w2, h2 = cv2.boundingRect(contours[bigBoy])
		p2 = ((2*x2 + w2) // 2, (2*y2 + h2) //2)
		# p1 = (centroids[biggestBoy][0], centroids[biggestBoy][1])
		# p2 = (centroids[bigBoy][0], centroids[bigBoy][1])
		print("p1:", p1, "p2:", p2)
	
		cv2.line(frame, p1, p2, color=(0, 255, 0), thickness=5)


	
	

# write imageWithCoutours to file
# first convert the image to BGR, which is the open cv standard format
#imageWithContoursBGR = cv2.cvtColor(imageWithContours, cv2.COLOR_RGB2BGR)
# then save the image
#cv2.imwrite('imageWithCountours.png',imageWithContoursBGR)
        
# display imageWithContours
	if verbose:
    		print('Preparing to display image...')
	# draws a line to determine the 'principle axis' of the axei
	cv2.imshow(window, frame)
	rawFrame.truncate(0)
	
	k = cv2.waitKey(1) & 0xFF
	if k == 27:
		cv2.destroyAllWindows()
		break
	
#print()

#print('Displaying image, close image window to exit')
#plt.show()

    
    
