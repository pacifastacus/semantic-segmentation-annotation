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
                 img_mode="bgr",
                 gt_dirname=None,
                 gt_ext='.npy',
                 gt_mode="numpy",
                 gt_autosave=False):
        """
        :param img_path: image filename
        :param img_mode: how the image read from file: "rgb","rgba","bgr","gray" (default: "bgr")
        :param gt_dirname: the folder name of gts. If given, the ground-truth folder will be set to this,
                        else it will be <image dir>_gt/
        :param gt_ext: file extension of ground-truth, eg. ".bmp", ".png", ".npy", ".h5"
        :param gt_mode: ground-truth representation mode: "rgb","gray","numpy" (default: "numpy")
        :param gt_autosave: if True save gt on Dataframe init, update and destroy (default is False)
        """
        self._img = None  # Image
        self._img_mode = img_mode
        self._gt = np.array(list())   # Ground-truth
        self._gt_mode = gt_mode
        self._img_fname = None  # Image filename w/o path
        self._img_ext = None  # Image file extension
        self._img_dir = None  # Image directory (absolute path)
        self._gt_fname = None  # GT filename w/o path
        self._gt_ext = gt_ext
        self._gt_dir = None  # Ground-truth directory (absolute path)
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
        if os.path.exists(self._gt_dir):
            gt_path = os.path.join(self._gt_dir,self._gt_fname)
            if os.path.exists(gt_path) and os.path.isfile(gt_path):
                print("Existing ground truth loaded")
                if self._gt_mode == "numpy":
                    self._gt = np.load(gt_path)
                else:
                    self._gt = cv2.imread(gt_path)
            else:
                print("New ground truth created")
                self._gt = np.zeros(self._img.shape[:2], dtype=np.uint8)  # Create a new empty map
        else:
            os.mkdir(self._gt_dir)
            if self._gt_autosave:
                self.save_gt()

    def __del__(self):
        if self._gt_autosave:
            self.save_gt()

    def get_image(self):
        return self._img

    def get_gt(self):
        return self._gt

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
                        "res": self._img.shape,
                        "mode": self._img_mode},
                "gt": {"path": os.path.join(self._gt_dir, self._gt_fname),
                       "fname": self._gt_fname,
                       "res": self._gt.shape,
                       "mode": self._gt_mode},
                "wdir": os.path.commonpath((self._img_dir, self._gt_dir)),
                "autosave":self._gt_autosave}

    def save_gt(self):
        filename = os.path.join(self._gt_dir, self._gt_fname)
        #### Switch-case construct ####
        def save_gray():
            grayim = np.stack((self._gt,)*3,axis=-1)
            cv2.imwrite(filename,grayim)
        def save_rgb():
            cv2.imwrite(filename,self._gt)
        def save_np():
            np.save(filename,self._gt)

        switch = {
            "gray" : save_gray,
            "rgb" : save_rgb,
            "numpy": save_np
        }
        #### End of Switch-case construct ####
        switch[self._gt_mode]()


if __name__ == "__main__":
    df = Dataframe("test_data/img/1_cam-image_array_.jpg",gt_autosave=False)
    gt = df.get_gt()
    df.save_gt()

    for key, value in df.get_meta().items():
        if type(value) is dict:
            print(key, ":")
            for key, value in value.items():
                print("\t",key,":",value)
        else:
            print(key,":",value)