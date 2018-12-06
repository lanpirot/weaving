import logging, threading, json_read_write
from PIL import Image, ImageTk, ImageDraw
import Tkinter as tk

def get_nails(nailsx, nailsy, image_x, image_y, border_width):
    ret = []
    ret.append(get_nail_line(border_width, border_width, image_x, image_y, 1, 0, 0, -1, nailsx, nailsy, border_width))
    ret.append(get_nail_line(image_x-border_width, border_width, image_x, image_y, 0, 1, 1, 0, nailsx, nailsy, border_width))
    ret.append(get_nail_line(image_x-border_width, image_y-border_width, image_x, image_y, -1, 0, 0, 1, nailsx, nailsy, border_width))
    ret.append(get_nail_line(border_width, image_y-border_width, image_x, image_y, 0, -1, -1, 0, nailsx, nailsy, border_width))
    return ret

def get_nail_line(startx, starty, image_x, image_y, movex, movey, tickdx, tickdy, nailsx, nailsy, border_width):
    ret = []
    if movex:
        steps = nailsx
        scale = float(image_x - 2*border_width) / steps
    else:
        steps = nailsy
        scale = float(image_y - 2*border_width) / steps
    for scalar in xrange(steps):
        s = int(scale * scalar)
        tickx, ticky = startx + movex*s, starty + movey*s
        ret.append((tickx, ticky, tickdx, tickdy))
    return ret
    
def get_nails_only(nails):
    ret = []
    for line in nails:
        ret.append([(a[0], a[1]) for a in line])
    #print ret
    return ret

directions = dict()
directions["N"] = (0,-1)
directions["E"] = (1,0)
directions["S"] = (0,1)
directions["W"] = (-1,0)

def get_dir(a, b):
    """Look up cardinal directions in the dictionary."""
    for dirc in directions.keys():
        if directions[dirc] == (a, b):
            return dirc
    raise

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)s) %(message)s',
                    )

class weave_thread(threading.Thread):
    def __init__(self, app, json_file, weave_daemon_finish_event):
        super(weave_thread, self).__init__()
        self.app = app
        self.json_file = json_file
        self.weave_daemon_finish_event = weave_daemon_finish_event
        self.setName("weave daemon")

    def run(self):
        logging.debug("starting")
        (self.nailsx, self.nailsy, self.steps_done, self.two_sided_nail, self.color_scheme, self.steps, self.picture_file) = json_read_write.read_json(self.json_file)
        self.image = Image.open(self.picture_file)
        self.height, self.width = self.image.height, self.image.width
        self.nails = get_nails_only(get_nails(self.nailsx, self.nailsy, self.width, self.height, 0))
        self.image_draw = ImageDraw.Draw(self.image)
        self.photo = ImageTk.PhotoImage(image=self.image)
        self.draw_steps()
        self.show()
        while not self.weave_daemon_finish_event.isSet():
            pass
        self.save_now()
        #whenever a step is finished call app.add_row_to_table(nail1, nail2)
    
    
    
    def show(self):
        self.show_window = tk.Toplevel(self.app)
        self.show_window.title("Current daemon thread picture")
        self.show_window.resizable(0,0)
        self.show_window.geometry(str(self.width) + "x" + str(self.height))
        self.canvas = tk.Canvas(self.show_window)
        self.canvas.configure(height = self.image.height, width = self.image.width)
        self.canvas.create_image((0, 0), image=self.photo, anchor=tk.NW)
        self.canvas.grid()
    
    def save_now(self):
        json_read_write.update_steps(self.json_file, self.steps)
        logging.debug("saved and exiting")
