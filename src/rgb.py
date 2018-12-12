import numpy

class RGB(numpy.ndarray):
    @classmethod
    def from_str(cls, rgbstr):
        return numpy.array([int(rgbstr[i:i+2], 16) for i in range(1, len(rgbstr), 2)]).view(cls)
 
    def __str__(self):
        self = self.astype(numpy.int16)
        return '#' + ''.join("00" if n < 0 else "0"+format(n, 'x') if n < 16 else format(n, 'x') if n < 256 else "FF" for n in self)

    def brighten(self):
        self[:] = (7*self)/6

    def darken(self):
        self[:] = (6*self)/7

def complement(color):
    white, color = RGB.from_str("#FFFFFF"), RGB.from_str(color)
    return white - color

def halfway(a, b):
	c1, c2 = RGB.from_str(a), RGB.from_str(b)
	return (c1 + c2) / 2

def color_minus(a, b):
    c1, c2 = RGB.from_str(a), RGB.from_str(b)
    return c1 - c2

def color_add(a, b):
    c1, c2 = RGB.from_str(a), RGB.from_str(b)
    return c1 + c2

def array_add(a, b):
    return [a[channel]+b[channel] for channel in range(3)]

def unfaithfulify(a):
    #watch out: the return value can be negative!
    if a == "#FFFFFF":
        subtrahend = RGB.from_str("#000000")
    else:
        subtrahend = RGB.from_str("#0F0F0F")
    a = RGB.from_str(a)
    a.darken()
    return a - subtrahend

def score(before, additionally):
    ret = 0
    for channel in range(3):
        ret += (255 - before[channel]) * additionally[channel]
    return ret
