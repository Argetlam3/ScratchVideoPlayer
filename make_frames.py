import cv2
import os

def extract_frames(video_path, output_folder, start_frame=1, limit=150):  # Scratch's limit is 150 frames at 10 resolution
    """
    Extracts frames from a video and saves them as individual images.

    Args:
        video_path (str): Path to the video file.
        output_folder (str): Path to the folder where frames will be saved.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    video_capture = cv2.VideoCapture(video_path)
    frame_count = 0
    [video_capture.read() for _ in range(start_frame)]  # Read the first frame to remove thumbnail

    success, image = video_capture.read()

    while success and frame_count < limit:
        cv2.imwrite(os.path.join(output_folder, f"frame_{frame_count:06d}.jpg"), image)
        success, image = video_capture.read()
        frame_count += 1
    
    video_capture.release()
    print(f"Extracted {frame_count} frames to {output_folder}")

if __name__ == "__main__":
    # Example usage
    video_file = r"C:\Users\name\Desktop\frame-gen\big_buck_bunny.mp4"
    frames_folder = os.path.dirname(__file__) + "/images/"
    extract_frames(video_file, frames_folder, start_frame=20, limit=500)
