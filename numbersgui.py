from PIL import Image
from tkinter import *

class NumbersGUI():
    def __init__(self, master=None):
        self.master = master
        self.master.geometry('{}x{}'.format(550, 554))
        self.create_widgets()


        # mouse coordinates
        self.x = 0
        self.y = 0

    def create_widgets(self):

        # top and bottom row frames
        self.top_frame = Frame(self.master, bg='lavender', width=550, height=150)
        self.btm_frame = Frame(self.master, bg='lavender', width=550, height=400)

        self.top_frame.grid(row=0, sticky='ew')
        self.btm_frame.grid(row=1, sticky='ew')

        # left and right for each row
        self.funcs = Frame(self.top_frame, bg='lavender', width=400, height=150, padx=3, pady=3)
        self.mini_display = Frame(self.top_frame, bg='lavender', width=150, height=150, padx=3, pady=3)
        self.funcs.grid(row=0, column=0, sticky='nsew')
        self.mini_display.grid(row=0, column=1, sticky='nsew')

        self.drawing_area = Canvas(self.btm_frame, bg='black', width=400, height=400)
        self.answer_display = Frame(self.btm_frame, bg='lavender', width=150, height=400, padx=3, pady=3)
        self.drawing_area.grid(row=0, column=0, sticky='nsew')
        self.answer_display.grid(row=0, column=1,  sticky='nsew')

        # add borders
        self.mini_display.config(highlightbackground='black', highlightthickness=2)

        """
        self.funcs.grid(row=0, column=0, sticky='nw')
        self.mini_display.grid(row=0, column=1,  sticky='ne')
        self.drawing_area.grid(row=1, column=0, sticky='sw')
        self.answer_display.grid(row=1, columns=1, sticky='se')

        
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.pack(side="bottom")
        """


root = Tk()
root.title("Guessing Numbers")
gui = NumbersGUI(master=root)
root.mainloop()

"""
from PIL import Image
img = Image.open('image.png').convert('LA')
img.save('greyscale.png')
"""