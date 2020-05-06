import os
import cv2
import imagetool
import utiltool
import numpy as np
from datetime import datetime


from image_selector import ImageSelector
from multiprocessing import Pool, Process, cpu_count, set_start_method

"""
Test 1: test get all rgb files function, save result in list of list
@ path: CSCI576ProjectMedia folder position
@ list_of_list: all the rgb files in each folder
"""
def test_getall_rgbfiles(path):
    return utiltool.get_filelist(path)


"""
Test 2: test get two images difference using Structural Similarity Measure method
The score can fall into the range [-1, 1] with a value of one being a “perfect match”.
"""
def test_get_similar_scores(path1, path2): 
    img1 = imagetool.readrgbfile(path1)
    img2 = imagetool.readrgbfile(path2)
    score = imagetool.get_img_diff(img2, img1)
    cv2.imshow("img1", cv2.cvtColor(img1, cv2.COLOR_RGB2BGR))
    cv2.imshow("img2", cv2.cvtColor(img2, cv2.COLOR_RGB2BGR))
    print("Similar score: {}".format(score))
    cv2.waitKey (0)
    cv2.destroyAllWindows()


def find_conner(cur_video, start, end):
    pre_img = imagetool.readrgbfile(cur_video[start])
    pre_score = 1
    min_score = 1
    min_index = end
    for i in range(start+1, end+1):
        cur_img = imagetool.readrgbfile(cur_video[i]) 
        cur_score = imagetool.get_img_diff(pre_img, cur_img)
        # print("Post-processing (img{}, img{}): {}".format(i-1, i, cur_score))
        if (min_score > cur_score):
            min_score = cur_score
            min_index = i-1
        pre_img = cur_img
        pre_score = cur_score
    return min_index


"""
Test 3  SHOT AND SCENE BOUNDARY DETECTION
@ input: video, start frame, end frame, sliding window size
@ output: scene range
"""
def find_scene_boundary(cur_video, start, end, k):
    starttime = datetime.now()
    pre_img = imagetool.readrgbfile(cur_video[start])
    pre_score = -1
    scene_list = []
    scene_start = 0
    for i in range(start+k, end, k):
        cur_img = imagetool.readrgbfile(cur_video[i]) 
        cur_score = imagetool.get_img_diff(pre_img, cur_img)
        print("Similarity score (img{}, img{}): {}".format(i-k, i, cur_score))
        if (pre_score != -1 and cur_score < 0.5 and abs(cur_score - pre_score) >= 0.2):
            scene_end = find_conner(cur_video, i-k, i)
            scene_list.append([scene_start, scene_end])
            scene_start = scene_end+1
            i = scene_start
            pre_img = imagetool.readrgbfile(cur_video[i]) 
            pre_score = -1
            continue
        pre_img = cur_img
        pre_score = cur_score
    if (scene_end < end-1):
        scene_list.append([scene_start, end-1])
    print("Time: {}".format(datetime.now()-starttime))
    return scene_list

# each scene select n candidates and then select one high quality key frame from candidates
def select_candidates(cur_video, scene_list, n):
    candidates_list = []
    for scene in scene_list:
        candidates = []
        start = scene[0]
        end = scene[1]
        k = (end - start) // n+1 if end - start > n else 1
        for i in range(start, end+1, k):
            cand = imagetool.readrgbfile(cur_video[i])
            candidates.append(cand)
        candidates_list.append(candidates)
    
    return candidates_list        


if __name__ == "__main__":
    # # set_start_method('spawn')
    # # n_processes = cpu_count()
    # # pool_selector = Pool(n_processes)

    # list_of_list = test_getall_rgbfiles("/Users/luckyjustin/Documents/JustinProject/576Project/CSCI576ProjectMedia")
    
    # cur_video = list_of_list[0]
    # starttime = datetime.now()

    # # img = imagetool.fast_readrgbfile(cur_video[1])
    # for i in range(0 , 1):
    #     img = imagetool.fast_readrgbfile(cur_video[i])
    # # res = map(imagetool.fast_readrgbfile, cur_video[0:30])
    # # reslist = list(res)
    # print("Time: {}".format(datetime.now()-starttime))
    # # cv2.imshow("img", cv2.cvtColor(img, cv2.COLOR_RGB2BGR))

    # # cv2.waitKey (0)
    # # cv2.destroyAllWindows()

    # videos_scene = []
    # videos_scene.append([[0, 44], [45, 387], [388, 594], [595, 854], [855, 991], [992, 1283], [1284, 1392], [1393, 1450], [1451, 1790], [1791, 2260], [2261, 2453], [2454, 2551]])
    # videos_scene.append([[0, 128], [129, 485], [486, 2971]])
    # videos_scene.append([[0, 97], [98, 453], [454, 1078], [1079, 1520], [1521, 1771]])
    # videos_scene.append([[0, 192], [193, 496], [497, 754], [755, 1407], [1408, 1801]])

    # candidates_frames = []
    # for i in range(0, len(videos_scene)):
    #     print("****** Start select {} video candidate frames ******".format(i))
    #     cur_video = list_of_list[i]
    #     cur_video_scene = videos_scene[i]
    #     candidates_frames.extend(select_candidates(cur_video, cur_video_scene, 10))
    #     print("-----Finish select {} video candidate frames------".format(i))

    # print("****** Start select key frames ******")
    # image_selecter = ImageSelector(pool_selector)
    # final_key_frames = []
    # for cand in candidates_frames:
    #     frame_list = image_selecter.select_best_frames(cand, 1)
    #     for frame in frame_list:
    #         final_key_frames.append(frame)
    # res = imagetool.combine_rgbimages(final_key_frames)
    # print("----- Finish select key frames ------")
    # cv2.imshow("synopsis", cv2.cvtColor(res, cv2.COLOR_RGB2BGR))
    # cv2.waitKey (0)
    # cv2.destroyAllWindows()

    # pool_selector.close()
    # pool_selector.join()
    # i = 0
    # for frame in top_frames:
    #     cv2.imshow("img"+str(i), cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
    #     i = i + 1

    # cv2.waitKey (0)
    # cv2.destroyAllWindows()
    # print(len(top_frames))
    # for i in range(0, len(cur_video)):
    #     imagetool.writeRGBToJPG(cur_video[i], "video4/" + str(i) + '.jpg')
    #     print(i)
    path = "./TestData/"
    all_videos_name = []
    for i in range(1, 5):
        name = "video"+str(i)
        all_videos_name.append(utiltool.get_filelist(path, name))
    test_get_similar_scores(path+all_videos_name[1][700], path+all_videos_name[1][750])
    # print(all_videos_name[1])
    # res = find_scene_boundary(cur_video, 0, len(cur_video), 5)
    # print(res)

