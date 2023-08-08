import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from PIL import Image

x = np.arange(0, 47)

#here is actual data of amount of green hama beads from pictures. These curve was presented with color of green
y = np.array([0, 0, 5, 10, 15, 20, 25, 30, 35, 39, 41, 41, 43, 45, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100,
              105, 110, 115, 120, 125, 130, 135, 140, 144, 149, 154, 159, 163, 165, 165, 165, 165, 165, 165, 155, 155])

#this will hold amount of wanted pixels from each picture
count = np.array([])

#insert location of folder where images reside. Now empty, since project is unfinished
files = os.listdir(r"<folder path here>")

#Filtering only the files.
files = [f for f in files if f.endswith("jpg")]

#this is to count progress, since code doesn't change image size, so progressing one image takes lot of time
j = 1

#looping of images from folder. JPG-image is open with Pillow, transformed to Numpy array, transforming values from RBG to HSV,
# and eventually certain greens are counted together and stored in count-nparray
for i in files:
   img = np.array(Image.open(fr"<folder path here>\{i}"))
   img_array = img.reshape(len(img)*len(img[0]),3)
   img_hsv = img_array/[255, 255, 255]
   img_hsv = colors.rgb_to_hsv(img_hsv)
   img_hsv = (img_hsv*[360, 100, 100]).astype(int)
   #this here limits colors for 'certain greens'. Once gui is created, change these to be adjustable.
   c = (np.logical_and(img_hsv[:, 0] >= 150, img_hsv[:, 0] <= 170)) & (np.logical_and(
    img_hsv[:, 1] > 45, img_hsv[:, 1] < 85)) & (np.logical_and(img_hsv[:, 2] < 50, img_hsv[:, 2] > 15))
   count = np.append(count, np.sum(c))
   #this here is to help follow the progress of operation. Needs to be changed
   print(f"{j}/47")
   j += 1

#apparently one hama bead pictured from above from certaing height is about 6000 pixels in size, so need to reduce counted amount
count = (count / 6000).astype(int)

plt.plot(x,y, 'g')
plt.plot(x,count, 'r')
plt.show()
