# -*- coding: utf-8 -*-
#!/usr/bin/env python
import Tkinter as tk
import tkFont
import tkFileDialog as file_dialog
import rgb, display, json_read_write, new_picture_window, crunch_pic
from tkintertable import TableCanvas, TableModel
import threading, logging, time
import ttk


class Application(tk.Tk):
    """A window for users to recreate their picture with nails and threads. Steps to re-weave are proposed, so that the picture 
    will be recreated. The computation is done in an extra thread. The steps can be saved/loaded in a companioning .json file to
    the picture."""
    
    def __init__(self):
        tk.Tk.__init__(self)
        self.init_values()
        self.create_widgets()
        self.create_daemon()
    
    def create_daemon(self):
        self.weave_daemon = crunch_pic.weave_thread(self, "")
        self.weave_daemon.setDaemon(True)
    
    def start_daemon(self):
        self.weave_daemon.json_file = self.json_file
        if self.weave_daemon.is_alive():
            raise Exception("Daemon is still alive!")
            self.weave_daemon.join()
            self.weave_daemon.restart()
        else:
            self.weave_daemon.start()
    
    def on_closing(self):
        if self.weave_daemon.is_alive():
            self.weave_daemon.save_now()
            time.sleep(0.1)
        else:
            logging.debug("No weave daemon found!")
        self.destroy()
    
    def init_values(self):
        """Some values are loaded. Some for an initial .json-creation."""
        #values of the menu itself
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        style = ttk.Style(self)
        style.theme_use('clam')
        self.default_font = tkFont.nametofont("TkDefaultFont")
        self.default_font.configure(size=11)
        self.option_add("*Font", self.default_font)
        self.main_color = self.cget('bg')
        self.red = "#BB2222"
        self.halfred = str(rgb.halfway(self.main_color, self.red))
        self.quarred = str(rgb.halfway(self.main_color, self.halfred))
        self.green = "#22BB22"
        self.halfgreen = str(rgb.halfway(self.main_color, self.green))
        self.quargreen = str(rgb.halfway(self.main_color, self.halfgreen))
        self.x_padding = 5
        self.y_padding = 5
        self.button_padding = 10
        self.mark = tk.IntVar()
        self.mark.set(1)
        self.resizable(0,0)
        #standard values of the picture and the weaving
        self.nailsx = 100
        self.nailsy = 100
        self.steps_done = 0
        self.two_sided_nail = True
        self.color_scheme = "bw"
        self.steps = []
        self.current_step = -1
    
    def open_file(self):
        """
        The File open menu has been clicked. The user gets to choose a existing project (a .json) which they can view or 
        compute new steps in. Otherwise the user choses a .jpg and the .json will be created from scratch, after a prompt 
        asking for some parameters.
        """
        self.file = file_dialog.askopenfilename(title='Choose picture to weave or finished weaving.json',filetypes=[("JSON","*.json"),("JSON","*.JSON"),("JPG","*.JPG"),("JPG","*.jpeg"),("JPG","*.jpg")], initialdir="weaves/example")
        if self.file:
            if self.file.partition(".")[2].lower() == "json":
                self.load(self.file)
                return
            elif self.file.partition(".")[2].lower() in ["jpeg", "jpg"]:
                self.picture_file = self.file
                new_picture_window.Config_Dialog(self, self.picture_file, self.nailsx, self.nailsy)
                return
            raise Exception("File type not recognized:", self.file.partition(".")[2].lower(), "of file", self.file)
    
    def load(self, json_file):
        #if thread is running dump it into (old) .json_file and exit it
        #read (new) .json_file
        #load the two canvasses
        #update table content
        self.current_step = -1
        self.tframe.destroy()
        self.place_table()
        self.json_file = json_file
        (self.nailsx, self.nailsy, self.steps_done, self.two_sided_nail, self.color_scheme, self.steps, self.picture_file) = json_read_write.read_json(json_file)
        self.start_daemon()
        self.reload_table(0)
        self.table.setSelectedRow(-1)
        display.load([(0, self.canvas_pic), (1, self.canvas_pos)], self.picture_file, self.nailsx, self.nailsy)
        for button in [self.start_button, self.back_button, self.play_button, self.end_button]:
            button.config(state=tk.ACTIVE)
    
    def reload_table(self, already_loaded=-1):
        while self.steps and type(self.steps[0]) == type([]):
            if not self.steps:
                return
            time.sleep(0.01)
        if already_loaded < 0:
            already_loaded = len(self.steps)
        for e, row in enumerate(self.steps[already_loaded:]):
            self.add_row_to_table(e, row)
        self.table.adjustColumnWidths()
        self.table.autoResizeColumns()
        self.table.redrawVisible()

    def add_row_to_table(self, e, row):
        r = self.table.addRow(key="Step "+str(e+1))
        nail1, nail2 = row
        self.table.model.setValueAt(str(nail1.number), e, 0)
        self.table.model.setValueAt(nail1.direction, e, 1)
        self.table.model.setValueAt(str(nail2.number), e, 2)
        self.table.model.setValueAt(nail2.direction.lower(), e, 3)

    def new_row(self, e, row):
        self.add_row_to_table(e, row)
        self.mark_current_row()
    
    def back_to_start(self):
        """User pressed back_to_start-button, and displays are reset."""
        if self.current_step >= 0:
            display.delete_lines(range(self.current_step+1))
            self.current_step = -1
            self.mark_current()

    def back_one_step(self):
        """User pressed back-button, and displays are reset and played back till one step before the current."""
        if self.current_step >= 0:
            display.delete_lines([self.current_step])
            self.current_step -= 1
            self.mark_current()

    def play_one_step(self):
        """User pressed forward-button, and displays are updated with the next step."""
        if self.current_step + 1 < len(self.steps):
            self.current_step += 1
            display.draw_lines([(self.current_step, self.steps[self.current_step])])
            self.mark_current()

    def play_to_end(self):
        """User pressed back-to-end-button, and displays are updated with the last step."""
        if self.current_step + 1 < len(self.steps):
            display.draw_lines([(k, self.steps[k]) for k in range(self.current_step + 1, len(self.steps))])
            self.current_step = len(self.steps) - 1
            self.mark_current()

    def mark_current_row(self):
        """Update the table with the current row, jump to it and highlight it. If no step has been perfomed no row will be highlighted."""
        self.table.set_yviews('moveto', max(0, float(self.current_step)/(len(self.steps)+0.5)))
        if self.current_step >= 0:
            self.table.setSelectedRow(self.current_step)
        else:
            self.table.setSelectedRow(-1)
        self.table.redrawVisible()
        
    
    def mark_current(self):
        """The row of the current step will be highlighted and shown in the table. If the user wants fat lines for the current step, 
        they will be drawn onto the canvas in fat and red."""
        self.mark_current_row()
        if self.mark.get() and self.current_step >= 0:
            display.draw_lines([(self.current_step, self.steps[self.current_step])], True)
        else:
            display.remove_marking()
    
    def place_buttons(self):
        """The play, back, to_end, to_start buttons are placed in the bottom."""
        self.button_frame = ttk.Frame(self)
        self.button_frame.grid(column=0, row=3, columnspan=2, padx=self.x_padding, pady=self.y_padding, sticky=tk.S)
        self.start_photo, self.back_photo, self.play_photo, self.end_photo = display.create_photos()
        
        self.start_button = ttk.Button(self.button_frame, command=self.back_to_start, image = self.start_photo, state=tk.DISABLED)
        self.start_button.grid(column=0, row=0, padx=self.button_padding)
        self.back_button = ttk.Button(self.button_frame, command=self.back_one_step, image = self.back_photo, state=tk.DISABLED)
        self.back_button.grid(column=1, row=0, padx=self.button_padding)
        self.play_button = ttk.Button(self.button_frame, command=self.play_one_step, image = self.play_photo, state=tk.DISABLED)
        self.play_button.grid(column=2, row=0, padx=self.button_padding)
        self.end_button = ttk.Button(self.button_frame, command=self.play_to_end, image = self.end_photo, state=tk.DISABLED)
        self.end_button.grid(column=3, row=0, padx=self.button_padding)
    
    def place_canvasses(self):
        """
           The three canvasses are placed. 
              The left (canvas_pic) is for the original photo.
              The right (canvopen_fileas_pos) is a view, of what the user should recreate themselves.
        """
        self.canvas_pic = tk.Canvas(self, bg="white", height = 200, width = 200)
        self.canvas_pic.grid(column=0, row=1, padx=self.x_padding, pady=self.y_padding)	        
        self.canvas_pos = tk.Canvas(self, bg="white", height = 200, width = 200)
        self.canvas_pos.grid(column=1, row=1, padx=self.x_padding, pady=self.y_padding)
    
    def place_table(self):
        """The table in the bottom describing the steps and their order."""
        self.tframe = ttk.Frame(self, width=460, height=130)
        self.tframe.grid(column=0, row = 2, columnspan=2, padx=self.x_padding, pady=self.y_padding)
        self.tframe.grid_propagate(0)
        self.table = TableCanvas(self.tframe, rows=0, cols=0, read_only=True, rowselectedcolor=self.quarred, editable=False)
        self.table.show()
        self.table.addColumn(newname="From")
        self.table.addColumn(newname="NESW")
        self.table.addColumn(newname="to")
        self.table.addColumn(newname="nesw")            

    def about(self):
        """The about window, that pops up, in the help context."""
        self.about_window = tk.Toplevel(self)
        self.about_window.title("About")
        self.about_window.resizable(0,0)
        self.about_window.geometry("250x170")
        self.about_frame = ttk.Frame(master=self.about_window)
        self.about_frame.pack_propagate(0)
        self.about_frame.pack(fill=tk.BOTH, expand=1)
        
        ttk.Label(self.about_frame, font= tkFont.Font(size=10, weight='bold'), width=240, wraplength=240, text="Copyright 2018 Alexander Boll", justify=tk.LEFT).pack(padx=5,pady=2)
        ttk.Label(self.about_frame, font= tkFont.Font(size=10), width=240, wraplength=240, text="This program can instruct you, how to weave a photo, with a couple of nails and a thread.\n\nYou can use and modify it for free, under the MIT license.", justify=tk.LEFT).pack(padx=5,pady=2)
        ttk.Button(self.about_frame, text="Ok", width=10, command=self.about_window.destroy).pack(pady=8)
        self.about_window.transient(self)
        self.about_window.grab_set()

    def place_menu(self):
        """The menu bar."""
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)
        
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label="Open file", command=self.open_file, font=self.default_font)
        self.file_menu.add_command(label="Start/continue weaving", command=self.create_daemon, background=self.quargreen, activebackground=self.halfgreen, state = tk.DISABLED, font=self.default_font)
        self.file_menu.add_command(label="Reload .json file", command=self.reload_table, state = tk.DISABLED, font=self.default_font)
        self.file_menu.add_command(label="Quit", command=self.quit, background=self.quarred, activebackground=self.halfred, font=self.default_font)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        
        self.view_menu = tk.Menu(self.menubar, tearoff=0)
        self.view_menu.add_checkbutton(label="Mark last move(s)", variable=self.mark, command=self.mark_current)
        self.menubar.add_cascade(label="View", menu=self.view_menu)        
        
        self.help_menu = tk.Menu(self.menubar, tearoff=0)
        self.help_menu.add_command(label="About", command=self.about)
        self.menubar.add_cascade(label="Help", menu=self.help_menu)

    def create_widgets(self):
        """The main parts of the app are created and placed on the grid of the window."""
        self.place_canvasses()
        self.place_table()
        self.place_buttons()
        self.place_menu()

app = Application()
app.title('Weave your pictures!')
app.mainloop()
