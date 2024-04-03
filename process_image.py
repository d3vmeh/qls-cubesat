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
    x1 = 0

    y = 0
    y1 = 0

    rects = []
    while x<img_width:
        x1 = x + rect_width
        while y<img_height:
            y1 = y + rect_height
            #print(x,y,x1,y1)
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
        ratios.append(num_white/num_black)
        
    return ratios

def highlight_rects(rects,difference,before_img,after_img,before_ratios,after_ratios):
    i = 0
    
    for rect in rects:
        before_ratio = before_ratios[i]
        after_ratio = after_ratios[i]

        i += 1

        if before_ratio-difference<after_ratio:
            before_img = cv2.rectangle(before_img, rect[0], rect[1], (255,0,0), 1)
            after_img = cv2.rectangle(after_img, rect[0], rect[1], (255,0,0), 1)

        elif before_ratio-difference>after_ratio:
            before_img = cv2.rectangle(before_img, rect[0], rect[1], (0,0,255), 4)
            after_img = cv2.rectangle(after_img, rect[0], rect[1], (0,0,255), 4)

       

    return before_img, after_img

    
before_path = "/Users/devm2/Documents/Cubesat/testing/beforealbany.png"
before_colored = cv2.imread(before_path)
before_img = cv2.imread(before_path, cv2.IMREAD_GRAYSCALE)

thresh = 50

after_path = "/Users/devm2/Documents/Cubesat/testing/afteralbany.png"
after_colored = cv2.imread(after_path)
after_img = cv2.imread(after_path,cv2.IMREAD_GRAYSCALE)
after_bw = cv2.threshold(after_img, thresh, 255, cv2.THRESH_BINARY)[1]


before_img = cv2.resize(before_img,after_img.shape[::-1])
before_colored = cv2.resize(before_colored,after_img.shape[::-1])

before_bw = cv2.threshold(before_img, thresh, 255, cv2.THRESH_BINARY)[1]





rects = make_rects(before_bw,100,100)

before_drawn = draw_rects(before_bw,rects)
after_drawn = draw_rects(after_bw,rects)



#cv2.imshow("image",before_bw)





before_ratios = get_amount_white(before_drawn,rects)
after_ratios = get_amount_white(after_drawn,rects)


final_before, final_after = highlight_rects(rects,0.004,before_colored,after_colored,before_ratios,after_ratios)

before_bw2 = cv2.threshold(before_img, thresh, 255, cv2.THRESH_BINARY)[1]
after_bw2 = after_bw
before_bw2, after_bw2 = highlight_rects(rects,0.3,before_bw2,after_bw2,before_ratios,after_ratios)




Hori = np.concatenate((show_ratios(final_before,rects,before_ratios), show_ratios(final_after,rects,after_ratios)), axis=1) 
#Hori = np.concatenate((before_bw, after_bw), axis=1) 
# concatenate image Vertically 
#Verti = np.concatenate((before_bw2, after_bw2), axis=0) 



# cv2.imshow("image",i)


cv2.imshow('HORIZONTAL', Hori) 
#cv2.imshow('VERTICAL', Verti)






cv2.waitKey(0) 
  
# # closing all open windows 
cv2.destroyAllWindows() 