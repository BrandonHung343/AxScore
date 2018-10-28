#!/usr/bin/env python3

print('Welcome to simple axe detector')
print()
# make this true to print out status messages while running
verbose = True

# import some useful libraries
if verbose:
    print('Loading modules...')
import time         # tools to manage time (e.g., sleep)
import picamera     # tools for the Raspberry Pi camera
import numpy as np  # this allows us to create arrays of numbers
# these next few lines import plotting tools
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
# this last one is openCV
import cv2

# set the camera up
if verbose:
    print('Initializing camera...')
camera = picamera.PiCamera()
camera.resolution = (1920,1088)
camera.framerate = 24
time.sleep(2) # sleep for 2 seconds to initialize camera hardware

# grab image, store in image in bgr format
if verbose:
    print('Acquiring image...')
imageBGR = np.empty((1088,1920,3), dtype=np.uint8)
camera.capture(imageBGR, 'bgr')

# write raw image to file
cv2.imwrite('rawImage.png',imageBGR)

# convert original image to rgb
imageRGB = cv2.cvtColor(imageBGR, cv2.COLOR_BGR2RGB)

if verbose:
    print('Segmenting image...')
# set color thresholds
bMin=0
bMax=255
gMin=0
gMax=255
rMin=210
rMax=255
minBGR = np.array([bMin, gMin, rMin])
maxBGR = np.array([bMax, gMax, rMax])

# use OpenCV inRange method to create a binary image based on the thresholds above
imageMask = cv2.inRange(imageBGR,minBGR,maxBGR) 

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
maxArea = 0

numContours = len(contours) # number of contours found
imageWithContours = imageRGB # make a copy of imageRGB to draw contours on
centroids = np.empty((numContours,2)) #initialize array to store centroids
counter = 0 # initialize a counter to count filtered contours
cntAreas = []

for thisContour in contours:
    area = cv2.contourArea(thisContour) # compute contour area using OpenCV
    cntAreas.append(area)
    if area > areaMin and area < areaMax:
        # draw current contour on image in red (255,0,0)
        imageWithContours = cv2.drawContours(imageWithContours, [thisContour], 0, (255,0,0), 3)
        # find the current contour moments and use them to centroid coordinates
        # google cv2.moments for more informatation
        M = cv2.moments(thisContour)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        centroids[counter] = [cx, cy] # add current centroid to the list
        counter=counter+1
        print('Coordinates of contour #{}: {},{}'.format(counter,cx,cy))
# print(centroids)

# try:
    # find max contour; first is a dud so moving on
    # biggestArea = min(cntAreas)
    # biggestBoy = cntAreas.index(biggestArea)
    # cntAreas.remove(biggestArea)
    # print(cntAreas)
   	 
    # biggestArea = min(cntAreas)
    # biggestBoy = cntAreas.index(biggestArea)
    # cntAreas.remove(biggestArea)
    # print(cntAreas)
    # bigArea = min(cntAreas)
    # bigBoy = cntAreas.index(bigArea)

# except:
    # pass

# if biggestBoy is not None and bigBoy is not None:
# print("Centroids are: ", centroids[biggestBoy], centroids[bigBoy])
# x1, y1, w1, h1 = cv2.boundingRect(contours[biggestBoy])
p1 = (int(centroids[0][0]), int(centroids[0][1]))
# x2, y2, w2, h2 = cv2.boundingRect(contours[bigBoy])
p2 = (int(centroids[1][0]), int(centroids[1][1]))
# p1 = (centroids[biggestBoy][0], centroids[biggestBoy][1])
# p2 = (centroids[bigBoy][0], centroids[bigBoy][1])
print("p1:", p1, "p2:", p2)	
imageWithContours = cv2.line(imageWithContours, p1, p2, color=(0, 255, 0), thickness=5)

imageWithContoursBGR = cv2.cvtColor(imageWithContours, cv2.COLOR_RGB2BGR)

	
# write imageWithCoutours to file
# first convert the image to BGR, which is the open cv standard format
# then save the image
cv2.imwrite('imageWithCountours.png',imageWithContoursBGR)
        
# display imageWithContours
if verbose:
    print('Preparing to display image...')
plt.imshow(imageWithContours)
print()
print('Displaying image, close image window to exit')
plt.show()

    
    
