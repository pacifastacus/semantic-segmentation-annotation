from tkinter import *
import numpy as np
from PIL import Image, ImageTk
from edge import calc_edges
from dataframe import Dataframe
import cv2
import glob

DEFAULT_IMG_SIZE = {"height": 200, "width": 200}
class App(Frame):
    def __init__(self, fileList, colormap, master=None):
        Frame.__init__(self, master)
        self.frame_increment = IntVar()
        #self.brightness = IntVar()
        self.seg_method = StringVar()
        self.seg_method.trace("w", self.__show_img)
        self.fname = fileList
        self._dataframe = Dataframe(fname[0])
        self.img = self._dataframe.get_image()
        self.mask = np.zeros(self._dataframe.get_img_shape(), dtype=np.uint8)
        self.gt = self._dataframe.get_gt()
        self.label = IntVar()
        self.colormap = colormap
        self.FRAME_COUNT = 0
        self.brush_point = (0, 0)
        self.bursh_mode = "bucket" # "bucket"|"bursh"|"pencil"
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
        self.gt_canvas = Canvas(img_frame, **DEFAULT_IMG_SIZE, bg="gray")
        self.image_canvas.pack(side=TOP, fill='both', expand=True)
        self.gt_canvas.pack(side=BOTTOM, fill='both', expand=True)
        self.image_canvas.bind("<ButtonPress-1>", self.__draw_action)
        self.__init_canvas()

    def __create_control_panel(self,slides_frame):
        methods = ["None", "Canny"]
        method_opt = OptionMenu(slides_frame, self.seg_method, *methods)
        labels = [0,1,2,3,4,5]
        label_opt = OptionMenu(slides_frame, self.label, *labels)
        label_opt.pack()
        method_opt.pack()
        self.seg_method.set(methods[1])

        #brightness_slider = Scale(slides_frame, label="brightness", orient=HORIZONTAL, variable=self.brightness)
        #brightness_slider.pack()

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
        self.gt = self._dataframe.get_gt()
        self.image_canvas.config(width=self.img.width(), height=self.img.height())
        self.gt_canvas.config(width=self.img.width(), height=self.img.height())
        self.image_canvas.create_image(0, 0, anchor='nw', image=self.img)
        self.gt_canvas.create_image(0, 0, anchor="nw", image=self.gt)

    def __new_df(self,fileidx):
        self._dataframe.save_gt()
        self._dataframe = Dataframe(self.fname[fileidx],gt_autosave=False)


    def __show_img(self,a=None,b=None,c=None):
        # global lmain
        self.img = self._dataframe.get_image()
        self.preprocess_image()
        self.image_canvas.create_image(0, 0, anchor='nw', image=self.img)
    def __show_gt(self):
        self.gt = self._dataframe.get_gt()
        self.gt_canvas.create_image(0, 0, anchor='nw', image=self.gt)

    def __call_next_frame(self):
        increment = self.frame_increment.get()
        if increment < 1:
            increment = 1
        self.FRAME_COUNT += increment
        if self.FRAME_COUNT >= len(fname):
            self.FRAME_COUNT = len(fname) - 1
        self.__new_df(self.FRAME_COUNT)
        self.__show_img()
        self.__show_gt()

    def __call_prev_frame(self):
        increment = self.frame_increment.get()
        if increment < 1:
            increment = 1
        self.FRAME_COUNT -= increment
        if self.FRAME_COUNT < 0:
            FRAME_COUNT = 0
        self.__new_df(self.FRAME_COUNT)
        self.__show_img()
        self.__show_gt()

    def __draw_action(self,event):
        if self.seg_method.get() == "Canny":
            self.fill_region(event)
        elif self.seg_method.get() == "None":
            self.draw(event)

    def get_brush_coordinates(self, event):
        self.brush_point = (event.x, event.y)
        print("brush coords:", self.brush_point)

    def fill_region(self,event):
        self.brush_point = (event.x, event.y)
        gt = self._dataframe.get_gt(raw=True)
        retval,image,mask,rect = cv2.floodFill(gt, np.pad(self.mask, pad_width=1), self.brush_point, colors[self.label.get()])
        self._dataframe.update_gt(gt)
        self.__show_gt()

    def draw(self,event):
        #TODO implement handdrawing
        pass

    def preprocess_image(self):
        method = self.seg_method.get()
        if method == "None":
            pass
        elif method == "Canny":
            img = cv2.cvtColor(self._dataframe.get_image(raw=True),cv2.COLOR_BGR2RGB)
            self.mask = calc_edges(cv2.cvtColor(img,cv2.COLOR_BGR2GRAY))
            img[self.mask != 0] = [0, 0, 0]
            self.img = ImageTk.PhotoImage(Image.fromarray(img))

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
    colors=[]
    with open("colormap.txt", "r") as color_file:
        for line in color_file:
            r, g, b = line.split()
            r = int(r)
            g = int(g)
            b = int(b)
            colors.append([r, g, b])

    app = App(fileList=fname,colormap=colors)
    app.master.title('Annotator')
    app.mainloop()
