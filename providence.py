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

# Moving
# python providence.py --mode "move" --query "aesthetic portrait" --input "/mnt/c/Users/rodrigo/Desktop/photosnew" --output "/mnt/c/Users/rodrigo/Desktop/photossorted" --amount "200" --cache "true"
# python providence.py --mode "move" --query "aesthetic orange" --input "/mnt/c/AI/training/datasets/raw-set2" --output "/mnt/c/AI/training/datasets/sorting-set2" --amount "200" --cache "true"
# .
# Copying
# python providence.py --mode "copy" --query "portrait" --input "/mnt/c/AI/training/datasets/raw-set2" --output "/mnt/c/AI/training/datasets/sorting" --cache "true"
# Sorting
# python providence.py --mode "sort" --query "aesthetic portrait" --input "/mnt/c/Users/rodrigo/Desktop/photosnew" --cache "true"

# Command Line Arguments
argv = sys.argv[1:]

try:
    options, args = getopt.getopt(argv, "m:q:i:o:a:c", ["mode=", "query=", "input=", "output=", "amount=", "cache="])
except:
    print("No Arguments?")

# Options
mode = "move" # "sort", "move", "copy"
imageQuery = "wow"
# inputDirectory = "/mnt/c/AI/training/datasets/raw-mix"
inputDirectory = "/mnt/c/AI/training/datasets/raw-set1"
outputDirectory = "/mnt/c/AI/training/datasets/sorting"
amount = 1 # only needed for mode "move"
cache = True # do you want to index every time?

for name, value in options:
    if name in ['-m', '--mode']:
        mode = value
    elif name in ['-q', '--query']:
        imageQuery = value
    elif name in ['-i', '--input']:
        inputDirectory = value
    elif name in ['-o', '--output']:
        outputDirectory = value
    elif name in ['-a', '--amount']:
        amount = int(value)
    elif name in ['-c', '--cache']:
        cache = value.lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']

if not cache:
    memery.clean(inputDirectory)
    memery.index_flow(inputDirectory, cpuCount)

imagePaths = memery.query_flow(inputDirectory, imageQuery)
if mode == "sort":
    print(f"Sorting all images and .txt files in {inputDirectory} ...")
    for imagePath in imagePaths:
        txtPath = os.path.splitext(imagePath)[0]+'.txt'
        currentIteration = currentIteration + 1
        countDown = len(imagePaths) - currentIteration
        print(countDown)
        imagePathWithoutImageDirectory = imagePath.replace(inputDirectory, "")
        if os.path.exists(imagePath):
            os.utime(imagePath, (int(time.time()) , int(time.time()) ))
        if os.path.exists(txtPath):
            os.utime(txtPath, (int(time.time()) , int(time.time()) ))
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
        print(txtPath)
        currentIteration = currentIteration + 1
        countDown = amount - currentIteration
        imagePathWithoutImageDirectory = imagePath.replace(inputDirectory, "")
        newImagePath = outputDirectory + imagePathWithoutImageDirectory
        textPathWithoutDirectory = txtPath.replace(inputDirectory, "")
        newTextPath = outputDirectory + textPathWithoutDirectory
        print(countDown, imagePathWithoutImageDirectory)
        if os.path.exists(imagePath):
            if not os.path.exists(outputDirectory):
                os.mkdir(outputDirectory)
            shutil.move(imagePath, newImagePath)
            os.utime(newImagePath, (int(time.time()) , int(time.time()) ))
            if os.path.exists(txtPath):
                shutil.move(txtPath, newTextPath)
                os.utime(newTextPath, (int(time.time()) , int(time.time()) ))
    print("... FINISHED MOVE")