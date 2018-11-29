import Tkinter as tk
import time
import display, json_read_write


Window = 0
button_padding = 10

new_json_file = ""
nailsx = 0
nailsy = 0
steps_done = 0
two_sided_nail = True
color_scheme = ""
steps = []
picture_file = ""
_app = 0
entry_width = 4




def window(app, p_f, nx, ny):
    global Window, nailsx, nailsy, two_sided_nail, color_scheme, steps, picture_file, _app, new_json_file
    picture_file, nailsx, nailsy, _app = p_f, nx, ny, app
    new_json_file = picture_file.rsplit("/", 1)[0] + "/" + "weave " + str(time.strftime('%c')) + ".json"
    Window = tk.Toplevel(app)
    place_widgets()

def place_widgets():
    canvas_pic = tk.Canvas(Window, bg="white", height = 200, width = 200)
    display.load(Window, [canvas_pic], picture_file, nailsx, nailsy, [])    
    canvas_pic.grid(column=0, row=0)
    show_ok_cancel()
    show_input_fields()
    

def show_input_fields():
    field_frame = tk.Frame(Window)
    field_frame.grid(column=1,row=0, padx=_app.x_padding, pady=_app.y_padding)
    tk.Label(field_frame, text="#horizontal nails").grid(row=0, column = 0, sticky=tk.W)
    tk.Label(field_frame, text="#vertical nails").grid(row=1, column = 0, sticky=tk.W)
    entry_x = tk.Entry(field_frame, width=entry_width)
    entry_x.grid(row=0, column=1)
    entry_y = tk.Entry(field_frame, width=entry_width)
    entry_y.grid(row=1, column=1)
    entry_x.insert(0, str(nailsx))
    entry_y.insert(0, str(nailsy))
    

def show_nailsxy():
    pass

def ok():
    global new_json_file, nailsx, nailsy, steps_done, two_sided_nail, color_scheme, steps, picture_file
    Window.destroy()
    json_read_write.write(new_json_file, nailsx, nailsy, steps_done, two_sided_nail, color_scheme, steps, picture_file)
    _app.json_file = new_json_file
    _app.load(new_json_file)
    
def quit():
    Window.destroy()
    _app.json_file = None
    

def show_ok_cancel():
    button_frame = tk.Frame(Window)
    button_frame.grid(column=0, row=1, columnspan=2, padx=_app.x_padding, pady=_app.y_padding, sticky=tk.S)
    ok_button = tk.Button(button_frame, text='Ok', command=ok)
    ok_button.grid(column=0, row=0, padx=button_padding)
    cancel_button = tk.Button(button_frame, text='Cancel', command=quit)
    cancel_button.grid(column=1, row=0, padx=button_padding)
