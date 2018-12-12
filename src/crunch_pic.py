import logging, threading, json_read_write, display, time, rgb
from PIL import Image, ImageTk, ImageDraw
import Tkinter as tk
import ttk
import os

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)s) %(message)s',)

def get_nails(nailsx, nailsy, image_x, image_y):
    ret = []
    get_nail_line(ret, 0, 0, image_x, image_y, 1, 0, 0, -1, nailsx, nailsy)
    get_nail_line(ret, image_x-1, 0, image_x, image_y, 0, 1, 1, 0, nailsx, nailsy)
    get_nail_line(ret, image_x-1, image_y-1, image_x, image_y, -1, 0, 0, 1, nailsx, nailsy)
    get_nail_line(ret, 0, image_y-1, image_x, image_y, 0, -1, -1, 0, nailsx, nailsy)
    return nails(ret)

def get_nail_line(ret, startx, starty, image_x, image_y, movex, movey, tickdx, tickdy, nailsx, nailsy):
    if movex:
        steps = nailsx
        scale = float(image_x) / steps
    else:
        steps = nailsy
        scale = float(image_y) / steps
    for scalar in xrange(steps):
        s = int(scale * scalar)
        x, y = startx + movex*s, starty + movey*s
        ret.append(nail(x,y, get_dir(tickdx, tickdy), scalar))
    return

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

class nail(object):
    def __init__(self, x, y, direction, number):
        self.x, self.y, self.direction, self.number = x, y, direction, number
        self.dir = directions[self.direction]

    def __str__(self):
        return "("+str(self.x)+","+str(self.y)+")"

    def to_json(self):
        return (self.x, self.y, self.number)

class nails(object):
    def __init__(self, nails):
        self.nails = nails

    def get_all_nails_off_of_direction(self, direction):
        return [nail for nail in self.nails if nail.direction != direction]

    def get_first_nail(self):
        return self.nails[0]

    def get_ticks(self):
        return [nail.get_tick() for nail in self.nails]

class weave_thread(threading.Thread):
    def __init__(self, app, json_file):
        super(weave_thread, self).__init__()
        self.app = app
        self.json_file = json_file
        self.setName("weave daemon")

    def run(self):
        logging.debug("starting")
        (self.nailsx, self.nailsy, self.steps_done, self.two_sided_nail, self.color_scheme, self.steps, self.picture_file) = json_read_write.read_json(self.json_file)
        self.image = Image.open(self.picture_file)
        self.height, self.width = self.image.height, self.image.width
        self.json_steps = []
        self.nailify_steps()
        self.put_colors(); self.color_index = 0
        self.current_color = self.next_color()
        self.unfaithful_complement = rgb.unfaithfulify(str(rgb.complement(self.current_color)))
        self.image.save(self.picture_file+".ppm")
        self.photo = tk.PhotoImage(file=self.picture_file+".ppm")
        os.remove(self.picture_file+".ppm")
        self.nails = get_nails(self.nailsx, self.nailsy, self.width, self.height)
        self.show()
        if not self.steps:
            self.current_nail = self.nails.get_first_nail()
        else:
            self.current_nail = self.steps[-1][1]
        while True:
            if len(self.steps) % 20 == 0:
                self.current_color = self.next_color()
                self.unfaithful_complement = rgb.unfaithfulify(str(rgb.complement(self.current_color)))
            self.next_nail = self.compute_next_step()
            self.draw_step((self.current_nail, self.next_nail))
            self.add_step(self.current_nail, self.next_nail)
            self.label_text.set("Current step: "+str(len(self.steps)))
            self.app.new_row(len(self.steps)-1, (self.current_nail, self.next_nail))
            #self.app.add_row_to_table(nail1, nail2)
            self.current_nail = self.next_nail
            time.sleep(0.1)
        self.save_now()

    def add_step(self, nail1, nail2):
        self.steps.append((nail1, nail2))
        self.json_steps.append((nail1.to_json(), nail2.to_json()))

    def nailify_steps(self):
        #ugly hack, to restore proper objects from the json_file
        steps = []
        temp = self.steps[:]
        self.steps = []
        for (nail1, nail2) in temp:
            nail00 = nail(nail1[0], nail1[1], self.get_direction_of_nail(nail1[0], nail1[1]), nail1[2])
            self.add_step(nail(nail1[0], nail1[1], self.get_direction_of_nail(nail1[0], nail1[1]), nail1[2]), nail(nail2[0], nail2[1], self.get_direction_of_nail(nail2[0], nail2[1]), nail2[2]))
        self.app.steps = self.steps

    def get_direction_of_nail(self, x, y):
        #ugly hack, as .json_file should be humanly readable
        if y == 0:
            return "N"
        if x == self.width - 1:
            return "E"
        if y == self.height - 1:
            return "S"
        if x == 0:
            return "W"
        raise Exception("A nail without a direction was found!")

    def next_color(self):
        self.color_index = (self.color_index + 1) % len(self.colors)
        return self.colors[self.color_index]

    def put_colors(self):
        if self.color_scheme == "bw":
            self.colors = ["#000000"]
        elif self.color_scheme == "rgb":
            self.colors = ["#FF0000", "#00FF00", "#0000FF"]
        else:
            raise Exception("Wrong color scheme found!")

    def compute_next_step(self):
        best_score, best_nail = 0, self.current_nail
        for pot_next_nail in nails.get_all_nails_off_of_direction(self.nails, self.current_nail.direction):
            next_score = self.score(self.current_nail, pot_next_nail)
            if next_score >= best_score:
                best_nail, best_score = pot_next_nail, next_score
        return best_nail

    def score(self, nail1, nail2):
        pixels = self.bresenham(nail1.x, nail1.y, nail2.x, nail2.y)
        ret = 0
        for p in pixels:
            ret += rgb.score(before=self.photo.get(p[0],p[1]), additionally=self.unfaithful_complement)
        return ret

    def draw_steps(self):
        for s in self.steps:
            self.draw_step(s)

    def draw_step(self, s):
        nail1, nail2 = s
        x1, y1, x2, y2 = nail1.x, nail1.y, nail2.x, nail2.y
        pixels = self.bresenham(x1, y1, x2, y2)
        for pixel in pixels:
            old_pixel_color = self.photo.get(pixel[0], pixel[1])
            new_pixel_color = rgb.array_add(old_pixel_color, self.unfaithful_complement)
            new_pixel_color = '#' + ''.join("00" if n < 0 else "0"+format(n, 'x') if n < 16 else format(n, 'x') if n < 256 else "FF" for n in new_pixel_color)
            self.photo.put(new_pixel_color, to=pixel)

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
        self.label_text = tk.StringVar()
        self.label_text.set("Current step: "+str(len(self.steps)))
        self.step_label = ttk.Label(self.frame, textvariable=self.label_text)
        self.step_label.grid(column=0, row=1, pady=5)
        self.draw_steps()

    def save_now(self):
        json_read_write.update_steps(self.json_file, self.json_steps)
        logging.debug("saved and exiting")
