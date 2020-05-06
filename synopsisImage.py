from image_selector import ImageSelector
import imagetool
import utiltool
from datetime import datetime
import face_detection
import cv2
from multiprocessing import Pool, Process, cpu_count, set_start_method
import random
import json
class Synopsis_Image:
    def __init__(self):
        super().__init__()


    # input : list of images path
    def extract_keyframe_for_videos(self, path, all_videos, image_selecter):
        
        videos_scene = []
        for i in range(0,len(all_videos)):
            scene_list = self.find_scene_boundary(path, all_videos[i], 0, len(all_videos[i]), 30)
            videos_scene.append(scene_list)
        for group in videos_scene:
            print(group)
        candidates_frames = []
        for i in range(0, len(videos_scene)):
            cur_video = all_videos[i]
            cur_video_scene = videos_scene[i]
            candidates_frames.extend(self.select_candidates(path, cur_video, cur_video_scene, 50))

        final_key_frames = []
        for cand in candidates_frames:
            frame_list, _ = image_selecter.select_best_frames(cand, 5) # can optimize with face detection
            # if 5 candidates have faces images, then pick one of them
            face_frames = []
            for frame in frame_list:
                face_nums = face_detection.detect_face(frame)
                if face_nums > 0 : face_frames.append(frame)
            
            if len(face_frames) > 0:
                frame_list, _ = image_selecter.select_best_frames(face_frames, 1)
            else:
                frame_list, _ = image_selecter.select_best_frames(frame_list, 1)
            
            for frame in frame_list:
                final_key_frames.append(frame)
        
        videos_scene, final_key_frames = self.video_postprocessing(videos_scene, final_key_frames)
        return videos_scene, final_key_frames

    def video_postprocessing(self, videos_scene, key_frames):
        print("---- Begin post-processing ----")
        final_videos_scene = []
        final_key_frames = []
        # case 1: compare(1, 3) if similar merge(1...3) otherwise compare(1, 2)
        offset = 0
        for video in videos_scene:
            i = 0
            cur_video_scene = []
            while (i < len(video)):
                 # each video frames scan neighbor and merge similar scene
                inc = 0
                if (i + 2 < len(video)):
                    cur_img = key_frames[i+offset]
                    next_img = key_frames[i+1+offset]
                    next2_img = key_frames[i+2+offset]
                    similar2 = imagetool.get_img_diff(cur_img, next2_img)
                    similar1 = imagetool.get_img_diff(cur_img, next_img)
                    print("similar1 {} similar2 {}".format(similar1, similar2))
                    if similar2 >= 0.4:
                        cur_video_scene.append([video[i][0], video[i+2][1]])
                        print("merge {} with {}".format(i+offset, i+2+offset))
                        inc = 3
                    elif similar1 >= 0.4:
                        cur_video_scene.append([video[i][0], video[i+1][1]])
                        print("merge {} with {}".format(i+offset, i+1+offset))
                        inc = 2
                    else:
                        cur_video_scene.append([video[i][0], video[i][1]])
                        inc = 1
                else:
                    cur_video_scene.append([video[i][0], video[i][1]])
                    inc = 1
                final_key_frames.append(key_frames[i+offset])
                i += inc
            final_videos_scene.append(cur_video_scene)
            offset += len(video)
        print(final_videos_scene)
        return final_videos_scene, final_key_frames
        

    def extract_key_framses_from_images(self, root, all_images_path, image_selecter):
        candidates_images = []
        candidates_name = []
        for path in all_images_path:
            img = imagetool.fast_readrgbfile(root+path)
            hasFace = face_detection.detect_face(img)
            if(hasFace or random.random() < 0.3):
                candidates_images.append(img)
                candidates_name.append(path)

        frame_list, index_list = image_selecter.select_best_frames(candidates_images, 10)
        final_images_name = []
        final_images = []
        index_list.sort()
        for i in index_list:
            final_images_name.append(candidates_name[i])
        for img_name in final_images_name:
            final_images.append(imagetool.fast_readrgbfile(root+img_name))
        return final_images_name, final_images

    def find_conner(self, path, cur_video, start, end):
        pre_img = imagetool.fast_readrgbfile(path+cur_video[start])
        pre_score = 1
        min_score = 1
        min_index = end
        for i in range(start+1, end+1):
            cur_img = imagetool.fast_readrgbfile(path+cur_video[i]) 
            cur_score = imagetool.get_img_diff(pre_img, cur_img)
            # print("Post-processing (img{}, img{}): {}".format(i-1, i, cur_score))
            if (min_score > cur_score):
                min_score = cur_score
                min_index = i-1
            pre_img = cur_img
            pre_score = cur_score
        return min_index


    """
    SHOT AND SCENE BOUNDARY DETECTION
    @ input: video, start frame, end frame, sliding window size
    @ output: scene range
    """
    def find_scene_boundary(self, path, cur_video, start, end, k):
        starttime = datetime.now()
        pre_img = imagetool.fast_readrgbfile(path+cur_video[start])
        pre_score = -1
        scene_list = []
        scene_start = 0
        scene_end = 0
        for i in range(start+k, end, k):
            cur_img = imagetool.fast_readrgbfile(path+cur_video[i]) 
            cur_score = imagetool.get_img_diff(pre_img, cur_img)
            print("Similarity score (img{}, img{}): {}".format(i-k, i, cur_score))
            if (k == 1):
                if (cur_score < 0.5):
                    scene_list.append([scene_start, i-1])
                    scene_start = i

            elif (pre_score != -1 and cur_score < 0.5 and abs(cur_score - pre_score) >= 0.2):
                scene_end = self.find_conner(path, cur_video, i-k, i)
                scene_list.append([scene_start, scene_end])
                scene_start = scene_end+1
                i = scene_start
                pre_img = imagetool.fast_readrgbfile(path+cur_video[i]) 
                pre_score = -1
                continue
            pre_img = cur_img
            pre_score = cur_score
        
        if (k > 1 and scene_end < end-1):
            scene_list.append([scene_start, end-1])
        print("Time: {}".format(datetime.now()-starttime))
        return scene_list
    

        # each scene select n candidates and then select one high quality key frame from candidates
    def select_candidates(self, path, cur_video, scene_list, n):
        candidates_list = []
        for scene in scene_list:
            candidates = []
            start = scene[0]
            end = scene[1]
            k = (end - start) // n+1 if end - start > n else 1
            for i in range(start, end+1, k):
                cand = imagetool.fast_readrgbfile(path + cur_video[i])
                num_of_faces = face_detection.detect_face(cand)
                if num_of_faces >= 1:
                    candidates.append(cand)
                elif random.random() <= 0.4:
                    candidates.append(cand)
                    
            candidates_list.append(candidates)
        
        return candidates_list

    def generateMetaData(self, candidates_videos, candidates_images):
        metadata = []
        for i in range(0, len(candidates_videos)):
            cur_video = candidates_videos[i]
            folder = "/TestData/video{}/".format(i+1)
            for frame in cur_video:
                metadata.append(utiltool.metadata_addvideo(folder, frame[0]+1, frame[1]+1, folder+"audio.wav"))
        for img in candidates_images:
            metadata.append( utiltool.metadata_addimage("/TestData/"+img))
        return metadata

if __name__ == "__main__":
    set_start_method('spawn')
    n_processes = cpu_count()
    pool_selector = Pool(n_processes)
    image_selecter = ImageSelector(pool_selector)
    my_synopsis = Synopsis_Image()


    path = "./TestData/"
    all_videos_name = []
    for i in range(1, 5):
        name = "video"+str(i)
        all_videos_name.append(utiltool.get_filelist(path, name))
    all_images_name = utiltool.get_filelist(path, "image")

    key_video_shots, key_video_frames = my_synopsis.extract_keyframe_for_videos(path, all_videos_name, image_selecter)
    key_images_name, key_images = my_synopsis.extract_key_framses_from_images(path, all_images_name, image_selecter)
    metadata = my_synopsis.generateMetaData(key_video_shots, key_images_name)
    with open('version_2.json', 'w') as json_file:
        json.dump(metadata, json_file)

    final_key_frames = key_video_frames + key_images
    res = imagetool.combine_rgbimages(final_key_frames)
    imagetool.savergbfile(res,len(final_key_frames), "version_2.rgb") #wed_synopsis
    cv2.imshow("synopsis", cv2.cvtColor(res, cv2.COLOR_RGB2BGR))
    cv2.waitKey (0)
    cv2.destroyAllWindows()