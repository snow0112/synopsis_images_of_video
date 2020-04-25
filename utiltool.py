import os
import imagetool
import cv2

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





# if __name__ == "__main__":
#     path = "/Users/luckyjustin/Documents/JustinProject/576Project/CSCI576ProjectMedia"
#     list_of_list = get_filelist(path)
#     testimage = list_of_list[0][0]
#     img = readrgb.readrgbfile(testimage)
#     cv2.imshow("Image", img) 
#     cv2.waitKey (0)
#     cv2.destroyAllWindows()
    # print(img)

