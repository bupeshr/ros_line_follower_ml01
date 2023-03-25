import cv2 

import numpy

image = cv2.imread("/home/bupesh/motion_ws/src/ros_line_follower_ml01/turtlebot_line_follower/resources/track.png") 
lower_yellow = numpy.array([20, 100, 100])  # Lower range of yellow color in HSV format
upper_yellow = numpy.array([30, 255, 255]) 
mask = cv2.inRange(image, lower_yellow, upper_yellow)
print("lower: ",lower_yellow)
print("-------------------------------------")
print("upper: ", upper_yellow)


detected_output = cv2.bitwise_and(image, image, mask =  mask) 

cv2.imshow("red color detection", image) 
cv2.imshow("output detection", detected_output) 

cv2.waitKey(0)
