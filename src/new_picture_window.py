import Tkinter as tk
import time
import display, json_read_write


Window = 0
button_padding = 10

new_json_file = "weave " + str(time.strftime('%c'))
nailsx = 0
nailsy = 0
steps_done = 0
two_sided_nail = True
color_scheme = ""
steps = []
picture_file = ""


def window(app, p_f, nx, ny):
    global Window, nailsx, nailsy, two_sided_nail, color_scheme, steps, picture_file
    picture_file, nailsx, nailsy = p_f, nx, ny
    Window = tk.Toplevel(app)
    canvas_pic = tk.Canvas(Window, bg="white", height = 200, width = 200)
    display.load(Window, [canvas_pic], picture_file, nailsx, nailsy, [])
    canvas_pic.grid(column=0, row=0)
    show_ok_cancel()



def show_nailsxy():
    pass

def ok():
    global new_json_file, nailsx, nailsy, steps_done, two_sided_nail, color_scheme, steps, picture_file
    Window.destroy()
    json_read_write.write(new_json_file, nailsx, nailsy, steps_done, two_sided_nail, color_scheme, steps, picture_file)
    return new_json_file
    
def quit():
    Window.destroy()
    return None
    

def show_ok_cancel():
     ok_button = tk.Button(Window, text='Ok', command=ok)
     ok_button.grid(column=0, row=1, padx=button_padding)
     cancel_button = tk.Button(Window, text='Cancel', command=quit)
     cancel_button.grid(column=1, row=1, padx=button_padding)
