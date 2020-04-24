import numpy as np
from PIL import Image

#imag = cv2.imread("image-0006.jpg")
#print(imag)
#cv2.imshow("test",imag)

#############################################################################
##
## readrgbfile is a function read a rgb file and output an 3darray
## only use numpy and pillow is only used to form image, show and save
##
## combine_rgbfile is a function combine rgb files from a list
##
#############################################################################

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
	#print(arr.shape)
	

	arr3d = arr.reshape((3, height, width)).transpose()
	#print(arr3d.shape)
	arr3d = arr3d.transpose(1,0,2)
	#print(arr3d.shape)
	new_img = Image.fromarray(arr3d, mode = None)
	new_img.save("test_synopis.png")
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


#filelist = ["image-0001.rgb", "image-0300.rgb", "image-0600.rgb", "image-0900.rgb", "image-1200.rgb"]
#combine_rgbfiles("../576RGBVideo1/", filelist)

#arr3d = readrgbfile("image-0006.rgb")
#savergbfile(arr3d)
#readrgbfile("test-MySynopsis.rgb", width = 352*5)


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
