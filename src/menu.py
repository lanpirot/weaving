# -*- coding: utf-8 -*-
#!/usr/bin/env python
import Tkinter as tk
import tkFileDialog as file_dialog
import rgb, display, json_read_write
from tkintertable import TableCanvas, TableModel


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
        self.button_padding = 10
        #standard values of the picture and the weaving
        self.nailsx = 100
        self.nailsy = 100
        self.steps_done = 0
        self.two_sided_nail = True
        self.color_scheme = "bw"
        self.steps = []

    
    def open_file(self):
        self.file = file_dialog.askopenfilename(title='Choose picture to weave or finished weaving.json',filetypes=[("JSON","*.json"),("JSON","*.JSON"),("JPG","*.JPG"),("JPG","*.jpeg"),("JPG","*.jpg")], initialdir="weaves/example")
        if self.file:
            if self.file.partition(".")[2].lower() == "json":
                self.load(self.file)
                return
            elif self.file.partition(".")[2].lower() in ["jpeg", "jpg"]:
                self.picture_file = self.file
                #TODO: Pop-up menu showing the picture and updating the nailx/naily
                print "JSON creation not supported yet"
                return
            raise Exception("File type not recognized:", self.file.partition(".")[2].lower(), "of file", self.file)
        else:
            print "No file chosen"

        #json_read_write.update_steps(self.file, self.steps)
    
    def start(self):
        pass
    
    def load(self, json_file):
        #if thread is running dump it into (old) .json_file
        #read (new) .json_file
        #load the three canvasses
        #update table content
        self.table.model.deleteRows(xrange(len(self.steps)))
        self.json_file = json_file
        self.reload_table(0)
        (self.nailsx, self.nailsy, self.steps_done, self.two_sided_nail, self.color_scheme, self.steps, self.picture_file) = json_read_write.read_json(json_file)
        self.nails = []
        display.load(self, self.canvas_pic, self.canvas_pos, self.canvas_neg, self.picture_file, self.nailsx, self.nailsy, self.nails)
        for s in xrange(self.steps_done):
            stepnail1, stepnail2 = self.steps[s]
            self.canvas_pos.create_line(stepnail1[1][0], stepnail1[1][1], stepnail2[1][0], stepnail2[1][1])
        self.reload_button.config(state=tk.ACTIVE)
    
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
        
        
    
    def place_buttons(self):
        self.quit_button = tk.Button(self, text='Quit', command=self.quit, bg=self.quarred, activebackground=self.halfred)
        self.quit_button.grid(column=0, row=2, padx=self.button_padding)
        self.open_dialog_button = tk.Button(self, text='Open file', command=self.open_file)
        self.open_dialog_button.grid(column=1, row=2, padx=self.button_padding)
        self.reload_button = tk.Button(self, text="Reload table", command=self.reload_table, state=tk.DISABLED)
        self.reload_button.grid(column=2, row=2, padx=self.button_padding)
        self.start_button = tk.Button(self, text="Start/Continue weaving", command=self.start, bg=self.quargreen, activebackground=self.halfgreen, state = tk.DISABLED)
        self.start_button.grid(column=3, row=2, padx=self.button_padding)
        
    
    def place_canvasses(self):
        self.canvas_pic = tk.Canvas(self, bg="white", height = 200, width = 200)
        self.canvas_pic.grid(column=0, row=0)	        
        self.canvas_pos = tk.Canvas(self, bg="white", height = 200, width = 200)
        self.canvas_pos.grid(column=1, row=0)
        self.canvas_neg = tk.Canvas(self, bg="white", height = 200, width = 200)
        self.canvas_neg.grid(column=2, row=0)
        #TODO: tool tip for mouse over "original picture" "weaved picture" "original picture - weaved picture"
    
    def place_table(self):
        self.tframe = tk.Frame(self, width=460, height=130)
        self.tframe.grid(column=0, row = 1, columnspan=3)
        self.tframe.grid_propagate(0)
        self.table = TableCanvas(self.tframe, rows=0, cols=0, read_only=True)
        self.table.show()
        self.table.addColumn(newname="From")
        self.table.addColumn(newname="NESW")
        self.table.addColumn(newname="to")
        self.table.addColumn(newname="nesw")

    def create_widgets(self):
        self.place_canvasses()
        self.place_buttons()
        self.place_table()

app = Application()
app.master.title('Weave your pictures!')
app.mainloop()
