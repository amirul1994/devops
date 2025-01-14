from moviepy.editor import VideoFileClip
import os


def get_video_duration(file_path):
    try:
        clip = VideoFileClip(file_path)
        return clip.duration
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return 0  # Return 0 duration for videos with errors


def accumulated_runtime(video_folder):
    total_duration = 0
    for filename in os.listdir(video_folder):
        if filename.endswith(
                ".mp4"):  # Adjust the file extension as needed
            file_path = os.path.join(video_folder, filename)
            total_duration += get_video_duration(file_path)

    return total_duration


# Example usage:
folder_path = "E:/needed_dsa/Newfolder"
total_runtime = accumulated_runtime(folder_path)
print(f"Total Accumulated Runtime: {total_runtime} seconds")
