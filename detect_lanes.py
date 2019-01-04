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

def make_coordinates(image, parameter):
	hight = image.shape[0]
	y1 = hight
	y2 = int(y1 * 2.1 / 5)
	x1 = int((y1 - parameter[1]) / parameter[0])
	x2 = int((y2 - parameter[1]) / parameter[0])
	return np.array([x1, y1, x2, y2])


image = cv2.imread('image/test_image.jpg')
canny_image = canny(image)
roi_image = ROI(canny_image)

lines = cv2.HoughLinesP(roi_image, 2, np.pi/180, 100, minLineLength = 40, maxLineGap = 5)
if lines is not None:
	left_lines = []
	right_lines = []
	for line in lines:
		x1, y1, x2, y2 = line.reshape(4)
		parameters = np.polyfit((x1, x2), (y1,y2), 1)
		if parameters[0] < 0:
			left_lines.append(parameters)
		else:
			right_lines.append(parameters)

	left_para = np.average(left_lines, axis = 0)
	right_para = np.average(right_lines, axis = 0)
	para_list = [left_para, right_para]
  

    #lines_average = [make_coordinates(image, left_para), make_coordinates(image, right_para)]
if para_list is not None:
    for para in para_list:
    	[x1, y1, x2, y2] = make_coordinates(image, para)
    	cv2.line(image, (x1, y1), (x2, y2), (255, 0, 0), 4)


cv2.imshow('result', image)
cv2.waitKey(0)


