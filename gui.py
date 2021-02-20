from tkinter import *
from PIL import Image, ImageTk
import cv2
import glob

class App(Frame):
    def __init__(self, master=None, fileList=None):
        Frame.__init__(self, master)
        self.frame_increment = IntVar()
        self.brightness = IntVar()
        self.seg_method = StringVar()
        self.fname = fileList
        self.loaded_img = None
        self.img_id = None
        self.canvas = None
        self.FRAME_COUNT = 0
        self.brush_point = (0, 0)
        self.grid()
        self.__createWidgets()
        self.__init_canvas()

    def __createWidgets(self):
        img_frame = Frame(self)
        img_frame.pack(side=LEFT)
        ctrl_frame = Frame(self)
        ctrl_frame.pack(side=RIGHT)
        slides_frame = Frame(ctrl_frame)
        slides_frame.pack(side=TOP, anchor=W)
        nav_frame = Frame(ctrl_frame)
        nav_frame.pack(side=BOTTOM, anchor=N)

        self.__create_canvas(img_frame)
        # lmain = Label(img_frame)
        # lmain.pack()
        self.__create_control_panel(slides_frame)
        self.__create_nav_panel(nav_frame)


    def __create_canvas(self,img_frame):
        self.canvas = Canvas(img_frame, width=200, height=200, bg="green", cursor="cross", relief=SUNKEN)
        self.canvas.pack(fill='both', expand=True)
        self.canvas.bind("<ButtonPress-1>", self.get_brush_coordinates)

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
        self.loaded_img = self.__load_image(0)
        self.canvas.config(width=self.loaded_img.width(),height=self.loaded_img.height())
        self.img_id = self.canvas.create_image(0, 0, anchor='nw', image=self.loaded_img)


    def __load_image(self, fileidx):
        img = cv2.imread(self.fname[fileidx], cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        im = Image.fromarray(img)
        print(im)

        return ImageTk.PhotoImage(im)

    def __show_frame(self, fname_idx):
        # global lmain
        imgtk = self.__load_image(fname_idx)
        print(fname[fname_idx])
        self.loaded_img = imgtk
        self.img_id = self.canvas.create_image(0, 0, anchor='nw', image=self.loaded_img)

    def __call_next_frame(self):
        increment = self.frame_increment.get()
        if increment < 1:
            increment = 1
        self.FRAME_COUNT += increment
        if self.FRAME_COUNT >= len(fname):
            self.FRAME_COUNT = len(fname) - 1
        self.__show_frame(self.FRAME_COUNT)

    def __call_prev_frame(self):
        increment = self.frame_increment.get()
        if increment < 1:
            increment = 1
        self.FRAME_COUNT -= increment
        if self.FRAME_COUNT < 0:
            FRAME_COUNT = 0
        self.__show_frame(self.FRAME_COUNT)

    def get_brush_coordinates(self, event):
        self.brush_point = (event.x, event.y)
        print("brush coords:",self.brush_point)


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
