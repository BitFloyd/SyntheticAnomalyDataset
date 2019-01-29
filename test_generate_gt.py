from Tkinter import *
from PIL import Image, ImageTk
import os
import pickle
import sys
import config

def make_videos_of_frames(i):

    dir = 'Videos'
    fid = 'images_'+str(i)+'_gt'

    str_command = 'ffmpeg -r 12 -y -i ' + os.path.join(fid, 'img_%08d.bmp') + ' ' + os.path.join(dir,'video_gt_' + str(i) + '.mp4')

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

#create_black_background_image
im = Image.frombytes('L', (width, height), "\x00" * width * height)
im = ImageTk.PhotoImage(im)
canvas.create_image(0, 0, image=im, anchor=NW)


dx = 1
dy = 0

with open("list_shapes_ltor.txt", "rb") as fp:   # Unpickling
    list_shapes_ltor= pickle.load(fp)

with open("list_shapes_rtol.txt", "rb") as fp:   # Unpickling
    list_shapes_rtol= pickle.load(fp)

list_colors = ["white", "black", "red", "green", "blue", "cyan", "yellow", "magenta"]

anom_count = 0

vid=0


for m in range(0,len(list_shapes_ltor)):
    i=0
    list_ltor=[]
    list_rtol=[]
    sublist_shapes_ltor=list_shapes_ltor[m]
    sublist_shapes_rtol=list_shapes_rtol[m]

    # create queue of shapes in -x and +x direction to be moved across screen
    for j in range(0,len(sublist_shapes_ltor)):

        #Left to right queue
        shape_color = sublist_shapes_ltor[j][0]
        x1ltor_c = sublist_shapes_ltor[j][1]
        x2ltor_c = sublist_shapes_ltor[j][2]

        shape = shape_color.split("_")[0]
        color = shape_color.split("_")[1]

        y1 = config.y1ltor
        y2 = config.y2ltor

        if(shape=='square'):
            #append square
            list_ltor.append(canvas.create_rectangle(x1ltor_c, y1, x2ltor_c, y2, fill='black',outline='black', tag='ltor_'+str(j)))
        else:
            #append_triangle
            list_ltor.append(canvas.create_polygon((x1ltor_c + x2ltor_c) / 2.0, y1, x1ltor_c, y2, x2ltor_c, y2, fill='white', tag='ltor_' + str(j)))


        # Right to Left queue
        shape_color = sublist_shapes_rtol[j][0]
        x1rtol_c = sublist_shapes_rtol[j][1]
        x2rtol_c = sublist_shapes_rtol[j][2]

        y1 = config.y1rtol
        y2 = config.y2rtol

        shape = shape_color.split("_")[0]
        color = shape_color.split("_")[1]


        if (shape=='circle'):
            # append circle
            list_rtol.append(canvas.create_oval(x1rtol_c, y1, x2rtol_c, y2, fill='black',outline='black',tag='rtol_' + str(j)))

        else:
            # append triangle
            list_rtol.append(canvas.create_polygon((x1rtol_c + x2rtol_c) / 2.0, y1, x1rtol_c, y2, x2rtol_c, y2, fill='white', tag='rtol_' + str(j)))

    image_folder = os.path.join('Test','images_'+str(vid)+'_gt')

    if(not os.path.exists(image_folder)):
        os.makedirs(image_folder)

    while (canvas.coords(list_ltor[-1])[0]<=width or canvas.coords(list_rtol[-1])[2]>=0):

        for k in list_ltor:
            canvas.move(k, dx, dy)
        for k in list_rtol:
            canvas.move(k, -dx, dy)
        # canvas.after(1)
        canvas.update()
        current_img = os.path.join(image_folder,'current_image.eps')
        savename = os.path.join(image_folder,'img_'+str(i).zfill(8)+'.'+'bmp')
        i+=1
        canvas.postscript(file=current_img)
        img=Image.open(current_img)
        img.save(savename,"bmp")

    make_videos_of_frames(vid)
    vid+=1

sys.exit(0)
