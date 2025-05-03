import make_frames
import make_data
import os
import numpy as np
from collections import Counter

def main():
    video_path = input("Enter the path to the video file: ")
    output_folder = input("Enter the output folder for frames: ")
    start_frame = int(input("Enter the start frame number: "))
    limit = input("Enter the limit for frames (or all for all): ")
    if limit.lower() == "all":
        limit = float("inf")  # Set to infinity to extract all frames
    else:
        limit = int(limit)

    make_frames.extract_frames(video_path, output_folder, start_frame, limit)

    resolution = int(input("Enter the resolution (default is 10): "))

    print("Extracting hex codes from images...")
    if not os.path.exists(output_folder):
        print("Output folder does not exist. Please check the path.")
        return
    
    if resolution <= 0:
        resolution = 10

    image_folder = output_folder
    hex_arrays = []
    colors = []

    for file in list(os.walk(image_folder))[0][2]:
            
            hex_array = make_data.get_hex_codes(image_folder + file, resolution=resolution)
            hex_arrays.append(hex_array)

    color_counter = Counter()
    for hex_array in hex_arrays:
        for row in hex_array:
            color_counter.update(row)

    most_common_colors = color_counter.most_common(200000)  # Get the 256 most common colors
    colors = [color[0] for color in most_common_colors]
    colors = np.array(colors)  # Convert to numpy array for easier manipulation


    make_data.save(resolution, hex_arrays, colors)
    print("Hex codes and colors saved successfully.")

if __name__ == "__main__":
    main()
