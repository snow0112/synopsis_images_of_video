# import the necessary packages
from skimage.measure import compare_ssim
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import peak_signal_noise_ratio as psnr
import numpy as np
from PIL import Image
# import argparse
# import imutils
import cv2
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
    grayA = cv2.cvtColor(imageA, cv2.COLOR_RGB2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_RGB2GRAY)

    # compute the Structural Similarity Index (SSIM) between the two
    # images, ensuring that the difference image is returned
    (score_ssim, diff) = ssim(grayA, grayB, gaussian_weightsbool=True, full=True)
    # print(diff)
    # compute the Histogram feasure between the two images [0, 1]
    # hist1 = cv2.calcHist([grayA], [0], None, [256], [0.0,255.0]) 
    # hist2 = cv2.calcHist([grayB], [0], None, [256], [0.0,255.0]) 
    hist1 = cv2.calcHist([imageA], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    hist2 = cv2.calcHist([imageB], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    score_hist = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)

    score = 0.7 * score_ssim + 0.3 * score_hist
    return score


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
	return arr3d

def fast_readrgbfile(filename, width = 352, height = 288):
	f = open(filename,"rb")
	image_bytes = f.read()
	decoded = np.fromstring(image_bytes, dtype=np.uint8)
	arr3d = decoded.reshape((3, height, width)).transpose().transpose(1,0,2)
	return arr3d

def rgb2png(filename, width = 352, height = 288):
	arr3d = readrgbfile(filename, width, height)
	new_img = Image.fromarray(arr3d, mode = None)
	new_img.save(filename[:-3] + "png")


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
			new_img = Image.fromarray(readrgbfile(foldername+filename) )
			synopsis = get_concat_h(synopsis, new_img)
		else:
			synopsis = Image.fromarray(readrgbfile(foldername+filename) )

	arr3d = np.array(synopsis)
	savergbfile(arr3d, len(filelist))

	#synopsis.save("test_synopis.png")
	
def combine_rgbimages(image_list):
	synopsis = None
	for img in image_list:
		if synopsis:
			new_img = Image.fromarray(img)
			synopsis = get_concat_h(synopsis, new_img)
		else:
			synopsis = Image.fromarray(img)
	return np.array(synopsis)

	
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
	# file = open("test-MySynopsis.rgb", "wb")
	file = open("test.rgb", "wb")
	binary_format = bytearray(arr)
	file.write(binary_format)
	file.close()
    
def readrgbtoQImage(fileName, width = 352, height = 288):
    arr3d = fast_readrgbfile(fileName, width =  width)
    bytesPerLine = 3*width
    img = QImage(arr3d.tobytes(), width, height, bytesPerLine, QImage.Format_RGB888)
    return img


def writeRGBToJPG(rgbPath, jpgPath): 
    img = readrgbfile(rgbPath)
    cv2.imwrite(jpgPath, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))

def rgb2gif(foldername, start_frame, end_frame, save_name):
	array = []
	for num in range(start_frame, end_frame):
		fileName = "image-"+str(num).zfill(4)+".rgb"
		arr3d = readrgbfile(foldername+fileName)
		img = Image.fromarray(arr3d, mode = None)
		array.append(img)
	array[0].save(save_name, save_all = True, append_images = array[1:], duration = 1000/30, loop = 0 )

def rgb2avi(foldername, start_frame, end_frame, save_name):
	array = []
	for num in range(start_frame, end_frame):
		fileName = "image-"+str(num).zfill(4)+".rgb"
		arr3d = readrgbfile(foldername+fileName)
		img = Image.fromarray(arr3d, mode = None)
		array.append(img.convert('RGB') )
	#array.astype(np.float32)

	out = cv2.VideoWriter('test.avi', 0,1,(352,288))
	for i in range(len(array)):
		out.write(array[i])
	out.release()


# if __name__ == "__main__":
	# foldername = "../../576RGBVideo1/"
	# for num in range(1, 100):
	# 	filename = "image-"+str(num).zfill(4)+".rgb"
	# 	rgb2png(foldername+filename)


# images = []
# p = 0
# for i in range(1,1501,100):
# 	images.append(fast_readrgbfile("../../576RGBVideo1/"+"image-"+str(i).zfill(4)+".rgb"))
# 	p+=1
# arr3d = combine_rgbimages(images)
# savergbfile(arr3d,p)
# print(p)