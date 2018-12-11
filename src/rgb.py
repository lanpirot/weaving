import numpy

class RGB(numpy.ndarray):
    @classmethod
    def from_str(cls, rgbstr):
        return numpy.array([int(rgbstr[i:i+2], 16) for i in range(1, len(rgbstr), 2)]).view(cls)
 
    def __str__(self):
        self = self.astype(numpy.int16)
        return '#' + ''.join("00" if n < 0 else "0"+format(n, 'x') if n < 16 else format(n, 'x') if n < 256 else "FF" for n in self)

    def brighten(self):
        self[:] = (4*self)/3

    def darken(self):
        self[:] = (3*self)/4

def complement(color):
    white, color = RGB.from_str("#FFFFFF"), RGB.from_str(color)
    return str(white - color)

def halfway(a, b):
	c1, c2 = RGB.from_str(a), RGB.from_str(b)
	return str((c1 + c2) / 2)

def color_minus(a, b):
    c1, c2 = RGB.from_str(a), RGB.from_str(b)
    return str(c1 - c2)

def color_add(a, b):
    c1, c2 = RGB.from_str(a), RGB.from_str(b)
    return str(c1 + c2)

def color_add_unfaithful(a, b):
    '''
    Color b is unfaithfully added to color a. Every color channel of b is multiplied with 3/4 
    and 30 is subtracted afterwards. (These are arbitrary values).
    Let color b = "#FF1200" -> b = [255, 18, 0], then the summand b_unfaithful = [140, -17, -30].
    '''
    c1, c2 = RGB.from_str(a), RGB.from_str(b)
    subtrahend = RGB.from_str("#1E1E1E")
    c2.darken()
    c2_unfaithful = c2 - subtrahend
    return str(c1 + c2_unfaithful)
