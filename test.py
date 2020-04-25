import os
import cv2
import imagetool
import utiltool

if __name__ == "__main__":

    """
    Test 1: test get all rgb files function, save result in list of list
    """
    path = "/Users/luckyjustin/Documents/JustinProject/576Project/CSCI576ProjectMedia"
    list_of_list = utiltool.get_filelist(path)
    # print(list_of_list)


    """
    Test 2: test get two images difference using Structural Similarity Measure method
    The score can fall into the range [-1, 1] with a value of one being a “perfect match”.
    """
    img1 = imagetool.readrgbfile(list_of_list[0][0])
    img2 = imagetool.readrgbfile(list_of_list[0][1])
    (score, diff) = imagetool.get_img_diff(img2, img1)
    cv2.imshow("img1", img1)
    cv2.imshow("img2", img1)
    print("SSIM: {}".format(score))
    cv2.waitKey (0)
    cv2.destroyAllWindows()