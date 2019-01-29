from Tkinter import *
from PIL import Image, ImageTk
import numpy as np
import os
import pickle
import sys
import config
import test_config

os.makedirs('Test')
mainfolder='Test'

def make_videos_of_frames(i):

    dir = 'Videos'
    fid = os.path.join(mainfolder,'images_'+str(i))
    str_command = 'ffmpeg -r 12 -y -i ' + os.path.join(fid, 'img_%08d.png') + ' ' + os.path.join(dir,'video_' + str(i) + '.mp4')

    os.system(str_command)

    str_command = 'rm -rf ' + os.path.join(fid,'current_image.eps')

    os.system(str_command)

    return True


#create tcl handle
window = Tk()

#create canvas
width = config.width
height = config.height

canvas = Canvas(window, width = width, height = height,highlightthickness=0)
canvas.pack(expand=YES, fill=BOTH)

#create_road_background_image
rimg = Image.open('roadimage.jpg')
rimg = rimg.resize((width,height), Image.ANTIALIAS)

road_img = ImageTk.PhotoImage(rimg)


canvas.create_image(0, 0, image=road_img, anchor=NW)


dx = 1
dy = 0

list_colors = ["white", "black", "red", "green", "blue", "cyan", "yellow", "magenta"]

anom_count = 0

vid=0
list_shapes_ltor=[]
list_shapes_rtol=[]

anom_prob = test_config.anom_prob



while(anom_count<test_config.anom_count):
    i=0
    list_ltor=[]
    list_rtol=[]

    sublist_shapes_ltor=[]
    sublist_shapes_rtol=[]

    # create queue of shapes in -x and +x direction to be moved across screen
    for j in range(0,test_config.n_shapes_in_video):

        # Left to Right queue
        if(j==0):
            x1ltor_c = -(22*(j+1))
            x2ltor_c = x1ltor_c+20
        else:
            x2ltor_c = x1ltor_old - np.random.randint(4,20)*1
            x1ltor_c = x2ltor_c-20

        y1 = config.y1ltor
        y2 = config.y2ltor

        rand_color = list_colors[np.random.randint(0,len(list_colors))]

        x1ltor_old = x1ltor_c

        if(np.random.rand() > anom_prob):
            #append square
            list_ltor.append(canvas.create_rectangle(x1ltor_c, y1, x2ltor_c, y2, fill=rand_color, tag='ltor_'+str(j)))
            sublist_shapes_ltor.append(['square_'+rand_color,x1ltor_c,x2ltor_c])
        else:
            #append triangle
            anom_count+=1
            sublist_shapes_ltor.append(['triangle_' + rand_color, x1ltor_c, x2ltor_c])
            list_ltor.append(canvas.create_polygon((x1ltor_c+x2ltor_c)/2.0, y1, x1ltor_c, y2, x2ltor_c,y2, fill=rand_color, tag='ltor_' + str(j)))

        #Right to Left queue
        if(j==0):
            x2rtol_c = 138 + ((j + 1) * 22)
            x1rtol_c = x2rtol_c-20
        else:
            x1rtol_c = x2rtol_old + np.random.randint(4,20)*1
            x2rtol_c = x1rtol_c+20

        x2rtol_old = x2rtol_c
        y1 = config.y1rtol
        y2 = config.y2rtol

        rand_color = list_colors[np.random.randint(0, len(list_colors))]

        if (np.random.rand() > anom_prob):
            # append circle
            list_rtol.append(canvas.create_oval(x1rtol_c, y1, x2rtol_c, y2, fill=rand_color, tag='rtol_' + str(j)))
            sublist_shapes_rtol.append(['circle_'+rand_color,x1rtol_c,x2rtol_c])
        else:
            # append triangle
            anom_count += 1
            sublist_shapes_rtol.append(['triangle_' + rand_color, x1rtol_c, x2rtol_c])
            list_rtol.append(canvas.create_polygon((x1rtol_c + x2rtol_c) / 2.0, y1, x1rtol_c, y2, x2rtol_c, y2, fill=rand_color, tag='rtol_' + str(j)))


    list_shapes_ltor.append(sublist_shapes_ltor)
    list_shapes_rtol.append(sublist_shapes_rtol)

    image_folder = os.path.join(mainfolder,'images_'+str(vid))

    if(not os.path.exists(image_folder)):
        os.makedirs(image_folder)

    while (canvas.coords(list_ltor[-1])[0]<=width or canvas.coords(list_rtol[-1])[2]>=0):

        for k in list_ltor:
            canvas.move(k, dx, dy)
        for k in list_rtol:
            canvas.move(k, -dx, dy)

        canvas.update()
        current_img = os.path.join(image_folder,'current_image.eps')
        savename = os.path.join(image_folder,'img_'+str(i).zfill(8)+'.png')
        i+=1
        canvas.postscript(file=current_img)
        img=Image.open(current_img)
        img.save(savename,"png")


    make_videos_of_frames(vid)
    vid+=1
    print "$$$$$$$$$$$$$$$$$$$$$$$$"
    print "ANOMALY COUNT:", anom_count
    print "$$$$$$$$$$$$$$$$$$$$$$$$"

    with open("list_shapes_ltor.txt", "wb") as fp:
        pickle.dump(list_shapes_ltor, fp)

sys.exit(0)


