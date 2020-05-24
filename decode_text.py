import Image
from PIL import ImageFilter
from pytesseract import image_to_string

import numpy as np
import cv2

img = cv2.imread('/home/cjv/Documents/relatix.io/train/best bumble messages-15.JPEG')

# scale the image
img = cv2.resize(img, (300,500), interpolation = cv2.INTER_AREA)

# remove noise
blur = cv2.blur(img,(5,5))
edges = cv2.Canny(blur,20,30)

# first find edges and thicken them
contours,h = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

for cnt in contours:
    cv2.drawContours(edges,[cnt],0,(255,255,0),thickness=2)

# turn edges into shapes
contours,h = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

for cnt in contours:
    cv2.drawContours(edges,[cnt],0,(255,255,0),thickness=cv2.FILLED)

#extract the shapes
contours,h = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

for cnt in contours:
    approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
    if 5 < len(approx) < 10:
        x,y,w,h = cv2.boundingRect(cnt)
        img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

cv2.imshow('img',img)
cv2.imshow('edge',edges)
cv2.waitKey(0)
cv2.destroyAllWindows()