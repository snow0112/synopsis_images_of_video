import os
import imagetool
import cv2
import json

"""
@ Input: root folder path 
@ Output: a list of list rgb filelist in each folder

This function aims to get all the rgb file in each sub folder.
And each folder's rgb file in a single list and return a list of list
e.g listoflist[0]:include all rgb file in 576RGBVideo1
    listoflist[1]:include all rgb file in 576RGBVideo2
"""
def get_filelist(folder_path):
    listoflist = []
    for root, dirs, files in os.walk(folder_path, topdown = False):
        cur_list = []
        if ("576RGBVideo" in root):
            for file_name in files:
                if ".rgb" in file_name:
                    path = os.path.join(root, file_name)
                    cur_list.append(path)
            cur_list.sort()
            listoflist.append(cur_list)

    return listoflist

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

metadata = []
metadata.append( metadata_addvideo("../../576RGBVideo1/", 1, 100,"../../video_1.wav") )
metadata.append( metadata_addvideo("../../576RGBVideo2/", 1, 100,"../../video_2.wav") )
metadata.append( metadata_addimage("../../Image/RGB/image-0003.rgb") )
#metajson = json.dumps(metadata)
with open('metadata.txt', 'w') as json_file:
  json.dump(metadata, json_file)
#print(metajson)


# if __name__ == "__main__":
#     path = "/Users/luckyjustin/Documents/JustinProject/576Project/CSCI576ProjectMedia"
#     list_of_list = get_filelist(path)
#     testimage = list_of_list[0][0]
#     img = readrgb.readrgbfile(testimage)
#     cv2.imshow("Image", img) 
#     cv2.waitKey (0)
#     cv2.destroyAllWindows()
    # print(img)

