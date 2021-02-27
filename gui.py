from tkinter import *
import numpy as np
#from edge import calc_edges
from PIL import Image, ImageTk
from dataframe import Dataframe
import cv2
import glob

DEFAULT_IMG_SIZE = {"height": 200, "width": 200}
class App(Frame):
    def __init__(self, master=None, fileList=None):
        Frame.__init__(self, master)
        self.frame_increment = IntVar()
        self.brightness = IntVar()
        self.seg_method = StringVar()
        self.fname = fileList
        self._dataframe = Dataframe(fname[0])
        self.img = self._dataframe.get_image()
        self.label = self._dataframe.get_gt()
        #self.label_map = None
        self.FRAME_COUNT = 0
        self.brush_point = (0, 0)
        self.grid()
        self.__createWidgets()

    def __createWidgets(self):
        self.img_frame = Frame(self)
        self.img_frame.pack(side=LEFT)
        ctrl_frame = Frame(self)
        ctrl_frame.pack(side=RIGHT)
        slides_frame = Frame(ctrl_frame)
        slides_frame.pack(side=TOP, anchor=W)
        nav_frame = Frame(ctrl_frame)
        nav_frame.pack(side=BOTTOM, anchor=N)

        self.__create_canvas(self.img_frame)
        # lmain = Label(selfimg_frame)
        # lmain.pack()
        self.__create_control_panel(slides_frame)
        self.__create_nav_panel(nav_frame)


    def __create_canvas(self,img_frame):
        self.image_canvas = Canvas(img_frame, **DEFAULT_IMG_SIZE, bg="green", cursor="cross")
        self.label_canvas = Canvas(img_frame, **DEFAULT_IMG_SIZE, bg="gray")
        self.image_canvas.pack(side=TOP, fill='both', expand=True)
        self.label_canvas.pack(side=BOTTOM, fill='both', expand=True)
        self.image_canvas.bind("<ButtonPress-1>", self.get_brush_coordinates)
        self.__init_canvas()

    def __create_control_panel(self,slides_frame):
        methods = ["None", "Canny", "K-Means"]
        method_opt = OptionMenu(slides_frame, self.seg_method, *methods)
        method_opt.pack()
        self.seg_method.set(methods[0])
        brightness_slider = Scale(slides_frame, label="brightness", orient=HORIZONTAL, variable=self.brightness)
        brightness_slider.pack()

    def __create_nav_panel(self,nav_frame):
        prev_button = Button(nav_frame, text="<<", command=self.__call_prev_frame)
        next_button = Button(nav_frame, text=">>", command=self.__call_next_frame)
        step_scale = Scale(nav_frame, label="step increment", orient=HORIZONTAL,
                           from_=0, to=100, resolution=5, variable=self.frame_increment)
        step_scale.pack(side=TOP)
        prev_button.pack(side=LEFT)
        next_button.pack(side=RIGHT)

    def __init_canvas(self):
        self.img = self._dataframe.get_image()
        self.label = self._dataframe.get_gt()
        self.image_canvas.config(width=self.img.width(), height=self.img.height())
        self.label_canvas.config(width=self.img.width(), height=self.img.height())
        self.image_canvas.create_image(0, 0, anchor='nw', image=self.img)
        self.label_canvas.create_image(0, 0, anchor="nw", image=self.label)

#    def __load_image(self, fileidx):
#        img = cv2.imread(self.fname[fileidx], cv2.IMREAD_COLOR)
#        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#        im = Image.fromarray(img)
#        return ImageTk.PhotoImage(im)
    def __new_df(self,fileidx):
        self._dataframe = Dataframe(self.fname[fileidx])


    def __show_img(self):
        # global lmain
        self.img = self._dataframe.get_image()
        self.image_canvas.create_image(0, 0, anchor='nw', image=self.img)
    def __show_label(self):
        self.label = self._dataframe.get_gt()
        self.label_canvas.create_image(0,0,anchor='nw', image=self.label)

    def __call_next_frame(self):
        increment = self.frame_increment.get()
        if increment < 1:
            increment = 1
        self.FRAME_COUNT += increment
        if self.FRAME_COUNT >= len(fname):
            self.FRAME_COUNT = len(fname) - 1
        self.__new_df(self.FRAME_COUNT)
        self.__show_img()
        self.__show_label()

    def __call_prev_frame(self):
        increment = self.frame_increment.get()
        if increment < 1:
            increment = 1
        self.FRAME_COUNT -= increment
        if self.FRAME_COUNT < 0:
            FRAME_COUNT = 0
        self.__new_df(self.FRAME_COUNT)
        self.__show_img()
        self.__show_label()

    def get_brush_coordinates(self, event):
        self.brush_point = (event.x, event.y)
        print("brush coords:", self.brush_point)


def sort_numbered_fname(e):
    import re
    match = re.search('([^0-9]*)([0-9]+)(.*)', e)
    num = int(match[2])
    return num

if __name__ == '__main__':
    # Get list of images
    img_dir = 'test_data/img/'
    fname = glob.glob(img_dir + '*.jpg')
    fname.sort(key=sort_numbered_fname)

    app = App(fileList=fname)
    app.master.title('Annotator')
    app.mainloop()
