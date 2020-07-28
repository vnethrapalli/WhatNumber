from PIL import Image as Img
from PIL import ImageTk
from tkinter import *
import numpy as np
from predictor import NumberClassifier
import os

class NumbersGUI():
    def __init__(self, master=None):
        self.master = master
        self.master.geometry('{}x{}'.format(554, 554))

        # mouse coordinates
        self.x = 0
        self.y = 0

        # colored grid
        self.img_dim = 20
        self.img = np.zeros((self.img_dim, self.img_dim))

        # neural net classifier
        self.classifier = NumberClassifier()

        self.pen_color = '#000000'

        self.create_widgets()

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

        self.canvas = Canvas(self.btm_frame, bg='#000000', width=400, height=400)
        self.answer_display = Frame(self.btm_frame, bg='lavender', width=150, height=400, padx=3, pady=3)
        self.canvas.grid(row=0, column=0, sticky='nsew')
        self.answer_display.grid(row=0, column=1,  sticky='nsew')

        # add borders
        self.mini_display.config(highlightbackground='#000000', highlightthickness=2)

        # add grayscale color slider (+ labels for the top left segment)
        Label(self.funcs, text='grayscale float value', bg='lavender', font=(24)).grid(row=0, column=0)
        self.color_slider = Scale(self.funcs, from_=0.0, to_=1.0, resolution=0.01, orient=HORIZONTAL, bg='lavender', command=self.adjust_color)
        self.color_slider.grid(row=1, column=0, ipadx=145, ipady=20)
        self.curr_color = Label(self.funcs, text='             ', bg=self.pen_color, font=(24)).grid(row=2, column=0)

        # canvas actions
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<Button-1>", self.draw)

        self.canvas.bind('<ButtonRelease-1>', self.update)

        # reset canvas button
        self.reset_bttn = Button(self.answer_display, bg='lavender', text='reset canvas', command=self.reset_canvas)
        self.reset_bttn.place(relx=0.5, rely=0.9, anchor=CENTER)

        # labels for the predictions
        Label(self.answer_display, text='predicted number:', bg='lavender', padx = 20, pady=10).grid(row=0, column=1)
        Label(self.answer_display, text='???', bg='lavender', padx=20, font=(48), anchor=CENTER).grid(row=1, column=1)

        # puts the image in the mini display
        im = Img.fromarray(255 * self.img.T)
        im = im.convert('RGB')
        im.save('nums/num.png')
        self.pic = ImageTk.PhotoImage(Img.open('nums/num.png'))
        self.mini_img = Label(self.mini_display, image=self.pic)
        self.mini_img.place(relx=0.5, rely=0.5, anchor=CENTER)


    def adjust_color(self, val):
        hex_val = str(hex(int(float(val[:5]) * 255)))[2:]
        if len(hex_val) == 1:
            hex_val = '0' + hex_val

        self.pen_color = '#' + 3 * hex_val
        Label(self.funcs, text='             ', bg=self.pen_color, font=(24)).grid(row=2, column=0)


    def draw(self, event):
        xpt = event.x - (event.x % self.img_dim)
        ypt = event.y - (event.y % self.img_dim)
        self.canvas.create_rectangle(xpt, ypt, xpt + self.img_dim, ypt + self.img_dim, fill=self.pen_color, outline='')

        # update color matrix
        color_float = int(self.pen_color[-2:], 16) / 255
        self.img[xpt // self.img_dim][ypt // self.img_dim] = color_float

    def update(self, event):
        # update current prediction
        guess = self.classifier.classify(self.img.T.flatten())
        Label(self.answer_display, text=str(guess), bg='lavender', padx=20, font=(48), anchor=CENTER).grid(row=1, column=1)

        im = Img.fromarray(255 * self.img.T)
        im = im.convert('RGB')
        im.save('nums/num.png')
        self.pic = ImageTk.PhotoImage(Img.open('nums/num.png'))
        self.mini_img = Label(self.mini_display, image=self.pic)
        self.mini_img.place(relx=0.5, rely=0.5, anchor=CENTER)

    def reset_canvas(self):
        self.img = np.zeros((self.img_dim, self.img_dim))
        self.canvas.delete('all')
        Label(self.answer_display, text='???', bg='lavender', padx=20, font=(48), anchor=CENTER).grid(row=1, column=1)


root = Tk()
root.title("Guessing Numbers")
gui = NumbersGUI(master=root)
root.mainloop()
