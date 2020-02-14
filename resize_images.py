# USAGE
# python resize_images.py --folder dataset --max-size 800

# %%
# import the necessary packages
from imutils import paths
import argparse
import cv2
import os


# %%
def image_resize(image, width, height, inter=cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # calculate the resize ratio and keep aspect
    r = min(height/float(h), width/float(w))
    dim = (int(w*r), int(h*r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation=inter)
    # return the resized image
    return resized


# %%
def resize_images(inputFolder, outputFolder, maxSize):
  imagePaths = list(paths.list_images(inputFolder))
  # loop over the image paths
  for (i, imagePath) in enumerate(imagePaths):
    # load the input image and convert it from RGB (OpenCV ordering)
    # to dlib ordering (RGB)
    print("[INFO] processing image {}/{}".format(i + 1, len(imagePaths)))
    print(imagePath)
    image = cv2.imread(imagePath)
    resized = image_resize(image, maxSize, maxSize)

    relpath = os.path.relpath(imagePath, inputFolder)
    newPath = os.path.join(outputFolder, relpath)
    print(newPath)
    os.makedirs(os.path.dirname(newPath), exist_ok=True)
    cv2.imwrite(newPath, resized)


# %%
if __name__ == "__main__":
  # construct the argument parser and parse the arguments
  ap = argparse.ArgumentParser()
  ap.add_argument("-i", "--input", required=True,
    help="path to input directory of images")
  ap.add_argument("-o", "--output", required=True,
    help="path to output directory of images")
  ap.add_argument("-s", "--size", type=int, required=True,
    help="max width and height after resizing the image")
  args = vars(ap.parse_args())

  resize_images(args["input"], args["output"], args["size"])
