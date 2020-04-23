import numpy as np
from PIL import Image

#imag = cv2.imread("image-0006.jpg")
#print(imag)
#cv2.imshow("test",imag)

#############################################################################
##
## a function read a rgb file and output an 3darray
## only use numpy and pillow is only used to form image, show and save
##
#############################################################################

def readrgbfile(filename):

	file = open(filename,"rb")
	byte = file.read(1)
	arr = []
	while byte:
		a = int.from_bytes(byte, byteorder = "big")
		arr.append(a)
		byte = file.read(1)
	file.close()

	arr = np.array(arr, dtype=np.uint8)
	arr3d = arr.reshape((3, 288, 352)).transpose()
	arr3d = arr3d.transpose(1,0,2)
	new_img = Image.fromarray(arr3d, mode = None)
	#new_img.show()
	return arr3d

#names = []
#for root, firs, files in os.walk("../576RGBVideo1", topdown = False):
#	for name in files:
#		if ".rgb" in name:
#			names.append(name)
#names.sort()

#for name in names:
#	readrgbfile("../576RGBVideo1/"+name)
#	print(name)
#	break;
