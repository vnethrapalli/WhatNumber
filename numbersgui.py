from PIL import Image as Img
from PIL import ImageTk
from tkinter import *
import numpy as np
from predictor import NumberClassifier
import os


class NumbersGUI:
    def __init__(self, master=None):
        self.master = master

        self.img_dim = 28
        self.pix_dim = 15
        self.menubar_thickness = 150
        self.master.geometry('{}x{}'.format(self.pix_dim * self.img_dim + self.menubar_thickness + 4, self.pix_dim * self.img_dim + self.menubar_thickness + 4))

        # colored grid
        self.img = np.zeros((self.img_dim, self.img_dim))

        # neural net classifier
        self.classifier = NumberClassifier()

        self.pen_color = '#000000'
        self.faded_pen = '#000000'

        self.create_widgets()


    def create_widgets(self):
        # top and bottom row frames
        self.top_frame = Frame(self.master, bg='lavender', width=self.pix_dim * self.img_dim + self.menubar_thickness, height=self.menubar_thickness)
        self.btm_frame = Frame(self.master, bg='lavender', width=self.pix_dim * self.img_dim + self.menubar_thickness, height=self.pix_dim * self.img_dim)

        self.top_frame.grid(row=0, sticky='ew')
        self.btm_frame.grid(row=1, sticky='ew')

        # left and right for each row
        self.funcs = Frame(self.top_frame, bg='lavender', width=self.pix_dim * self.img_dim, height=self.menubar_thickness, padx=3, pady=3)
        self.mini_display = Frame(self.top_frame, bg='lavender', width=self.menubar_thickness, height=self.menubar_thickness, padx=3, pady=3)
        self.funcs.grid(row=0, column=0, sticky='nsew')
        self.mini_display.grid(row=0, column=1, sticky='nsew')

        self.canvas = Canvas(self.btm_frame, bg='#000000', width=self.pix_dim * self.img_dim, height=self.pix_dim * self.img_dim)
        self.answer_display = Frame(self.btm_frame, bg='lavender', width=self.menubar_thickness, height=self.pix_dim * self.img_dim, padx=3, pady=3)
        self.canvas.grid(row=0, column=0, sticky='nsew')
        self.answer_display.grid(row=0, column=1,  sticky='nsew')

        # add borders
        self.mini_display.config(highlightbackground='#000000', highlightthickness=2)

        # add grayscale color slider (+ labels for the top left segment)
        Label(self.funcs, text='grayscale float value', bg='lavender', font=(24)).grid(row=0, column=0)
        self.color_slider = Scale(self.funcs, from_=0.0, to_=1.0, resolution=0.01, orient=HORIZONTAL, bg='lavender', command=self.adjust_color)
        self.color_slider.grid(row=1, column=0, ipadx=155, ipady=20)
        self.curr_color = Label(self.funcs, text='             ', bg=self.pen_color, font=(24)).grid(row=2, column=0)

        # canvas actions
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<Button-1>", self.draw)

        self.canvas.bind('<ButtonRelease-1>', self.update)

        # reset canvas button
        self.reset_bttn = Button(self.answer_display, bg='lavender', text='reset canvas', command=self.reset_canvas)
        self.reset_bttn.place(relx=0.5, rely=0.9, anchor=CENTER)

        # labels for the predictions
        Label(self.answer_display, text='predicted number:', bg='lavender', padx = 20, pady=10).grid(row=0, column=0)
        Label(self.answer_display, text='???', bg='lavender', fg='MediumPurple3', padx=20, font=(48), anchor=CENTER).grid(row=1, column=0)

        # puts the image in the mini display
        self.update_mini_display()

        # create loading button and entry
        Label(self.answer_display, text='enter .txt file to load', bg='lavender', pady=10).grid(row=2, column=0)
        self.fileentry = Entry(self.answer_display, textvariable=StringVar(self.answer_display, 'values/namehere.txt'))
        self.fileentry.grid(row=3, column=0)
        self.load_bttn = Button(self.answer_display, text='load', bg='lavender', command=self.load_values)
        self.load_bttn.grid(row=4, column=0)
        self.ld_message = Label(self.answer_display, text=' ', bg='lavender', fg='red', pady=5)
        self.ld_message.grid(row=5, column=0)


    def adjust_color(self, val):
        hex_val = str(hex(int(float(val[:5]) * 255)))[2:]
        faded = str(hex(int(0.9 * float(val[:5]) * 255)))[2:]
        if len(hex_val) == 1:
            hex_val = '0' + hex_val

        if len(faded) == 1:
            faded = '0' + faded

        self.pen_color = '#' + 3 * hex_val
        self.faded_pen = '#' + 3 * faded
        Label(self.funcs, text='             ', bg=self.pen_color, font=(24)).grid(row=2, column=0)

    def draw(self, event):
        xpt = (event.x - (event.x % self.pix_dim)) // self.pix_dim
        ypt = (event.y - (event.y % self.pix_dim)) // self.pix_dim

        #draw faded portions
        faded_float = int(self.faded_pen[-2:], 16) / 255
        if ypt + 1 < self.img_dim  and xpt < self.img_dim and xpt >= 0:
            self.canvas.create_rectangle(xpt * self.pix_dim, (ypt + 1) * self.pix_dim, (xpt + 1) * self.pix_dim, (ypt + 2) * self.pix_dim, fill=self.faded_pen,outline='')
            self.img[ypt + 1][xpt] = faded_float

        if xpt - 1 >= 0 and xpt < self.img_dim and ypt < self.img_dim and ypt >= 0:
            self.canvas.create_rectangle((xpt - 1) * self.pix_dim, ypt * self.pix_dim, xpt * self.pix_dim, (ypt + 1) * self.pix_dim, fill=self.faded_pen,outline='')
            self.img[ypt][xpt - 1] = faded_float

        # draw main portion
        color_float = int(self.pen_color[-2:], 16) / 255
        if xpt >= 0 and xpt < self.img_dim and ypt >= 0 and ypt < self.img_dim:
            self.canvas.create_rectangle(xpt * self.pix_dim, ypt * self.pix_dim, (xpt + 1) * self.pix_dim, (ypt + 1) * self.pix_dim, fill=self.pen_color,
                                         outline='')
            self.img[ypt][xpt] = color_float

    def update(self, event):
        # update current prediction
        guess = self.classifier.classify(self.img.flatten())
        Label(self.answer_display, text=str(guess), bg='lavender', fg='MediumPurple3', padx=20, font=(48), anchor=CENTER).grid(row=1, column=0)

        self.update_mini_display()

    def reset_canvas(self):
        self.img = np.zeros((self.img_dim, self.img_dim))
        self.canvas.delete('all')
        Label(self.answer_display, text='???', bg='lavender', fg='MediumPurple3', padx=20, font=(48), anchor=CENTER).grid(row=1, column=0)

        self.update_mini_display()

    # load input values from a text file
    def load_values(self):
        filename = self.fileentry.get()
        if filename[-4:] != '.txt':
            self.ld_message['text'] = 'please use .txt file'
            return

        if not os.path.isfile(filename):
            self.ld_message['text'] = 'file not found'
            return

        values = []
        with open(filename, 'r') as file:
            for line in file:
                v = [float(thing) for thing in line.split(',')]
                values += v

        values = np.asarray([values])
        self.img = values.reshape(self.img_dim, self.img_dim).T

        for row in range(len(self.img)):
            for col in range(len(self.img[row])):
                hex_val = str(hex(int(float(self.img[row][col] * 255))))[2:]
                if len(hex_val) == 1:
                    hex_val = '0' + hex_val

                color = '#' + 3 * hex_val
                xpt = row * self.pix_dim
                ypt = col * self.pix_dim
                self.canvas.create_rectangle(xpt, ypt, xpt + self.pix_dim, ypt + self.pix_dim, fill=color,outline='')

        self.update_mini_display()

        # update current prediction
        guess = self.classifier.classify(self.img.flatten())
        Label(self.answer_display, text=str(guess), bg='lavender', fg='MediumPurple3', padx=20, font=(48),
              anchor=CENTER).grid(row=1, column=0)


    def update_mini_display(self):
        im = Img.fromarray(255 * self.img)
        im = im.convert('RGB')
        im.save('nums/num.png')
        self.pic = ImageTk.PhotoImage(Img.open('nums/num.png'))
        self.mini_img = Label(self.mini_display, image=self.pic)
        self.mini_img.place(relx=0.5, rely=0.5, anchor=CENTER)


root = Tk()
root.title("Guessing Numbers")
root.resizable(False, False)
gui = NumbersGUI(master=root)
root.mainloop()
