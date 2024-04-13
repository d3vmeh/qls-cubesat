import cv2
import numpy as np
import math
import matplotlib.pyplot as plt


def show_ratios(img,rects,ratios):
    i = 0
    for rect in rects:
        x = rect[0][0]
        y = rect[0][1]
        width = rect[1][0] - rect[0][0]
        height = rect[1][1] - rect[0][1]
        centerx = int(x+width/2)
        centery = int(y + height/2)
        img = cv2.putText(img, str(round(ratios[i]*100,1)), (x, centery), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
        i += 1
    return img



def make_rects(img,rect_width,rect_height):
    img_width = img.shape[1]
    img_height = img.shape[0]

    x = 0
    y = 0
    
    x1 = 0
    y1 = 0

    rects = []
    while x<img_width:
        x1 = x + rect_width
        while y<img_height:
            y1 = y + rect_height
            rect = [[x,y],[x1,y1]]
            rects.append(rect)
            y = y1
        y = 0
        x = x1 
    return rects


def draw_rects(img,rects):

    for rect in rects:
        img = cv2.rectangle(img, rect[0], rect[1], (255,0,0), 1)

    
    return img

def get_amount_white(img,rects):
    ratios = []
    for rect in rects:
        rect_width = rect[1][0]-rect[0][0]
        rect_height = rect[1][1]-rect[0][1]

        rect_x = rect[0][0]
        rect_y = rect[0][1]

        img_area = img[rect_y:rect_y+rect_height,rect_x:rect_x+rect_width]
        
        r = np.array(img_area)

        num_white = 0
        num_black = 0

        num = 0
        for p in r:
            for z in p:
                num += 1
                if z == 255:
                    num_white += 1
                else:
                    num_black += 1

        if num_black != 0:
            ratios.append(num_white/num_black)
        else:
            ratios.append(0.99)
        
    return ratios


def highlight_rects(rects,difference,before_img,after_img,before_ratios,after_ratios,
                    show_text=False,text_scale = 0.9, text_thickness = 2):
    i = 0
    
    for rect in rects:
        before_ratio = before_ratios[i]
        after_ratio = after_ratios[i]


        if show_text == True:
            x = rect[0][0]
            y = rect[0][1]
            height = rect[1][1] - rect[0][1]
            centery = int(y + height/2)
            before_img = cv2.putText(before_img, str(round(before_ratios[i]*100,1)), 
                                     (x, centery), cv2.FONT_HERSHEY_SIMPLEX, 
                                     text_scale, (36,255,12), text_thickness)
            after_img = cv2.putText(after_img, str(round(after_ratios[i]*100,1)), 
                                    (x, centery), cv2.FONT_HERSHEY_SIMPLEX, 
                                    text_scale, (36,255,12), text_thickness)
        
        
        
        if before_ratio-difference<after_ratio:
            before_img = cv2.rectangle(before_img, rect[0], rect[1], (255,0,0), 1)
            after_img = cv2.rectangle(after_img, rect[0], rect[1], (255,0,0), 1)

        elif before_ratio-difference>after_ratio:
            before_img = cv2.rectangle(before_img, rect[0], rect[1], (0,0,255), 4)
            after_img = cv2.rectangle(after_img, rect[0], rect[1], (0,0,255), 4)

        i += 1
    return before_img, after_img



#Converting images to black-and-white
thresh = 180
before_path = "images/houstonbefore.png"
before_colored = cv2.imread(before_path)
before_img = cv2.imread(before_path, cv2.IMREAD_GRAYSCALE)

after_path = "images/houstonafter.png"
after_colored = cv2.imread(after_path)
after_img = cv2.imread(after_path,cv2.IMREAD_GRAYSCALE)
after_bw = cv2.threshold(after_img, thresh, 255, cv2.THRESH_BINARY)[1]


before_img = cv2.resize(before_img,after_img.shape[::-1])
before_colored = cv2.resize(before_colored,after_img.shape[::-1])

before_bw = cv2.threshold(before_img, thresh, 255, cv2.THRESH_BINARY)[1]


#Dividing images into rectangles
rects = make_rects(before_bw,30,30)
before_drawn = draw_rects(before_bw,rects)
after_drawn = draw_rects(after_bw,rects)


#Get pixel ratios
before_ratios = get_amount_white(before_drawn,rects)
after_ratios = get_amount_white(after_drawn,rects)

ratio_difference = 0.15
final_before, final_after = highlight_rects(rects,ratio_difference,before_colored,after_colored,before_ratios,after_ratios,show_text = True, text_scale = 0.4, text_thickness= 1)


#Showing before and after images side-by-side
comparison_bw = np.concatenate((before_bw, after_bw), axis=1) 

comparison_color = np.concatenate((final_before,final_after),axis = 1)

cv2.imshow('Black-and-white: Before (left) VS After (right)', comparison_bw) 
cv2.imshow("Before (left) VS After (right)",comparison_color)

cv2.waitKey(0) 
cv2.destroyAllWindows() 
