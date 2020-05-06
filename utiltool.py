import os
import imagetool
import cv2
import json
from PIL import Image, ImageOps, ImageFilter
from PIL import ImageEnhance
import imutils
import numpy as np

"""
@ Input: root folder path, and tag for video or images
@ Output: a list of list rgb filelist in each folder

This function aims to get all the rgb file in each sub folder.
And each folder's rgb file in a single list and return a list of list
e.g res[0]:include all rgb file in Video1
    res[1]:include all rgb file in Video2
"""
def get_filelist(folder_path, tag):
    res = []
    for root, dirs, files in os.walk(folder_path, topdown = False):
        if (tag in root):
            for file_name in files:
                if ".rgb" in file_name:
                    # path = os.path.join(root, file_name)
                    # res.append(path)
                    res.append(tag+"/"+file_name)
        res.sort()

    return res
    # for root, dirs, files in os.walk(folder_path, topdown = False):
    #     print(sorted(dirs))
    #     if tag == "video":
    #         cur_list = []
    #         if ("video" in root):
    #             for file_name in files:
    #                 if ".rgb" in file_name:
    #                     path = os.path.join(root, file_name)
    #                     cur_list.append(path)
    #             cur_list.sort()
    #             res.append(cur_list)
    #     else: 
    #         if ("image" in root):
    #             for file_name in files:
    #                 if ".rgb" in file_name:
    #                     path = os.path.join(root, file_name)
    #                     res.append(path)
    #             res.sort()

    # return res

def metadata_addvideo(folder_name, start_frame, end_frame, audio_file):
    videodict = {}
    videodict["tp"] = 1
    videodict["folder"] = folder_name
    videodict["start"] = start_frame
    videodict["end"] = end_frame
    videodict["audio"] = audio_file
    return videodict

def metadata_addimage(file_name):
    imagedict = {}
    imagedict["tp"] = 0
    imagedict["path"] = file_name
    return imagedict

# metadata = []
# for i in range(5):
#     metadata.append( metadata_addvideo("../../576RGBVideo1/", 1, 100,"../../video_1.wav") )
#     metadata.append( metadata_addvideo("../../576RGBVideo2/", 1, 100,"../../video_2.wav") )
#     metadata.append( metadata_addvideo("../../576RGBVideo3/", 1, 90,"../../video_3.wav") )
#     metadata.append( metadata_addvideo("../../576RGBVideo4/", 1, 100,"../../video_4.wav") )
#     metadata.append( metadata_addimage("../../Image/RGB/image-0003.rgb") )
# #metajson = json.dumps(metadata)
# with open('metadata.json', 'w') as json_file:
#   json.dump(metadata, json_file)
# #print(metajson)


if __name__ == "__main__":
    # img = imagetool.fast_readrgbfile("wed_synopsis.rgb", 352*15, 288)
    # img = Image.fromarray(img, mode = None)
    img = Image.open('before-processing.png')
    for i in range(1, 15):
        cropped_image = img.crop((352*i-15, 0, 352*i+15, 288))
        blur = cropped_image.filter(ImageFilter.GaussianBlur(radius = 3))
        img.paste(blur, (352*i-15, 0, 352*i+15, 288))
    
    width, height = img.size
    sharp = ImageEnhance.Sharpness(img).enhance(1.5)
    contrast = ImageEnhance.Contrast(sharp).enhance(1.5)
    out = ImageOps.expand(contrast, (5, 20), fill='white')

    finial_img = out.resize((width, height),Image.ANTIALIAS)
    finial_img.show()
    finial_img.save("after-processing.png")
    img = cv2.imread("after-processing.png")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imagetool.savergbfile(img, 15, "wed_synopsis.rgb")
    pass

    
