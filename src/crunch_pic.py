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
