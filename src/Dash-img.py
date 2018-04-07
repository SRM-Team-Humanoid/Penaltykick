#!/usr/bin/env python
import cv2
import numpy as np
import time
import rospy
from std_msgs.msg import String
y,u,v = 0,117,59
kernel = np.ones((5,5),np.uint8)
cap = cv2.VideoCapture(1)
x =360
width = cap.get(3)
height= cap.get(4)
flag1 = True
area = 0
def getArea() :
	move="nothing"
	global x,y,flag1
	global cap,y,u,v,kernel,width,height,flag,area,iter,abc
	y1,u,v = 0,99,50#[105, 117, 113]
	#flag1=True
	t=time.time()
	rec=True
	area1=0
	while rec:
		ret,frame = cap.read()

		img_yuv = cv2.cvtColor(frame,cv2.COLOR_BGR2YUV)
		mask = cv2.inRange(img_yuv, (np.array([0,u-25,v-25])), (np.array([255,u+25,v+25])))

		
		erode = cv2.erode(mask,kernel,iterations = 1)
		dilate = cv2.dilate(erode,kernel,iterations = 1)

		
		erode = cv2.erode(mask,kernel,iterations = 1)
		dilate = cv2.dilate(erode,kernel,iterations = 1)	

		image,contour,hierarchy = cv2.findContours(dilate,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		
		if cv2.waitKey(1) == 27:
			flag = 0
		 

		
		if contour :
			#cnt = contour[0]
			cnt = max(contour, key = cv2.contourArea)		#getting contour with max area
			(x,y),radius = cv2.minEnclosingCircle(cnt)		#calculating center of the ball
			x,y,radius = int(x),int(y),int(radius)
			cv2.circle(frame,(x,y),radius,(0,255,0),2)		#drawing circle across contour

			area = radius*radius*3.14
			cv2.imshow("Masking",mask)
			cv2.imshow("YUV",frame)


		
		if x>340+120 :
			move = "right"

		elif x<300-120 :
			move = "left"

		else:

			if flag1 and area<15000:
				move = "forward"
			else:
				flag1=False
				move = "stop"
			area1=area
		# print move
		if cv2.waitKey(1) == 27:
			break
		print area1
                return move



def talker() :
	#msg=raw_input()
	pub=rospy.Publisher('get_area',String,queue_size=10)
	rospy.init_node('talker',anonymous=True) 
	rate=rospy.Rate(10)

	while not rospy.is_shutdown() :
		msg = getArea()
		pub.publish(msg)
                time.sleep(0.1)

if __name__=="__main__" :
	try :
		talker()
	except rospy.ROSInterruptException :
		pass
