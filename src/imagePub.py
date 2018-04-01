#!/usr/bin/env python
import cv2
import numpy as np
import time
import rospy
import Soccer
from std_msgs.msg import Bool

try:
	index = sys.argv[1]
except:
	index = 1



cap = cv2.VideoCapture(index)
y,u,v = 0,99,50
kernel = np.ones((5,5),np.uint8)

width = cap.get(3)
height= cap.get(4)
area = 0
flag = 1
iter = 180
abc = 1
#cv2.namedWindow("Masking")
#cv2.namedWindow("YUV")
def detect():

	global cap,y,u,v,kernel,width,height,flag,area,iter,abc
	
	while flag:
		
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
          		#return True
			x1,y1 = width/2,height/2
			#if x<x1+100 and x>x1-100 and y<y1+100 and y>y1-100 : 
				#print "detected"
			abc = 0
			return True
			
			'''else:
				return False
			
			
			print "area: ",area," ","x: ",x," ","y: ",y	
			'''

		else:
			'''if abc:
				if iter>0:
					head.pan_right_to_left()
				

				else:
					head.pan_left_to_right()
					if iter == -179:
						iter = 180
				
				iter -= 2
			'''
			cv2.imshow("Masking",mask)
			cv2.imshow("YUV",frame)
			return False
		

	


class Head(object) :
	def __init__(self,dxl) :
		self.pan = 19
		self.pan_ang = 90
		self.tilt = 20
		self.dxl = dxl
		self.prev_ang = 0
	
	def dxl_pan_write(self,write) :
		self.dxl.angleWrite(self.pan,write)

	def dxl_tilt_write(self,write) :
		self.dxl.angleWrite(self.tilt,write)
 
	def pan_left_to_right(self,pan=2.0) :
		self.dxl_pan_write(self.pan_ang)
		time.sleep(0.001)
		self.pan_ang += pan		
		return self.pan_ang

	def pan_right_to_left(self,pan=2.0) :
		self.dxl_pan_write(self.pan_ang)
		time.sleep(0.001) 
		self.pan_ang -= pan
		return self.pan_ang


def talker() :

	pub=rospy.Publisher('detect',Bool,queue_size=10)
	rospy.init_node('talker',anonymous=True) 
	rate=rospy.Rate(10)

	while not rospy.is_shutdown() :
		msg = detect()
		pub.publish(msg)


if __name__=="__main__" :
	try :
		#dxl = Soccer.Dynamixel(lock=20)
		#head = Head(dxl)
		talker()
	except rospy.ROSInterruptException :
		cap.release()
		cv2.destroyAllWindows()





