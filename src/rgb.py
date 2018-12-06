import numpy

class RGB(numpy.ndarray):
    @classmethod
    def from_str(cls, rgbstr):
        return numpy.array([int(rgbstr[i:i+2], 16) for i in range(1, len(rgbstr), 2)]).view(cls)
 
    def __str__(self):
        #self = self.astype(numpy.uint8)
        return '#' + ''.join("00" if n < 0 else "0"+format(n, 'x') if n < 16 else format(n, 'x') for n in self)


def complement(color):
    white, color = RGB.from_str("#FFFFFF"), RGB.from_str(color)
    return str(white - color)

def halfway(a, b):
	c1, c2 = RGB.from_str(a), RGB.from_str(b)
	return str((c1 + c2) / 2)

def color_minus(a, b):
    c1, c2 = RGB.from_str(a), RGB.from_str(b)
    return str(c1 - c2)
