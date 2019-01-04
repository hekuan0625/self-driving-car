import cv2
import matplotlib.pyplot as plt
import numpy as np

def canny(image):
	gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

	blur = cv2.GaussianBlur(gray, (5,5), 0)
	canny = cv2.Canny(blur, 20, 80)
	return canny

def ROI(image):
	mask = np.zeros_like(image)
	vertices = np.array([[(200, image.shape[0]), 
		                  (1100, image.shape[0]), 
		                  (550, 250)]])
	cv2.fillPoly(mask, vertices, 255)
	crop_image = cv2.bitwise_and(image, mask)
	return crop_image


image = cv2.imread('image/test_image.jpg')
canny_image = canny(image)
roi_image = ROI(canny_image)

lines = cv2.HoughLinesP(roi_image, 2, np.pi/180, 100, minLineLength = 40, maxLineGap = 5)
if lines is not None:
	for line in lines:
		x1, y1, x2, y2 = line.reshape(4)
		cv2.line(image, (x1,y1), (x2,y2), (255, 0, 0), 3)


cv2.imshow('result', image)
cv2.waitKey(0)


