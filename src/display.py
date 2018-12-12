import Tkinter as tk
import ttk
from PIL import Image, ImageTk, ImageDraw
import crunch_pic


all_canvasses = dict()
border_width = 40
new_window_canvas_id = 3

class my_canvas(object):
    

    def __init__(self, picture_file, canvas, nails, draw_var):
        self.picture_file = picture_file
        self.canvas = canvas
        self.nails = nails
        self.draw_var = draw_var
        img = Image.open(self.picture_file)
        self.start_image = Image.new("RGBA", (img.width + 2*border_width, img.height + 2*border_width))
        self.height, self.width = self.start_image.height, self.start_image.width
        if draw_var <= 0:
            self.start_image.paste(img, box=(border_width, border_width))
        
        self.image_draw = ImageDraw.Draw(self.start_image)
        self.draw_border()
        self.tick_length = 3
        self.draw_ticks()
        self.start_photo = ImageTk.PhotoImage(image=self.start_image)
        self.image = self.start_image.copy()
        self.image_draw = ImageDraw.Draw(self.image)
                
        self.canvas.delete("all")
        self.canvas.configure(height = self.image.height, width = self.image.width)
        self.canvas.create_image((0, 0), image=self.start_photo, anchor=tk.NW, tags="image")

    def draw_ticks(self):
        for tick in self.nails.nails:
            self.draw_tick_line(tick)
            if tick.number % 5 == 0:
                self.draw_tick_line(tick, long=True)
                w, h = self.image_draw.textsize(str(tick.number))
                self.image_draw.text(((tick.x+7*self.tick_length*tick.dir[0])-w/2+border_width, (tick.y+7*self.tick_length*tick.dir[1])-h/2+border_width), text=str(tick.number), fill="black")

    def draw_tick_line(self, tick, long=False):
        tick_length = self.tick_length
        if long:
            tick_length *= 2
        start_x, start_y, end_x, end_y = tick.x+border_width, tick.y+border_width, tick.x+2*tick_length*tick.dir[0]+border_width, tick.y+2*tick_length*tick.dir[1]+border_width
        self.image_draw.line([(start_x, start_y), (end_x, end_y)], fill="black")

    def draw_border(self):
        width, height = self.start_image.width, self.start_image.height
        self.image_draw.line([(border_width, border_width), (width-border_width-1, border_width), (width-border_width-1, height-border_width-1), (border_width, height-border_width-1), (border_width, border_width)], fill="black")

    def delete_lines(self, lines):
        self.canvas.delete("marker")
        for l in lines:
            self.canvas.delete("line"+str(l))
    
    def draw_lines(self, lines, mark=False):
        """Lines can only be drawn on the right canvas. On the middle one, they may be put in a special mode (mark)."""
        if self.draw_var == 0:
            return
        for l in lines:
            self.draw_line(l, mark)

    def draw_line(self, (l, (nail1, nail2)), mark=False):
        """On the middle canvas the lines are put on positively, on the right negatively. If the user selected the mark-mode, the line will be put on fat and red."""
        x1, y1 = nail1.x, nail1.y
        x2, y2 = nail2.x, nail2.y
        if mark and self.draw_var > 0:
            self.canvas.delete("marker")
            self.canvas.create_line((x1+border_width, y1+border_width), (x2+border_width, y2+border_width), fill=("#FF0000"), width=3, tags="marker")
        else:
            self.canvas.create_line((x1+border_width, y1+border_width), (x2+border_width, y2+border_width), fill=("#000000"), tags="line"+str(l))

    def remove_marking(self):
        self.canvas.delete("marker")


def load(canvasses, picture_file, nails_x, nails_y):
    global all_canvasses, border_width
    img = Image.open(picture_file)
    nails = crunch_pic.get_nails(nails_x, nails_y, img.width, img.height)
    for (id, c) in canvasses:
        if id == 0 or id == new_window_canvas_id:
            draw_var = 0
        elif id == 1:
            draw_var = 1
        else:
            draw_var = -1
        all_canvasses[id] = my_canvas(picture_file, c, nails, draw_var)
    return

def destroy():
    del all_canvasses[new_window_canvas_id]

def delete_lines(lines):
    for c in all_canvasses:
        all_canvasses[c].delete_lines(lines)

def draw_lines(steps, mark=False):
    for c in all_canvasses:
        all_canvasses[c].draw_lines(steps, mark)

def remove_marking():
    for c in all_canvasses:
        all_canvasses[c].remove_marking()

def create_photos():
    """The button pictures are loaded for the play, back ... buttons."""
    start_photo = ImageTk.PhotoImage(image=Image.open("icons/icons-start.png"))
    back_photo = ImageTk.PhotoImage(image=Image.open("icons/icons-bplay.png"))
    play_photo = ImageTk.PhotoImage(image=Image.open("icons/icons-play.png"))
    end_photo = ImageTk.PhotoImage(image=Image.open("icons/icons-end.png"))
    return (start_photo, back_photo, play_photo, end_photo)
