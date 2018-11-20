import Tkinter as tk
from PIL import Image, ImageTk, ImageDraw

border_width = 40
tick_length = 3
canvasses = [0, 1, 2]
photos = [0, 1, 2]
my_image_source = 0
my_image_blank = 0

directions = dict()
directions["N"] = (0,-1)
directions["E"] = (1,0)
directions["S"] = (0,1)
directions["W"] = (-1,0)

def get_dir(a, b):
    for dirc in directions.keys():
        if directions[dirc] == (a, b):
            return dirc
    raise

#after the picture was already loaded once, and we need to reset to the very beginning
def reload_from_start():
    for c in canvasses:
        if c[2] != 1:
            photos[c[2]] = ImageTk.PhotoImage(image=my_image_source)
            canvasses[c[2]] = (c[0], my_image_source.copy(), c[2])
        else:
            photos[c[2]] = ImageTk.PhotoImage(image=my_image_blank)
            canvasses[c[2]] = (c[0], my_image_blank.copy(), c[2])
        c[0].itemconfigure('image', image=photos[c[2]])
        
#load new picture from very start
def load(master_app, canvas_pic, canvas_pos, canvas_neg, picture_file, nailsx, nailsy, nails):
    global canvasses, my_image_source, my_image_blank
    cs = (canvas_pic, canvas_pos, canvas_neg)
    with Image.open(picture_file) as img:
        my_image_blank = Image.new("RGBA", (img.width + 2*border_width, img.height + 2*border_width))
        my_image_source = my_image_blank.copy()
        my_image_source.paste(img, box=(border_width, border_width))
        
        for e in xrange(len(canvasses)):
            if e != 1:
                photos[e] = ImageTk.PhotoImage(image=my_image_source)
                canvasses[e] = (cs[e], my_image_source, e)
            else:
                photos[e] = ImageTk.PhotoImage(image=my_image_blank)
                canvasses[e] = (cs[e], my_image_blank, e)
        clear_load_canvasses(nailsx, nailsy, nails)
        #these images can now be reused, for drawing purposes from the very start
        my_image_blank = canvasses[1][1].copy()
        my_image_source = canvasses[0][1].copy()

def clear_load_canvasses(nailsx, nailsy, nails):
    for c in canvasses:
        canvas, photo = c[0], photos[c[2]]
        canvas.delete("all")
        
        canvas.configure(height = photo.height(), width = photo.width())
        draw_border(c, nailsx, nailsy, nails)
        photos[c[2]] = ImageTk.PhotoImage(image=c[1])
        canvas.create_image((0, 0), image=photos[c[2]], anchor=tk.NW, tags="image")
        

def draw_border(c, nailsx, nailsy, nails):
    height, width = photos[c[2]].height(), photos[c[2]].width()
    border = border_width
    
    image_draw = ImageDraw.Draw(c[1])
    image_draw.line([(border, border), (width-border, border), (width-border, height-border), (border, height-border), (border, border)], fill="black")
    draw_ticks(image_draw, c[2], border, border, 1, 0, 0, -1, nailsx, nailsy, nails)
    draw_ticks(image_draw, c[2], width-border, border, 0, 1, 1, 0, nailsx, nailsy, nails)
    draw_ticks(image_draw, c[2], width-border, height-border, -1, 0, 0, 1, nailsx, nailsy, nails)
    draw_ticks(image_draw, c[2], border, height-border, 0, -1, -1, 0, nailsx, nailsy, nails)
        

def draw_ticks(image_draw, app, startx, starty, movex, movey, tickdx, tickdy, nailsx, nailsy, nails):
    border = border_width
    if movex:
        steps = nailsx
        scale = float(photos[0].width()-2*border_width) / steps
    else:
        steps = nailsy
        scale = float(photos[0].height()-2*border_width) / steps
    for scalar in xrange(steps):
        s = int(scale * scalar)
        tickx, ticky = startx + movex*s, starty + movey*s
        if not app:
            #all nails (but only for one canvas) get archived for later usage in the actual algorithm
            nails.append(((scalar, get_dir(tickdx, tickdy)), (tickx, ticky), (tickx-border, ticky-border)))
        image_draw.line([(tickx, ticky), (tickx+tick_length*tickdx, ticky+tick_length*tickdy)], fill="black")
        if scalar % 5 == 0:
            image_draw.line([(tickx, ticky), (tickx+2*tick_length*tickdx, ticky+2*tick_length*tickdy)], fill="black")
            #myfont = ImageFont.truetype("my-font", 16)
            #draw.textsize(msg, font=myFont)
            w, h = image_draw.textsize(str(scalar))
            image_draw.text(((tickx+6*tick_length*tickdx)-w/2, (ticky+6*tick_length*tickdy)-h/2), text=str(scalar), fill="black")

def draw_lines(lines):
    image_draw_p = ImageDraw.Draw(canvasses[1][1])
    image_draw_n = ImageDraw.Draw(canvasses[2][1])
    for l in lines:
        draw_line(l, image_draw_p, +1)
        draw_line(l, image_draw_n, 0)
    photos[1] = ImageTk.PhotoImage(image=canvasses[1][1])
    canvasses[1][0].itemconfigure('image', image=photos[1])
    photos[2] = ImageTk.PhotoImage(image=canvasses[2][1])
    canvasses[2][0].itemconfigure('image', image=photos[2])

def draw_line((nail1, nail2), draw, pos_neg):
    x1, y1 = nail1[1][0], nail1[1][1]
    x2, y2 = nail2[1][0], nail2[1][1]
    if pos_neg:
        draw.line([(x1, y1), (x2, y2)], (0,0,0,30))
    else:
        draw.line([(x1, y1), (x2, y2)], (255,255,255,10))
