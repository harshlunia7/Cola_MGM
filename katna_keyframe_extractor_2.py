from Katna.video import Video
from Katna.writer import KeyFrameDiskWriter
import os
import ntpath
from moviepy.editor import VideoFileClip
import glob
import math 

def get_video_duration(file_path):
    try:
        video = VideoFileClip(file_path)
        duration = video.duration
        video.close()
        return duration
    except Exception as e:
        print("Error:", e)
        return None

if __name__ == "__main__":
    categories = ['igniting', 'walking', 'kicking', 'neutral']
    for category in categories:
        print(f"Processing Category: {category}")
        
        videos_dir = f"./videos/{category}"
        videos = glob.glob(os.path.join(videos_dir, "./*mp4"))
        
        output_dir = f"extracted_frames/{category}"
        os.makedirs(output_dir, exist_ok=True)

        gt_record_file = open(os.path.join(output_dir, "gt.txt"), "w")
        gt_record_file.write(f"input_video_file_path\tvideo_duration\tno_of_frames_extracted\textracted_frame_location\tcategory\n")

        vd = Video()
        
        for video_file_path in videos:
            video_name = video_file_path.split('/')[-1].split('.')[0]

            os.makedirs(os.path.join(output_dir, video_name), exist_ok=True)
            diskwriter = KeyFrameDiskWriter(location=os.path.join(output_dir, video_name))
            print(f"Input video file path = {video_file_path}")
            try:
                video_duration = get_video_duration(video_file_path)
                no_of_frames_to_returned = math.ceil(video_duration / 5)
                vd.extract_video_keyframes(
                    no_of_frames=no_of_frames_to_returned, file_path=video_file_path,
                    writer=diskwriter
                )
            except:
                print(f"Some Issue with video {video_file_path}")
                os.system(f"rm -rf {os.path.join(output_dir, video_name)}")
                continue
            gt_record_file.write(f"{video_file_path}\t{video_duration}\t{no_of_frames_to_returned}\t{os.path.join(output_dir, video_name)}\t{category}\n")
        gt_record_file.close()