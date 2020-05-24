import cv2
import numpy as np
import os
import pandas as pd
import Image
from PIL import ImageFilter
from pytesseract import image_to_string
from Tkinter import *
import random

directory = 'train'
drawing = False # true if mouse is pressed
ix,iy,fx,fy = -1,-1,-1,-1

# mouse callback function
def draw(event,x,y,flags,param):
    global ix,iy,fx,fy,drawing,potential_sequence

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        fx, fy = x, y
        crop_img = img[iy:y, ix:x]
        potential_sequence = image_to_string(crop_img) + '\n'
        print(potential_sequence)

# process based on tesseract
data = []
potential_sequence = ''
sequence = ''
fles = os.listdir('./{0}'.format(directory))
fle = fles.pop(0)
img = cv2.imread('{0}/{1}'.format(directory, fle), 0)
done = False

while(1):
    
    if done: # check if the operation has been cancelled
        break 

    cv2.namedWindow('image')
    cv2.setMouseCallback('image', draw)
    cv2.imshow('image',img)

    k = cv2.waitKey(1) & 0xFF
    if k == ord('n'):
        print(sequence)
        if sequence != '':
            data.append((fle, sequence[:-2]))
        try:
            fle = fles.pop(0)
            img = cv2.imread('{0}/{1}'.format(directory, fle), 0)
        except:
            done = True
        sequence = ''
    elif k == ord('s'):
        sequence = sequence + potential_sequence + '\n'
        potential_sequence = ''
        cv2.rectangle(img,(ix,iy),(fx,fy),(random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)),2)
        ix,iy,fx,fy = -1,-1,-1,-1
    elif k == 27:
        done = True
        break

df = pd.DataFrame(data, columns=["files", "text"])
df.to_csv("howdy.csv".format(directory),index=False, encoding ='utf-8')
cv2.destroyAllWindows()