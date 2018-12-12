import logging, threading, json_read_write, display, time, rgb
from PIL import Image, ImageTk, ImageDraw
import Tkinter as tk
import ttk
import os

def get_nails(nailsx, nailsy, image_x, image_y, border_width):
    ret = []
    ret.append(get_nail_line(0, 0, image_x, image_y, 1, 0, 0, -1, nailsx, nailsy, border_width))
    ret.append(get_nail_line(image_x-1, 0, image_x, image_y, 0, 1, 1, 0, nailsx, nailsy, border_width))
    ret.append(get_nail_line(image_x-1, image_y-1, image_x, image_y, -1, 0, 0, 1, nailsx, nailsy, border_width))
    ret.append(get_nail_line(0, image_y-1, image_x, image_y, 0, -1, -1, 0, nailsx, nailsy, border_width))
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
        self.put_colors(); self.color_index = 0
        self.current_color = self.next_color()
        self.unfaithful_complement = rgb.unfaithfulify(str(rgb.complement(self.current_color)))
        self.image = Image.open(self.picture_file)
        self.image.save(self.picture_file+".ppm")
        self.photo = tk.PhotoImage(file=self.picture_file+".ppm")
        os.remove(self.picture_file+".ppm")
        self.height, self.width = self.image.height, self.image.width
        self.nails = get_nails_only(get_nails(self.nailsx, self.nailsy, self.width, self.height, 0))
        self.show()
        while True:
            if len(self.steps) % 20 == 0:
                self.current_color = self.next_color()
                self.unfaithful_complement = rgb.unfaithfulify(str(rgb.complement(self.current_color)))
            self.next_nail = self.compute_next_step()
            print "next line to", self.next_nail
            self.draw_step((self.current_nail, self.next_nail))
            self.steps.append((self.current_nail, self.next_nail))
            #app.add_row_to_table(nail1, nail2)
            self.current_nail = self.next_nail
            time.sleep(0.1)
        self.save_now()

    def next_color(self):
        self.color_index = (self.color_index + 1) % len(self.colors)
        return self.colors[self.color_index]

    def put_colors(self):
        self.color_scheme = "rgb"
        if self.color_scheme == "bw":
            self.colors = ["#000000"]
        elif self.color_scheme == "rgb":
            self.colors = ["#FF0000", "#00FF00", "#0000FF"]
        else:
            raise "Wrong color scheme found!"

    def get_direction_of_nail(self, nail):
        x, y = nail
        if y == 0:
            return 0
        if x == self.image.width-1:
            return 1
        if y == self.image.height-1:
            return 2
        if x == 0:
            return 3
        raise "A nail without a direction was found!"

    def compute_next_step(self):
        current_dir = self.get_direction_of_nail(self.current_nail)
        best_score, best_nail = 0, self.current_nail
        for pot_next_nails in self.nails[:current_dir]+self.nails[current_dir+1:]:
            for pot_next_nail in pot_next_nails:
                next_score = self.score(self.current_nail, pot_next_nail)
                if next_score >= best_score:
                    best_nail, best_score = pot_next_nail, next_score
        return best_nail

    def score(self, (x1,y1), (x2,y2)):
        pixels = self.bresenham(x1,y1,x2,y2)
        ret = 0
        for p in pixels:
            ret += rgb.score(before=self.photo.get(p[0],p[1]), additionally=self.unfaithful_complement)
        return ret

    def draw_steps(self):
        if not self.steps:
            self.current_nail = self.nails[0][0]
        else:
            self.current_nail = self.steps[-1][-1]
        for s in self.steps:
            self.draw_step(s)

    def draw_step(self, s):
        nail1, nail2 = s
        x1, y1 = nail1[0], nail1[1]
        x2, y2 = nail2[0], nail2[1]
        pixels = self.bresenham(x1,y1,x2,y2)
        for pixel in pixels:
            old_pixel_color = self.photo.get(pixel[0], pixel[1])
            new_pixel_color = rgb.array_add(old_pixel_color, self.unfaithful_complement)
            new_pixel_color = '#' + ''.join("00" if n < 0 else "0"+format(n, 'x') if n < 16 else format(n, 'x') if n < 256 else "FF" for n in new_pixel_color)
            self.photo.put(new_pixel_color, to=pixel)
        self.step_label.configure(text="Current step: "+str(len(self.steps)))

    def bresenham(self, x1,y1,x2,y2):
        pixels = []
        dx, dy = abs(x2-x1), -abs(y2-y1)
        sx, sy = -cmp(x1, x2), -cmp(y1, y2)
        err = dx + dy
        while True:
            pixels.append((x1, y1))
            if (x1 == x2 and y1 == y2):
                break
            e2 = 2*err
            if e2 > dy:
                err += dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy
        return pixels

    def show(self):
        self.show_window = tk.Toplevel(self.app)
        self.show_window.title("Current daemon thread picture")
        self.show_window.resizable(0,0)
        self.show_window.geometry(str(self.width) + "x" + str(self.height+50))
        self.frame = ttk.Frame(self.show_window)
        self.frame.grid()
        self.canvas = tk.Canvas(self.frame, bg="#FFFFFF")
        self.canvas.configure(height = self.image.height, width = self.image.width)
        self.canvas.create_image((0, 0), image=self.photo, anchor=tk.NW, tags="image")
        self.canvas.grid(column=0, row=0)
        self.step_label = ttk.Label(self.frame, text="Current step: "+str(len(self.steps)))
        self.step_label.grid(column=0, row=1, pady=5)
        self.draw_steps()

    def save_now(self):
        json_read_write.update_steps(self.json_file, self.steps)
        logging.debug("saved and exiting")
