import os
import time
from PIL import Image


currentIteration = 0
currentTime = int(time.time())

def get_image_paths(directory="."):
    image_extensions = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif", ".webp")
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.lower().endswith(image_extensions)]

def get_total_pixels(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
    return width * height

# Get image paths in the current directory
image_paths = get_image_paths()

# Sort image paths by total pixels
sorted_image_paths = sorted(image_paths, key=get_total_pixels)

print(f"Sorting all images")
for imagePath in sorted_image_paths:
    txtPath = os.path.splitext(imagePath)[0]+'.txt'
    currentIteration += 1
    countDown = len(sorted_image_paths) - currentIteration
    print(countDown)
    if os.path.exists(imagePath):
        os.utime(imagePath, (currentTime + currentIteration , currentTime + currentIteration ))
    if os.path.exists(txtPath):
        os.utime(txtPath, (currentTime + currentIteration , currentTime + currentIteration ))
print("... FINISHED SORT")