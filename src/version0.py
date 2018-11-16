from PIL import Image
import math
import time
import random

line_width = 45
num_rounds = 1500
num_nails = 400

pic = Image.open('INPUT.JPG')
img = pic.copy()
img = img.convert('L')
res = Image.new('L', img.size)
nail_radius = 1

for x in range(res.size[0]):
    for y in range(res.size[1]):
        res.putpixel((x, y), 255)
print "Canvas whitened..."
sqrt2 = math.sqrt(2)
sqrt2h = 0.6#sqrt2 / 2

def random_sort(list):
    l = []
    while len(list) > 0:
        index = random.randint(0, len(list) - 1)
        l += [list[index]]
        del list[index]        
    return l

def ordered((x1,y1), (x2,y2)):
    if x1 < x2:
        return True
    if x1 == x2 and y1 < y2:
        return True
    return False

def vec_plus((x1, y1), (x2, y2)):
    return (x1+x2, y1+y2)

def vec_scalar(a, (x,y)):
    return (a*x, a*y)

def step(curr, v):
    next = vec_plus(curr, v)
    next_pixels = []
    if (int(curr[0]) != int(next[0]) and int(curr[1]) != int(next[1])):
        inter1 = (next[0], curr[1])
        inter2 = (curr[0], next[1])
        next_pixels += [(int(inter1[0]), int(inter1[1])), (int(inter2[0]), int(inter2[1]))]
    next_pixels += [(int(next[0]), int(next[1]))]
    return (next, next_pixels)

def dist_point_to_line((ori, dir), (x, y)):
    (x_o, y_o) = (ori[0], ori[1])
    (x_d, y_d) = (dir[0], dir[1])
    a = -(x_o*x_d - x*x_d + y_o*y_d - y*y_d) / (x_d*x_d + y_d*y_d)#/2
    #print ori, dir, (x,y), a, length((ori[0] + a*dir[0], ori[1] + a*dir[1]), (x,y))
    return length(vec_plus(ori, vec_scalar(a, dir)), (x,y))

def midpoint((x,y)):
    return (x+0.5, y+0.5)

def norm(dist):
    dist = max(0, sqrt2h - dist)
    if dist <= 0:
        return 0
    return int(line_width * dist / sqrt2h + line_width)

def length((x1, y1), (x2, y2)):
    x = x1 - x2
    y = y1 - y2
    return math.sqrt(x*x + y*y)

class Line(object):
    def __init__(self, point_a, point_b):
        self.ori = point_a
        self.des = point_b
        self.dir = self.normalize(Line.get_direction(self, point_a, point_b))
    
    def get_direction(self, (ax, ay), (bx, by)):
        return (bx - ax, by - ay)
    
    def normalize(self, (x, y)):
        leng = length((0, 0), (x, y))
        if leng == 0:
            leng = 1
        return (x / leng, y / leng)
        
    def pixels_hit(self):
        hits = []
        if ordered(self.ori, self.des):
            (a, b, v) = (self.ori, self.des, self.dir)
        else:
            (a, b, v) = (self.des, self.ori, (-self.dir[0], -self.dir[1]))
        curr = a
        hits += [(curr, norm(dist_point_to_line((self.ori, self.dir), midpoint((int(curr[0]), int(curr[1]))))))]
        #das sollte int(curr[0]) int(curr[1)] sein
        while ordered(curr, b):
            (curr, pixels_hit) = step(curr, v)
            for pixel_hit in pixels_hit:
                if pixel_hit == hits[-1][0]:
                    continue
                nor = norm(dist_point_to_line((self.ori, self.dir), midpoint(pixel_hit)))
                #print pixel_hit, nor, dist_point_to_line((self.ori, self.dir), midpoint(pixel_hit))
                if nor > 0:
                    hits += [(pixel_hit, nor)]
        return hits
    
    def printify(self):
        if self.des[0] < 0:
            seite = 'LINKS'
        if self.des[1] < 0:
            seite = 'OBEN'
        if self.des[0] > img.size[0]:
            seite = 'RECHTS'
        if self.des[1] > img.size[1]:
            seite = 'UNTEN'
        return str(vec_plus((0,0),self.ori)), str(vec_plus((0,0),self.des)), seite#, str(self.dir)
        
    def length(self):
        return length(self.ori, self.des)

def normalize(scale):
    return max(min(255, scale), 0)

def add_pixel(pic, pixel, multiple):
    if is_outside(pixel[0]):
        return
    pic.putpixel(pixel[0], normalize(pic.getpixel(pixel[0]) + multiple * pixel[1]))
    return

def is_outside((x,y)):
    if x < 0 or y < 0 or y >= res.size[1] or x >= res.size[0]:
        return True
    return False

def get_difference(line, res, pic, t):
    difference = 0
    pixels = line.pixels_hit()
    #print pixels
    if len(pixels) < 10 or min(length(pixels[0][0], line.ori), length(pixels[0][0], line.des)) > 1 or min(length(pixels[-1][0], line.ori), length(pixels[-1][0], line.des)) > 1:
        return 255**3 * len(pixels)
    hit = False
    for pixel in pixels:
        if is_outside(pixel[0]):
            difference += 255**3
        else:
            blacken = (255 - pic.getpixel(pixel[0]))
            d = pixel[1] - blacken
            if blacken > line_width / 2:
                hit = True
            difference += d**3
            #difference += abs(min(0, (255 - pic.getpixel(pixel[0])) - pixel[1]))
            #difference += abs(normalize(pic.getpixel(pixel[0]) - pixel[1]))
    if difference < 0:
        difference /= math.sqrt(len(pixels) + line.length())
    else:
        difference *= math.sqrt(len(pixels) + line.length())
    if hit == False:
        return 255**3 * len(pixels)
    return int(difference / len(pixels))
    #return int(difference / len(pixels))

def same_side((x1, y1), (x2, y2)):
    if x1 == x2 or y1 == y2:
        return True
    if x1 == x2:
        if x1 <= 0 or x1 >= img.size[0] - 1:
            return True
    if y1 == y2:
        if y1 <= 0 or y1 >= img.size[1] - 1:
            return True
    return False

nails = [(-1,y) for y in range(-1, img.size[1] + 2)]  + [(img.size[0]+1, y) for y in range(-1, img.size[1] + 2)]
nails += [(x,-1) for x in range(img.size[0]+1)] + [(x, img.size[1]+1) for x in range(img.size[0]+1)]
nails = [nails[i] for i in range(len(nails)) if nails[i][0] % 5 == 0 or nails[i][1] % 5 == 0]
#east-west-north-south them
nails_t  = [vec_plus(nail, (nail_radius,0)) for nail in nails if nail[0] >= 0 and nail[0] <= img.size[0]]
nails_t += [vec_plus(nail, (-nail_radius,0)) for nail in nails if nail[0] >= 0 and nail[0] <= img.size[0]]
nails_t += [vec_plus(nail, (0,nail_radius)) for nail in nails if nail[0] < 0 or nail[0] > img.size[0]]
nails_t += [vec_plus(nail, (0,-nail_radius)) for nail in nails if nail[0] < 0 or nail[0] > img.size[0]]
nails = nails_t[:]
print nails

print "There are ", str(len(nails)), " nails."
#nails = random_sort(nails)[:num_nails]
rounds = 0
nail = nails[0]
last_benefit = 10000000000
last_nail = nails[-1]

def start(nail, nails):
    return [n for n in nails if length(nail, n) < nail_radius*2.5 and length(nail, n) > nail_radius*1.5]

while rounds < num_rounds:   
    min_benefit = 10000000000000
    nails = random_sort(nails)
    start_nails = start(nail, nails)
    for nail in start_nails:    
        for n in range(len(nails)):
            if nails[n] in start_nails or nails[n] == last_nail or same_side(nail, nails[n]):
                continue
            curr_line = Line(nail, nails[n])
            benefit = get_difference(curr_line, res, img, False)
            if benefit < min_benefit and random.randint(0,10) > 0:
                (min_benefit, best_line) = (benefit, curr_line)
                best_nail = nails[n]
            if min_benefit < last_benefit:
                break
    (last_benefit, last_nail) = (min_benefit, nail)
    for pixel in best_line.pixels_hit():
        add_pixel(res, pixel, -1)
        add_pixel(img, pixel, +1)
    rounds += 1
    nail = best_nail
    print "Line", rounds, "done.", min_benefit, best_line.printify()
    if rounds % 100 == 0 or rounds == num_rounds: #and rounds >= 500:
        file_name = 'width = ' + str(line_width) + ' ' + 'nails = ' + str(len(nails)) + ' ' + str(time.strftime('%c')) + ' ' + str(rounds)
        res.save(file_name,'jpeg')
        file_name = 'inverse width = ' + str(line_width) + ' ' + 'nails = ' + str(len(nails)) + ' ' + str(time.strftime('%c')) + ' ' + str(rounds)
        img.save(file_name,'jpeg')
print "Done!!"


#different color channels
#different line_widths
#maybe a "white" color to readden brightness in certain parts
#maybe a darkest pixel saved, go to that, or as close as possible

#maybe nail positions inside the picture