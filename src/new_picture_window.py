import Tkinter as tk
import tkMessageBox
import time
import display, json_read_write

class Config_Dialog(tk.Toplevel):

    def __init__(self, app, p_f, nx, ny):
        tk.Toplevel.__init__(self)
        self.init(app, p_f, nx, ny)

    def init(self, app, p_f, nx, ny):
        self.title("Configure picture settings")
        self.loaded = False
        self.picture_file, self.app = p_f, app
        self.new_json_file = self.picture_file.rsplit("/", 1)[0] + "/" + "weave " + str(time.strftime('%c')) + ".json"
        
        self.color_variable = tk.StringVar()
        self.color_variable.set("bw")
        self.two_sided_variable = tk.BooleanVar()
        self.two_sided_variable.set(True)
        self.nailsx, self.nailsy = nx, ny
        
        self.entry_width = 4
        self.steps_done = 0
        self.steps = []
        
        self.transient(self.app)
        self.grab_set()
        self.place_widgets()

    def place_widgets(self):
        self.show_ok_cancel()
        self.show_right_side()
        self.show_canvas()

    def show_canvas(self):
        self.canvas_pic = tk.Canvas(self, bg="white", height = 1, width = 1)
        display.load(self, [self.canvas_pic], self.picture_file, max(1, int(self.entry_x.get())), max(1, int(self.entry_y.get())), [])
        self.canvas_pic.grid(column=0, row=0)
        self.loaded = True

    def is_Okay(self, text_after, is_y):
        if not ((text_after.isdigit() and int(text_after) <= 500) or text_after == ""):
            return False
        if self.loaded:
            if is_y:
                x, y = self.entry_x.get(), text_after
            else:
                x, y = text_after, self.entry_y.get()
            if x == "":
                x = "1"
            if y == "":
                y = "1"
            display.load(self, [self.canvas_pic], self.picture_file, max(1, int(x)), max(1, int(y)), [])
        return True


    def show_right_side(self):
        self.field_frame = tk.Frame(self)
        self.field_frame.grid(column=1, row=0, padx=self.app.x_padding, pady=self.app.y_padding)
        self.show_input_fields()
        self.show_radio_buttons()

    def show_input_fields(self):
        okay_command = self.field_frame.register(self.is_Okay)
        
        tk.Label(self.field_frame, text="#horizontal nails").grid(row=0, column = 0, sticky=tk.W)
        tk.Label(self.field_frame, text="#vertical nails").grid(row=1, column = 0, sticky=tk.W)
        self.entry_x = tk.Entry(self.field_frame, width=self.entry_width, validate='key', validatecommand=(okay_command, '%P', False))
        self.entry_x.grid(row=0, column=1)
        self.entry_y = tk.Entry(self.field_frame, width=self.entry_width, validate='key', validatecommand=(okay_command, '%P', True))
        self.entry_y.grid(row=1, column=1)
        self.entry_x.insert(0, str(self.nailsx))
        self.entry_y.insert(0, str(self.nailsy))

    def show_radio_buttons(self):
        tk.Label(self.field_frame, text="Color mode:").grid(row=2, column=0, sticky=tk.W)
        self.bw_button = tk.Radiobutton(self.field_frame, text = "black/white", variable=self.color_variable, value="bw")
        self.gr_button = tk.Radiobutton(self.field_frame, text = "gray scale", state=tk.DISABLED, variable=self.color_variable, value="gray")
        self.rg_button = tk.Radiobutton(self.field_frame, text = "rgb", state=tk.DISABLED, variable=self.color_variable, value="rgb")
        self.bw_button.grid(padx=self.app.button_padding, sticky=tk.W)
        self.gr_button.grid(padx=self.app.button_padding, sticky=tk.W)
        self.rg_button.grid(padx=self.app.button_padding, sticky=tk.W)
        tk.Label(self.field_frame, text="Nail sides:").grid(row=6, column=0, sticky=tk.W)
        self.two_sided_button = tk.Radiobutton(self.field_frame, text = "Two sided nails", variable=self.two_sided_variable, value=True)
        self.one_sided_button = tk.Radiobutton(self.field_frame, text = "One sided nails", state = tk.DISABLED, variable=self.two_sided_variable, value = False)
        self.two_sided_button.grid(padx=self.app.button_padding, sticky=tk.W)
        self.one_sided_button.grid(padx=self.app.button_padding, sticky=tk.W)


    def show_nailsx_variabley(self):
        pass

    def ok(self):
        if self.entry_x.get() == "" or self.entry_y.get() == "":
            tkMessageBox.showerror("Error!", "The nail numbers must both contain a number!", parent=self)
            return
        json_read_write.write(self.new_json_file, max(1, int(self.entry_x.get())), max(1, int(self.entry_y.get())), self.steps_done, self.two_sided_variable.get(), self.color_variable.get(), self.steps, self.picture_file)
        self.app.json_file = self.new_json_file
        self.app.load(self.new_json_file)
        self.destroy()
        
    def quit(self):
        self.app.json_file = None
        self.destroy()

    def show_ok_cancel(self):
        self.button_frame = tk.Frame(self)
        self.button_frame.grid(column=0, row=1, columnspan=2, padx=self.app.x_padding, pady=self.app.y_padding, sticky=tk.S)
        self.ok_button = tk.Button(self.button_frame, text='Use these settings', command=self.ok)
        self.ok_button.grid(column=0, row=0, padx=self.app.button_padding)
        self.cancel_button = tk.Button(self.button_frame, text='Cancel', command=self.quit)
        self.cancel_button.grid(column=1, row=0, padx=self.app.button_padding)
