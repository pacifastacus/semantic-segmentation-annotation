import numpy as np
from PIL import Image, ImageTk
import cv2
import os
import sys


class Dataframe:
    """A Dataframe object represents a data pair from a training dataset.
    In this project a pair means an image frame and the associated ground-truth (ie. a matrix of integers).
    """

    def __init__(self, img_path,
                 gt_dirname=None,
                 gt_autosave=False,
                 colormap=[[0,0,0]]):
        """
        :param img_path: image filename
        :param gt_dirname: the folder name of gts. If given, the ground-truth folder will be set to this,
                        else it will be <image dir>_gt/
        :param gt_autosave: if True save gt on Dataframe init, update and destroy (default is False)
        """
        self._img = None  # Image
        self._gt = np.array(list())   # Ground-truth
        self._img_fname = None  # Image filename w/o path
        self._img_ext = None  # Image file extension
        self._img_dir = None  # Image directory (absolute path)
        self._gt_fname = None  # GT filename w/o path
        self._gt_dir = None  # Ground-truth directory (absolute path)
        self._gt_ext = ".png"
        self._colors = colormap
        self._gt_autosave = gt_autosave

        # Init image
        # Read image from file
        if not os.path.isfile(img_path):
            raise FileNotFoundError("im_frame_path is not a file")
        self._img_dir, self._img_fname = os.path.split(os.path.abspath(img_path))
        self._img = cv2.imread(img_path)

        # Init ground-truth
        self._gt_fname, self._img_ext = os.path.splitext(self._img_fname)
        self._gt_fname = self._gt_fname + self._gt_ext
        # Try to read gt from file OR init a new one
        if not gt_dirname:
            self._gt_dir = self._img_dir + "_gt"
        else:
            self._gt_dir = os.path.join(os.path.basename(self._img_dir), gt_dirname)
        if not os.path.exists(self._gt_dir):
            os.mkdir(self._gt_dir)
        gt_path = os.path.join(self._gt_dir, self._gt_fname)
        if os.path.exists(gt_path) and os.path.isfile(gt_path):
            print("Existing ground truth loaded")
            self._gt = cv2.imread(gt_path)

        else:
            print("New ground truth created")
            self._gt = np.zeros(self._img.shape, dtype=np.uint8)  # Create a new empty map

    def __del__(self):
        if self._gt_autosave:
            self.save_gt()

    def get_image(self, raw=False):
        """
        return image for Tkinter
        :param raw: if True return the image as numpy array
        :return:
        """
        if raw:
            return self._img.copy()

        img = cv2.cvtColor(self._img, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(img)
        return ImageTk.PhotoImage(im)

    def get_gt(self, raw=False):
        if raw:
            return self._gt.copy()

        gt = cv2.cvtColor(self._gt, cv2.COLOR_BGR2RGB)
        gt = Image.fromarray(gt)
        return ImageTk.PhotoImage(gt)

    def get_img_shape(self):
        return self._img.shape

    def get_meta(self):
        """
        Return a dict structure containing info about image and ground-truth.
        {"img": {"path":<absolute path>,
                 "fname":<filename>,
                 "res":img.shape,
                 "mode":"rgb"|"bgr"|"gray"|etc.
                },
         "gt":  {"path":<absolute path>,
                 "fname":<filename>,
                 "res":gt.shape,
                 "mode":"rgb"|"gray"|"array"
                },
        "wdir":<absolute common path of img and gt>,
        "autosave":<state of autosave feature>
        :return: a structured dict of meta-data
        """
        return {"img": {"path": os.path.join(self._img_dir, self._img_fname),
                        "fname": self._img_fname,
                        "res": self._img.shape},
                "gt": {"path": os.path.join(self._gt_dir, self._gt_fname),
                       "fname": self._gt_fname,
                       "res": self._gt.shape},
                "wdir": os.path.commonpath((self._img_dir, self._gt_dir)),
                "autosave":self._gt_autosave}

    def save_gt(self):
        filename = os.path.join(self._gt_dir, self._gt_fname)
        cv2.imwrite(filename, self._gt)

    def update_gt(self,gt):
        self._gt = gt

    def label2color(self, label):
        return self._colors[label]

    def color2label(self, rgb):
        try:
            return self._colors.index(list(rgb))
        except ValueError:
            return -1
