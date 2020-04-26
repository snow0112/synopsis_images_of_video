# import the necessary packages
from skimage.measure import compare_ssim
import numpy as np
from PIL import Image
# import argparse
#import imutils
#import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *

"""
* The score: represents the structural similarity index between the two input images. 
    This value can fall into the range [-1, 1] with a value of one being a “perfect match”.
* The diff:  contains the actual image differences between the two input images 
"""
def get_img_diff(imageA, imageB):
    # convert the images to grayscale
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

    # compute the Structural Similarity Index (SSIM) between the two
    # images, ensuring that the difference image is returned
    (score, diff) = compare_ssim(grayA, grayB, full=True)
    # diff = (diff * 255).astype("uint8")
    return score, diff


"""
readrgbfile is a function read a rgb file and output an 3darray
only use numpy and pillow is only used to form image, show and save
combine_rgbfile is a function combine rgb files from a list
"""


def readrgbfile(filename, width = 352, height = 288):

	file = open(filename,"rb")
	byte = file.read(1)
	arr = []
	while byte:
		a = int.from_bytes(byte, byteorder = "big")
		arr.append(a)
		byte = file.read(1)
	file.close()
	arr = np.array(arr, dtype=np.uint8)	
	arr3d = arr.reshape((3, height, width)).transpose()
	#print(arr3d.shape)
	arr3d = arr3d.transpose(1,0,2)
	#print(arr3d.shape)
	# new_img = Image.fromarray(arr3d, mode = None)
	# new_img.save("test_synopis.png")
	#new_img.show()
	return arr3d

def get_concat_h(im1, im2):
	#print(im1.width)
	dst = Image.new('RGB', (im1.width + im2.width, im1.height))
	dst.paste(im1, (0, 0))
	dst.paste(im2, (im1.width, 0))
	return dst

def combine_rgbfiles(foldername, filelist):

	synopsis = None

	for filename in filelist:
		if synopsis:
			new_img = Image.fromarray( readrgbfile(foldername+filename) )
			synopsis = get_concat_h(synopsis, new_img)
		else:
			synopsis = Image.fromarray( readrgbfile(foldername+filename) )

	arr3d = np.array(synopsis)
	savergbfile(arr3d, len(filelist))

	#synopsis.save("test_synopis.png")
	

def savergbfile(arr3d, w):
	#print("save file")
	print(arr3d.shape)
	arr3d = arr3d.transpose(1,0,2)
	print(arr3d.shape)
	arr3d = arr3d.transpose()
	print(arr3d.shape)
	totallength = 304128*w
	arr = arr3d.reshape((totallength,))
	#print(arr.shape)
	#print(arr[:10])
	file = open("test-MySynopsis.rgb", "wb")
	binary_format = bytearray(arr)
	file.write(binary_format)
	file.close()


def readrgbtoQImage(fileName, width = 352, height = 288):
    arr3d = readrgbfile(fileName, width =  width)
    img = QImage(width, height, QImage.Format_RGB32)
    for x in range(width):
        for y in range(height):
            value = qRgb(arr3d[y][x][0], arr3d[y][x][1], arr3d[y][x][2] )
            img.setPixel( x, y , value )
    return img