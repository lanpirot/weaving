
# -*- coding: utf-8 -*-
#open folder button
#2. pic inside: display pic, ask for dimensions and colors and create empty .steps
#3. pic and .steps inside: display pic, or lines with slider and step forward/backward, pic-lines with slider
#   button for more steps in background
#reload content button

#!/usr/bin/env python
import Tkinter as tk
import tkFileDialog as file_dialog
import rgb, display, json_read_write



class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.init_values()
        self.create_widgets()
    
    def init_values(self):
        #values of the menu itself
        self.main_color = self.cget('bg')
        self.red = "#FF0000"
        self.halfred = rgb.halfway(self.main_color, self.red)
        self.quarred = rgb.halfway(self.main_color, self.halfred)
        self.green = "#00FF00"
        self.halfgreen = rgb.halfway(self.main_color, self.green)
        self.quargreen = rgb.halfway(self.main_color, self.halfgreen)
        #standard values of the picture and the weaving
        self.nailsx = 100
        self.nailsy = 100
        self.two_sided_nail = True
        self.color_scheme = "bw"
        self.steps = []

    
    def open_file(self):
        self.file = file_dialog.askopenfilename(title='Choose picture to weave or finished weaving.json',filetypes=[("JSON","*.json"),("JSON","*.JSON"),("JPG","*.JPG"),("JPG","*.jpeg"),("JPG","*.jpg")], initialdir="weaves/example")
        if self.file:
            if self.file.partition(".")[2].lower() == "json":
                self.json_file = self.file
                (self.nailsx, self.nailsy, self.two_sided_nail, self.color_scheme, self.steps, self.picture_file) = json_read_write.read_json(self.json_file)
                self.reload_button.config(state=tk.ACTIVE)
                self.nails = []
                display.load(self, self.canvas_pic, self.canvas_pos, self.canvas_neg, self.picture_file, self.nailsx, self.nailsy, self.nails)
                return
            elif self.file.partition(".")[2].lower() in ["jpeg", "jpg"]:
                self.picture_file = self.file
                #TODO: Pop-up menu showing the picture and updating the nailx/naily
                print "JSON creation not supported yet"
                return
            print "File type not recognized:", self.file.partition(".")[2].lower(), "of file", self.file
        else:
            print "No file chosen"
    
    def start(self):
        pass
    
    def reload(self):
        pass
    
    def place_buttons(self):
        self.quit_button = tk.Button(self, text='Quit', command=self.quit, bg=self.quarred, activebackground=self.halfred)
        self.quit_button.grid(column=0, row=2, padx=10)
        self.open_dialog_button = tk.Button(self, text='Open file', command=self.open_file)
        self.open_dialog_button.grid(column=1, row=2, padx=10)
        self.reload_button = tk.Button(self, text="Reload", command=self.reload, state=tk.DISABLED)
        self.reload_button.grid(column=2, row=2, padx=10)
        self.start_button = tk.Button(self, text="Start/Continue weaving", command=self.start, bg=self.quargreen, activebackground=self.halfgreen, state = tk.DISABLED)
        self.start_button.grid(column=3, row=2, padx=10)
        
    
    def place_canvasses(self):
        self.canvas_pic = tk.Canvas(self, bg="white", height = 200, width = 200)
        self.canvas_pic.grid(column=0, row=0)	        
        self.canvas_pos = tk.Canvas(self, bg="white", height = 200, width = 200)
        self.canvas_pos.grid(column=1, row=0)
        self.canvas_neg = tk.Canvas(self, bg="white", height = 200, width = 200)
        self.canvas_neg.grid(column=2, row=0)
        #TODO: tool tip for mouse over "original picture" "weaved picture" "original picture - weaved picture"
        
    def moved(self, pos):
        #TODO: update sheet to new scroll_bar position
        return    
        
    def place_scroll_bar(self):
        self.scroll_bar = tk.Scrollbar(self, orient=tk.HORIZONTAL, jump=1, command=self.moved)
        self.scroll_bar.grid(column=0, columnspan=4, row=1, sticky=tk.W+tk.E)

    def create_widgets(self):
        self.place_canvasses()
        self.place_buttons()
        self.place_scroll_bar()

app = Application()
app.master.title('Weave your pictures!')
app.mainloop()
