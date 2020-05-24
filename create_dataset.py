import cv2
import numpy as np
import random
import csv

def create_text():
    ''' generates text between 1-200 chars '''

    CHAR_LST = "abcdefghijklnmopqrstuvwxyzABCDEFGHIJKLNMOPQRSTUVWXYZ0123456789\n,':?!"
    POS_LST = "LR" # either the left person or right sends

    text_len = random.randint(1, 100)
    pos = POS_LST[random.randint(0, 1)]

    text = ''
    for i in range(text_len): # generate a unique character for each pos in string
        if i % 25 == 0 and i != 0: # every 25 chars insert break
            text += '\n'
        else:
            text += CHAR_LST[random.randint(0,len(CHAR_LST) - 1)]
    return text, pos

def rounded_rectangle(src, top_left, bottom_right, radius=1, color=255, thickness=1, line_type=cv2.LINE_AA):
    ''' creates a rounded rectangle '''

    #  corners:
    #  p1 - p2
    #  |     |
    #  p4 - p3

    p1 = top_left
    p2 = (bottom_right[0], top_left[1])
    p3 = bottom_right
    p4 = (top_left[0], bottom_right[1])

    height = abs(bottom_right[0] - top_left[1])

    if radius > 1:
        radius = 1

    corner_radius = int(radius * (height/2))

    if thickness < 0:

        #big rect
        top_left_main_rect = (int(p1[0] + corner_radius), int(p1[1]))
        bottom_right_main_rect = (int(p3[0] - corner_radius), int(p3[1]))

        top_left_rect_left = (int(p1[0]), int(p1[1] + corner_radius))
        bottom_right_rect_left = (int(p4[0] + corner_radius), int(p4[1] - corner_radius))

        top_left_rect_right = (int(p2[0] - corner_radius), int(p2[1] + corner_radius))
        bottom_right_rect_right = (int(p3[0]), int(p3[1] - corner_radius))

        all_rects = [
        [top_left_main_rect, bottom_right_main_rect], 
        [top_left_rect_left, bottom_right_rect_left], 
        [top_left_rect_right, bottom_right_rect_right]]

        [cv2.rectangle(src, rect[0], rect[1], color, thickness) for rect in all_rects]

    # draw straight lines
    cv2.line(src, (int(p1[0] + corner_radius), int(p1[1])), (int(p2[0] - corner_radius), int(p2[1])), color, abs(thickness), line_type)
    cv2.line(src, (int(p2[0]), int(p2[1] + corner_radius)), (int(p3[0]), int(p3[1] - corner_radius)), color, abs(thickness), line_type)
    cv2.line(src, (int(p3[0] - corner_radius), int(p4[1])), (int(p4[0] + corner_radius), int(p3[1])), color, abs(thickness), line_type)
    cv2.line(src, (int(p4[0]), int(p4[1] - corner_radius)), (int(p1[0]), int(p1[1] + corner_radius)), color, abs(thickness), line_type)

    # draw arcs
    cv2.ellipse(src, (int(p1[0] + corner_radius), int(p1[1] + corner_radius)), (corner_radius, corner_radius), 180.0, 0, 90, color ,thickness, line_type)
    cv2.ellipse(src, (int(p2[0] - corner_radius), int(p2[1] + corner_radius)), (corner_radius, corner_radius), 270.0, 0, 90, color , thickness, line_type)
    cv2.ellipse(src, (int(p3[0] - corner_radius), int(p3[1] - corner_radius)), (corner_radius, corner_radius), 0.0, 0, 90,   color , thickness, line_type)
    cv2.ellipse(src, (int(p4[0] + corner_radius), int(p4[1] - corner_radius)), (corner_radius, corner_radius), 90.0, 0, 90,  color , thickness, line_type)

    return src

def put_text( img, text_arr, pos_arr ):
    ''' puts the text on the img '''
    
    FONT = cv2.FONT_HERSHEY_SIMPLEX 
    FONT_SCALE = 0.5
    FONT_THICKNESS = 1
    IMG_WIDTH = 400

    color_combo_dic = {
        'light': ( (232,232,232), (0,0,0) ),
        'dark': ( (254,139,42), (255,255,255) )
    }

    padding = random.randint(15, 25)
    l = random.randint(40, 60) # distance from the L message to the L border
    r = random.randint(40, 60) # distance from the R message to the R border
    
    dy = 20 # line height
    y = random.randint(100, 150) # distance to the top 

    for text, pos in zip(text_arr, pos_arr): # iterate over both lsts

        max_label_width = 0 # width of the text
        height = 0 # height of the text
        color_combo = color_combo_dic[random.choice(['light', 'dark'])] # color palette of this message

        for i, line in enumerate(text.split('\n')): # first create the blob
            
            (label_width, label_height), baseline = cv2.getTextSize(line, FONT, FONT_SCALE, FONT_THICKNESS)
            if label_width > max_label_width:
                max_label_width = label_width
            height += (label_height + dy / 2)

        if pos == 'L':
            x = l
        if pos == 'R':
            x = IMG_WIDTH - (r + max_label_width)
        
        height += padding
        max_label_width += padding

        rounded_rectangle(img, (x - (padding // 2), y - (padding // 2)), ( x + max_label_width, y + height), color=color_combo[0], radius=0.15, thickness=-1) # draw the rectangle

        for i, line in enumerate(text.split('\n')): # handle the new lines
            y += dy
            cv2.putText(img, line, (x, y), FONT, FONT_SCALE, color_combo[1], FONT_THICKNESS, cv2.LINE_AA) 

        y += random.randint(50, 70) # variance in spacing between texts

def create_background():
    ''' returns an image with a background template '''
    IMG_WIDTH = 400
    IMG_HEIGHT = 600
    background_num = random.randint(1, 8)

    raw_img = cv2.imread('img_templates/background_{0}.png'.format(background_num))
    return cv2.resize(raw_img, (IMG_WIDTH,IMG_HEIGHT))

def main(i):
    ''' creates the img and saves '''
    
    texts_num = random.randint(1, 3) # how many texts will be sent
    img = create_background()
    
    text_arr = [] # holds the string of texts
    pos_arr = [] # holds which side the texts are on
    for text in range(texts_num):
        text, pos = create_text()
        text_arr.append(text), pos_arr.append(pos)

    put_text( img, text_arr, pos_arr )
    directory = 'test'
    fle = 'tinder-{0}.png'.format(i)
    cv2.imwrite('{0}/{1}'.format(directory, fle), img)

    with open('test.csv', 'a') as csvfile: # appends in case of error
        fieldnames = ['file','text']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'file': fle, 'text': '\n'.join(text_arr) })

imgs = 10000
for i in range(imgs): # create img_num of text images
    main(i)
    print(i)