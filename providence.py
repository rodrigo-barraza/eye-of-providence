import os
import time
import shutil
import sys
import getopt
from memery.core import Memery
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
memery = Memery()
currentIteration = 0
cpuCount = os.cpu_count()

# Indexing
# python "/mnt/c/develop/eye-of-providence/providence.py" --mode "index" --input "/mnt/c/AI/training/datasets/rodrigography2"
# Moving
# python /mnt/c/develop/eye-of-providence/providence.py --mode "move" --query "cat" --input "/mnt/c/Users/rodrigo/Desktop/photosnew" --output "/mnt/c/Users/rodrigo/Desktop/photossorted" --amount "2000" --reindex "false"
# Copying
# python providence.py --mode "copy" --query "portrait" --input "/mnt/c/AI/training/datasets/raw-set2" --output "/mnt/c/AI/training/datasets/sorting" --reindex "false"
# Sorting
# python "/mnt/c/develop/eye-of-providence/providence.py" --mode "sort" --query "colorful girl" --input "/mnt/c/AI/training/datasets/curated" --reindex "false"

# Command Line Arguments
argv = sys.argv[1:]

try:
    options, args = getopt.getopt(argv, "m:q:iq:i:o:a:r", ["mode=", "query=", "image_query=", "input=", "output=", "amount=", "reindex="])
except:
    print("No Arguments?")

# Options
mode = "index" # "index", "sort", "move", "copy"
query = None
imageQuery = None
inputDirectory = None
outputDirectory = None
amount = None # only needed for mode "move"
reindex = False # do you want to index every time?

for name, value in options:
    if name in ['-m', '--mode']:
        mode = value
    elif name in ['-q', '--query']:
        query = value
    elif name in ['-iq', '--image_query']:
        imageQuery = value
    elif name in ['-i', '--input']:
        inputDirectory = value
    elif name in ['-o', '--output']:
        outputDirectory = value
    elif name in ['-a', '--amount']:
        amount = int(value)
    elif name in ['-r', '--reindex']:
        reindex = value.lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']

if reindex and mode != "index":
    memery.clean(inputDirectory)
    memery.index_flow(inputDirectory, cpuCount)

if mode == "index":
    print(f"Indexing all images in {inputDirectory} ...")
    memery.clean(inputDirectory)
    memery.index_flow(inputDirectory, cpuCount)
    print("... FINISHED INDEX")
elif mode != "index":
    imagePaths = memery.query_flow(inputDirectory, query, imageQuery)
    if mode == "sort":
        print(f"Sorting all images and .txt files in {inputDirectory} ...")
        for imagePath in imagePaths:
            txtPath = os.path.splitext(imagePath)[0]+'.txt'
            currentIteration = currentIteration + 1
            countDown = len(imagePaths) - currentIteration
            print(countDown)
            imagePathWithoutImageDirectory = imagePath.replace(inputDirectory, "")
            if os.path.exists(imagePath):
                os.utime(imagePath, (int(time.time()) + currentIteration , int(time.time()) + currentIteration ))
            if os.path.exists(txtPath):
                os.utime(txtPath, (int(time.time()) + currentIteration , int(time.time()) + currentIteration ))
        print("... FINISHED SORT")
    if mode == "copy":
        print(f"Copying and sorting all images and .txt files from {inputDirectory} to {outputDirectory} ...")
        for imagePath in imagePaths:
            txtPath = os.path.splitext(imagePath)[0]+'.txt'
            currentIteration = currentIteration + 1
            countDown = len(imagePaths) - currentIteration
            print(countDown)
            imagePathWithoutImageDirectory = imagePath.replace(inputDirectory, "")
            newImagePath = outputDirectory + imagePathWithoutImageDirectory
            textPathWithoutDirectory = txtPath.replace(inputDirectory, "")
            newTextPath = outputDirectory + textPathWithoutDirectory
            if os.path.exists(imagePath):
                if not os.path.exists(outputDirectory):
                    os.mkdir(outputDirectory)
                shutil.copyfile(imagePath, newImagePath)
                if os.path.exists(txtPath):
                    shutil.copyfile(txtPath, newTextPath)
        print("... FINISHED COPY")
    elif mode == "move":
        print(f"Moving and sorting {amount} images and .txt files from {inputDirectory} to {outputDirectory} ...")
        for imagePath in imagePaths[:amount]:
            txtPath = os.path.splitext(imagePath)[0]+'.txt'
            currentIteration = currentIteration + 1
            countDown = amount - currentIteration
            imagePathWithoutImageDirectory = imagePath.replace(inputDirectory, "")
            newImagePath = outputDirectory + imagePathWithoutImageDirectory
            textPathWithoutDirectory = txtPath.replace(inputDirectory, "")
            newTextPath = outputDirectory + textPathWithoutDirectory
            if os.path.exists(imagePath):
                if not os.path.exists(outputDirectory):
                    os.mkdir(outputDirectory)
                shutil.move(imagePath, newImagePath)
                os.utime(newImagePath, (int(time.time()) , int(time.time()) ))
                print(countDown, newImagePath)
                if os.path.exists(txtPath):
                    shutil.move(txtPath, newTextPath)
                    os.utime(newTextPath, (int(time.time()) , int(time.time()) ))
                    print(countDown, newTextPath)
        print("... FINISHED MOVE")