"""
generate a 360x480 array of hex codes from an image
"""

from PIL import Image
import os
import numpy as np

# Counter
from collections import Counter

def get_hex_codes(image_path, resolution=1):
    global colors
    assert 480 % resolution == 0, "Res must be a factor of 480 and 360"
    assert 360 % resolution == 0, "Res must be a factor of 480 and 360"
    
    """
    Retrieves an array of hexadecimal color codes from an image.

    Args:
        image_path: Path to the image file.

    Returns:
        A list of lists, where each inner list represents a row of pixels
        and contains the hexadecimal color codes for that pixel.
    """
    img = Image.open(image_path)
    img = img.convert("RGB").resize((int(480/resolution), int(360/resolution)))  # Ensure the image is in RGB format
    width, height = img.size
    hex_codes = []

    for y in range(int(height)):
        row_codes = []
        for x in range(int(width)):
            r, g, b = img.getpixel((x, y))
            hex_code = '#{:02x}{:02x}{:02x}'.format(r, g, b)
            
            # Compress the hex code
            hex_code = hex_code.replace("#", "")  # Remove the '#' character
            hex_code = int(hex_code, 16)  # Convert hex to int

            row_codes.append(hex_code)
        hex_codes.append(row_codes)
    return hex_codes, colors

resolution = 10
image_folder = os.path.dirname(__file__) + "/images/"
hex_arrays = []
colors = []

print(list(os.walk(image_folder))[0])
for file in list(os.walk(image_folder))[0][2]:
    print(file)
    """if not file.endswith((".jpg", ".jfif", ".png", ".JPG", ".jpeg")):
        continue"""
    hex_array, _ = get_hex_codes(image_folder + file, resolution=resolution)
    hex_arrays.append(hex_array)

color_counter = Counter()
for hex_array in hex_arrays:
    for row in hex_array:
        color_counter.update(row)

most_common_colors = color_counter.most_common(200000)  # Get the 256 most common colors
colors = [color[0] for color in most_common_colors]
colors = np.array(colors)  # Convert to numpy array for easier manipulation


with open(f"hexes_res_{resolution}.txt", "w") as f:
    for hex_array in hex_arrays:
        for row in hex_array:
            for color in row:
                if color in colors:
                    f.write("!" + str(np.where(colors == color)[0][0]))  # Get the index of the color in the most common colors
                    print("found color", color, "at index", np.where(colors == color)[0][0])
                else:
                    f.write("." + str(color))
                # ! if it's an index in the colors, . if it's not

                f.write(" ")
            f.write("-")
        f.write("\n")

with open(f"hexes_res_{resolution}_cs.txt", "w") as f:
    for color in colors:
        f.write(str(color))
        f.write("\n")