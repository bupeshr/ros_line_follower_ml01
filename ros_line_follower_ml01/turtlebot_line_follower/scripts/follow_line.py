#!/usr/bin/env python3

"""
Line follower robot with RGB camera, I'm using Turtlebot3 Waffle pi in this project

Author: Bupesh Rethinam Veeraiah

"""

import rospy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
import cv2, cv_bridge
import numpy as np


class Color_line_follower:
    # intializing the necessary variables 
    def __init__(self):
        self.image_sub = rospy.Subscriber("/camera/rgb/image_raw",Image, self.camera_1)
        self.cmd_pub = rospy.Publisher("/cmd_vel", Twist, queue_size = 1)
        self.bridge = cv_bridge.CvBridge()
        self.twist = Twist()
        self.lower_color = np.array([20,100,100])
        self.upper_color = np.array([30,255,255])
        # print("init")

    # callback function of the subscriber
    def camera_1(self, msg):
        image = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8") #Using CvBridge converting ros image to cv2 image
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)                    #converting the RGB image to hsv image for color detection
        mask =cv2.inRange(hsv,self.lower_color, self.upper_color)       #masking the color 
        kernel = np.ones((5,5),np.uint8)
        mask = cv2.erode(mask,kernel,iterations=2)                      
        m= cv2.moments(mask)                                            

        if m['m00']>0:
            cx = int(m['m10']/m['m00'])
            cy = int(m['m01']/m['m00'])

            # Drawing rectangle and circle in the line detected
            x, y, w, h = cv2.boundingRect(mask)
            cv2.rectangle(image, (x,y),((x+w),(y+h)),(250,140,150),3)
            cv2.circle(image, (cx,cy),3,(255,0,255),2) 

            #error calculation
            error = cx - image.shape[1]/2
            # print(self.error)

            # velocity values when line is detected
            self.twist.linear.x = 0.5
            self.twist.angular.z= -(error/100)
            self.cmd_pub.publish(self.twist)
        
        # print("camera")
        cv2.imshow("Output", image)
        cv2.imshow("masked", mask)
        cv2.waitKey(2)


rospy.init_node("rethens_ranger", anonymous= True)
follower = Color_line_follower()
rospy.spin()
# print("every time")
