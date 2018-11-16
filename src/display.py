import Tkinter as tk
from PIL import Image, ImageTk

border_width = 40
tick_length = 3
my_photo = 0

def load(master_app, canvas_pic, canvas_pos, canvas_neg, picture_file, nailsx, nailsy, nails):
    global my_photo
    with Image.open(picture_file) as my_image:
        my_photo = ImageTk.PhotoImage(image=my_image)
        clear_load_canvasses(master_app, canvas_pic, canvas_pos, canvas_neg, my_photo, nailsx, nailsy, nails)

    
def put_photo_on_canvasses(master_app, canvasses, my_photo):
    for e, c in enumerate(canvasses):
        c.delete("all")
        c.configure(height = my_photo.height()+2*border_width, width = my_photo.width()+2*border_width)
	c.create_image((border_width,border_width), image=my_photo, anchor=tk.NW, tags="image")
	c.grid(column = e*2, row = 0)
    
def draw_ticks(c, my_photo, startx, starty, movex, movey, tickdx, tickdy, nailsx, nailsy, nails):
    if movex:
        steps = nailsx
        scale = float(my_photo.width()) / steps
    else:
        steps = nailsy
        scale = float(my_photo.height()) / steps
    for scalar in xrange(steps):
        s = int(scale * scalar)
        tickx, ticky = startx + movex*s, starty + movey*s
        nails.append((scalar, tickx, ticky))
        c.create_line(tickx, ticky, tickx+tick_length*tickdx, ticky+tick_length*tickdy, tags="tick")
        if scalar % 5 == 0:
            c.create_line(tickx, ticky, tickx+2*tick_length*tickdx, ticky+2*tick_length*tickdy, tags="tick")
            c.create_text(tickx+6*tick_length*tickdx, ticky+6*tick_length*tickdy, text=str(scalar), tags="tick")
    
def draw_border(canvasses, my_photo, nailsx, nailsy, nails):
    height, width = my_photo.height(), my_photo.width()
    border = border_width
    for c in canvasses:
        c.create_line(border, border, width+border, border, width+border, height+border, border, height+border, border, border, tags="border")
        draw_ticks(c, my_photo, border, border, 1, 0, 0, -1, nailsx, nailsy, nails)
        draw_ticks(c, my_photo, width+border, border, 0, 1, 1, 0, nailsx, nailsy, nails)
        draw_ticks(c, my_photo, border+width, border+height, -1, 0, 0, 1, nailsx, nailsy, nails)
        draw_ticks(c, my_photo, border, height+border, 0, -1, -1, 0, nailsx, nailsy, nails)

    
def clear_load_canvasses(master_app, canvas_pic, canvas_pos, canvas_neg, my_photo, nailsx, nailsy, nails):
    put_photo_on_canvasses(master_app, (canvas_pic, canvas_neg), my_photo)
    canvas_pos.delete("all")
    canvas_pos.configure(height = my_photo.height()+2*border_width, width = my_photo.width()+2*border_width)
    draw_border((canvas_pic, canvas_pos, canvas_neg), my_photo, nailsx, nailsy, nails)
