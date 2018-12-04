import Tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import crunch_pic

border_width = 40
tick_length = 3
all_canvasses = dict()

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
        self.draw_ticks()
        self.start_photo = ImageTk.PhotoImage(image=self.start_image)
        self.image = self.start_image.copy()
        self.image_draw = ImageDraw.Draw(self.image)
                
        self.canvas.delete("all")
        self.canvas.configure(height = self.image.height, width = self.image.width)
        self.canvas.create_image((0, 0), image=self.start_photo, anchor=tk.NW, tags="image")
            
    def draw_ticks(self):
        for tick_line in self.nails:
            self.draw_tick_line(tick_line)

    def draw_tick_line(self, tick_line):
        for e, tick in enumerate(tick_line):
            start_x, start_y, end_x, end_y = tick[0], tick[1], tick[0]+tick_length*tick[2], tick[1]+tick_length*tick[3]
            self.image_draw.line([(start_x, start_y), (end_x, end_y)], fill="black")
            if e % 5 == 0:
                start_x, start_y, end_x, end_y = tick[0], tick[1], tick[0]+2*tick_length*tick[2], tick[1]+2*tick_length*tick[3]
                self.image_draw.line([(start_x, start_y), (end_x, end_y)], fill="black")
                w, h = self.image_draw.textsize(str(e))
                self.image_draw.text(((tick[0]+6*tick_length*tick[2])-w/2, (tick[1]+6*tick_length*tick[3])-h/2), text=str(e), fill="black")

    def draw_border(self):
        width, height = self.start_image.width, self.start_image.height
        self.image_draw.line([(border_width, border_width), (width-border_width, border_width), (width-border_width, height-border_width), (border_width, height-border_width), (border_width, border_width)], fill="black")

    def reload_from_start(self):
        self.image = self.start_image.copy()
        self.image_draw = ImageDraw.Draw(self.image)
        self.photo = self.start_photo
        self.canvas.itemconfigure('image', image=self.photo)
    
    def draw_lines(self, lines, mark=False):
        """Lines can only be drawn on the middle and right canvas. On the middle one, they may be put in a special mode (mark)."""
        if self.draw_var == 0:
            return
        for l in lines:
            self.draw_line(l, mark)
        self.photo = ImageTk.PhotoImage(image=self.image)
        self.canvas.itemconfigure('image', image=self.photo)

    def draw_line(self, (nail1, nail2), mark=False):
        """On the middle canvas the lines are put on positively, on the right negatively. If the user selected the mark-mode, the line will be put on fat and red."""
        x1, y1 = nail1[1][0], nail1[1][1]
        x2, y2 = nail2[1][0], nail2[1][1]
        if mark and self.draw_var > 0:
            self.image_draw.line([(x1, y1), (x2, y2)], (255,0,0), width=3)
        else:
            if self.draw_var > 0:
                self.image_draw.line([(x1, y1), (x2, y2)], (0,0,0,30))
            else:
                self.image_draw.line([(x1, y1), (x2, y2)], (255,255,255,10))


def load(canvasses, picture_file, nails_x, nails_y):
    global all_canvasses, border_width
    img = Image.open(picture_file)
    nails = crunch_pic.get_nails(nails_x, nails_y, img.width+2*border_width, img.height+2*border_width, border_width)
    for (id, c) in canvasses:
        if id == 0 or id == 3:
            draw_var = 0
        elif id == 1:
            draw_var = 1
        else:
            draw_var = -1
        all_canvasses[id] = my_canvas(picture_file, c, nails, draw_var)
    return crunch_pic.get_nails_only(nails)

def destroy():
    del all_canvasses[3]

def reload_from_start():
    for c in all_canvasses:
        all_canvasses[c].reload_from_start()

def draw_lines(steps, mark=False):
    for c in all_canvasses:
        all_canvasses[c].draw_lines(steps, mark)
    
def create_photos():
    """The button pictures are loaded for the play, back ... buttons."""
    start_photo = ImageTk.PhotoImage(image=Image.open("icons/icons-start.png"))
    back_photo = ImageTk.PhotoImage(image=Image.open("icons/icons-bplay.png"))
    play_photo = ImageTk.PhotoImage(image=Image.open("icons/icons-play.png"))
    end_photo = ImageTk.PhotoImage(image=Image.open("icons/icons-end.png"))
    return (start_photo, back_photo, play_photo, end_photo)
