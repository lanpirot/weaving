# -*- coding: utf-8 -*-
#!/usr/bin/env python
import Tkinter as tk
import tkFont
import tkFileDialog as file_dialog
import rgb, display, json_read_write#, new_picture_window
from tkintertable import TableCanvas, TableModel


class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.init_values()
        self.create_widgets()
    
    def init_values(self):
        #values of the menu itself
        self.default_font = tkFont.nametofont("TkDefaultFont")
        self.default_font.configure(size=11)
        self.option_add("*Font", self.default_font)
        self.main_color = self.cget('bg')
        self.red = "#BB2222"
        self.halfred = rgb.halfway(self.main_color, self.red)
        self.quarred = rgb.halfway(self.main_color, self.halfred)
        self.green = "#22BB22"
        self.halfgreen = rgb.halfway(self.main_color, self.green)
        self.quargreen = rgb.halfway(self.main_color, self.halfgreen)
        self.x_padding = 5
        self.y_padding = 5
        self.button_padding = 10
        self.mark = tk.IntVar()
        self.mark.set(0)
        #standard values of the picture and the weaving
        self.nailsx = 100
        self.nailsy = 100
        self.steps_done = 0
        self.two_sided_nail = True
        self.color_scheme = "bw"#TODO: "grayscale" "rgb"
        self.steps = []
        self.current_step = -1

    
    def open_file(self):
        self.file = file_dialog.askopenfilename(title='Choose picture to weave or finished weaving.json',filetypes=[("JSON","*.json"),("JSON","*.JSON"),("JPG","*.JPG"),("JPG","*.jpeg"),("JPG","*.jpg")], initialdir="weaves/example")
        if self.file:
            if self.file.partition(".")[2].lower() == "json":
                self.load(self.file)
                return
            elif self.file.partition(".")[2].lower() in ["jpeg", "jpg"]:
                self.picture_file = self.file
                self.json_file = new_picture_window.window(app, self.picture_file, self.nailsx, self.nailsy)
                if self.json_file:
                    self.load(self.json_file)
                return
            raise Exception("File type not recognized:", self.file.partition(".")[2].lower(), "of file", self.file)
    
    def start(self):
        pass
    
    def load(self, json_file):
        #if thread is running dump it into (old) .json_file
        #read (new) .json_file
        #load the three canvasses
        #update table content
        self.current_step = -1
        self.tframe.destroy()
        self.place_table()
        self.json_file = json_file
        self.reload_table(0)
        self.table.setSelectedRow(-1)
        (self.nailsx, self.nailsy, self.steps_done, self.two_sided_nail, self.color_scheme, self.steps, self.picture_file) = json_read_write.read_json(json_file)
        self.nails = []
        display.load(self, [self.canvas_pic, self.canvas_pos, self.canvas_neg], self.picture_file, self.nailsx, self.nailsy, self.nails)
        self.file_menu.entryconfig("Reload .json file", state=tk.NORMAL)
        for button in [self.start_button, self.back_button, self.play_button, self.end_button]:
            button.config(state=tk.ACTIVE)
    
    def reload_table(self, already_loaded=-1):
        #if thread is running dump it into .json_file
        #read .json_file
        #update table content
        if already_loaded < 0:
            already_loaded = len(self.steps)
        new_steps = json_read_write.get_steps(self.json_file)
        for e, row in enumerate(new_steps[already_loaded:]):
            r = self.table.addRow(key="Step "+str(e+1))
            nail1, nail2 = row
            self.table.model.setValueAt(nail1[0][0], e, 0)
            self.table.model.setValueAt(nail1[0][1], e, 1)
            self.table.model.setValueAt(nail2[0][0], e, 2)
            self.table.model.setValueAt(nail2[0][1].lower(), e, 3)
        self.table.adjustColumnWidths()
        self.table.autoResizeColumns()
        self.table.redrawVisible()
        self.steps = new_steps

    def delete_markings_nactive(self):
        if self.mark.get():
            self.view_menu.entryconfig("Delete all markings", state=tk.NORMAL)
        else:
            self.view_menu.entryconfig("Delete all markings", state=tk.DISABLED)

    def delete_markings(self):
        if self.current_step >= 0:
            display.reload_from_start()
            display.draw_lines(self.steps[:self.current_step+1])
    
    def back_to_start(self):
        if self.current_step >= 0:
            display.reload_from_start()
            self.current_step = -1
            self.mark_current()

    def back_one_step(self):
        if self.current_step >= 0:
            display.reload_from_start()
            self.current_step -= 1
            display.draw_lines(self.steps[:self.current_step+1])
            self.mark_current()

    def play_one_step(self):
        if self.current_step + 1 < len(self.steps):
            self.current_step += 1
            display.draw_lines(self.steps[self.current_step:self.current_step+1])
            self.mark_current()

    def play_to_end(self):
        if self.current_step + 1 < len(self.steps):
            display.draw_lines(self.steps[self.current_step + 1:])
            self.current_step = len(self.steps) - 1
            self.mark_current()

    #TODO: show current table-row
    def mark_current_row(self):
        if self.current_step >= 0:
            self.table.setSelectedRow(self.current_step)
            #self.table.movetoSelectedRow(row="Step "+str(self.current_step))
        else:
            self.table.setSelectedRow(-1)
#           self.table.movetoSelectedRow(row="Step "+str(0))
        self.table.redrawVisible()
    
    def mark_current(self):
        self.mark_current_row()
        if self.mark.get():
            display.draw_lines(self.steps[self.current_step:self.current_step+1], True)
    
    def place_buttons(self):
        self.button_frame = tk.Frame(self)
        self.button_frame.grid(column=0, row=3, columnspan=3, padx=self.x_padding, pady=self.y_padding, sticky=tk.S)
        self.start_photo, self.back_photo, self.play_photo, self.end_photo = display.create_photos()
        
        self.start_button = tk.Button(self.button_frame, command=self.back_to_start, image = self.start_photo, state=tk.DISABLED)
        self.start_button.grid(column=0, row=0, padx=self.button_padding)
        self.back_button = tk.Button(self.button_frame, command=self.back_one_step, image = self.back_photo, state=tk.DISABLED)
        self.back_button.grid(column=1, row=0, padx=self.button_padding)
        self.play_button = tk.Button(self.button_frame, command=self.play_one_step, image = self.play_photo, state=tk.DISABLED)
        self.play_button.grid(column=2, row=0, padx=self.button_padding)
        self.end_button = tk.Button(self.button_frame, command=self.play_to_end, image = self.end_photo, state=tk.DISABLED)
        self.end_button.grid(column=3, row=0, padx=self.button_padding)
    
    def place_canvasses(self):
        self.canvas_pic = tk.Canvas(self, bg="white", height = 200, width = 200)
        self.canvas_pic.grid(column=0, row=1, padx=self.x_padding, pady=self.y_padding)	        
        self.canvas_pos = tk.Canvas(self, bg="white", height = 200, width = 200)
        self.canvas_pos.grid(column=1, row=1, padx=self.x_padding, pady=self.y_padding)
        self.canvas_neg = tk.Canvas(self, bg="white", height = 200, width = 200)
        self.canvas_neg.grid(column=2, row=1, padx=self.x_padding, pady=self.y_padding)
        #TODO: tool tip for mouse over "original picture" "weaved picture" "original picture - weaved picture (todo)"
    
    def place_table(self):
        self.tframe = tk.Frame(self, width=460, height=130)
        self.tframe.grid(column=0, row = 2, columnspan=3, padx=self.x_padding, pady=self.y_padding)
        self.tframe.grid_propagate(0)
        self.table = TableCanvas(self.tframe, rows=0, cols=0, read_only=True, rowselectedcolor=self.quarred, editable=False)
        self.table.show()
        self.table.addColumn(newname="From")
        self.table.addColumn(newname="NESW")
        self.table.addColumn(newname="to")
        self.table.addColumn(newname="nesw")

    def about(self):
        self.about_window = tk.Toplevel(self)
        self.about_window.title("About")
        self.about_window.resizable(0,0)
        self.about_window.geometry("250x160")
        self.about_frame = tk.Frame(master=self.about_window)
        self.about_frame.pack_propagate(0)
        self.about_frame.pack(fill=tk.BOTH, expand=1)
        
        tk.Label(self.about_frame, font= tkFont.Font(size=10, weight='bold'), width=240, wraplength=240, text="Copyright 2018 Alexander Boll", justify=tk.LEFT).pack(padx=5,pady=2)
        tk.Label(self.about_frame, font= tkFont.Font(size=10), width=240, wraplength=240, text="This program can instruct you, how to weave a photo, with a couple of nails and a thread.\n\nYou can use and modify it for free, under the MIT license.", justify=tk.LEFT).pack(padx=5,pady=2)
        tk.Button(self.about_frame, text="Ok", width=10, command=self.about_window.destroy).pack(pady=8)
        self.about_window.transient(self)
        self.about_window.grab_set()

    def place_menu(self):
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)
        
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label="Open file", command=self.open_file, font=self.default_font)
        self.file_menu.add_command(label="Start/continue weaving", command=self.start, background=self.quargreen, activebackground=self.halfgreen, state = tk.DISABLED, font=self.default_font)
        self.file_menu.add_command(label="Reload .json file", command=self.reload_table, state = tk.DISABLED, font=self.default_font)
        self.file_menu.add_command(label="Quit", command=self.quit, background=self.quarred, activebackground=self.halfred, font=self.default_font)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        
        self.view_menu = tk.Menu(self.menubar, tearoff=0)
        self.view_menu.add_checkbutton(label="Mark last move", variable=self.mark, command=self.delete_markings_nactive)
        self.view_menu.add_command(label="Delete all markings", command=self.delete_markings, state=tk.DISABLED)
        self.menubar.add_cascade(label="View", menu=self.view_menu)
        
        
        self.help_menu = tk.Menu(self.menubar, tearoff=0)
        self.help_menu.add_command(label="About", command=self.about)
        self.menubar.add_cascade(label="Help", menu=self.help_menu)

    def create_widgets(self):
        self.place_canvasses()
        self.place_table()
        self.place_buttons()
        self.place_menu()

app = Application()
app.title('Weave your pictures!')
app.mainloop()
