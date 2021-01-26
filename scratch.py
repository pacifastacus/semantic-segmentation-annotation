import tkinter as tk
from PIL import Image, ImageTk
import cv2

# --- functions ---

def on_click():
    # change image on canvas
    canvas.itemconfig(image_id, image=image2)

# --- main ---

root = tk.Tk()

# canvas for image
canvas = tk.Canvas(root, width=60, height=60)
canvas.pack()

# button to change image
button = tk.Button(root, text="Change", command=on_click)
button.pack()

# images
fname1 = "/home/palkovics/PycharmProjects/semantic-segmentation-annotation/test_data/img/1_cam-image_array_.jpg"
fname2 = "/home/palkovics/PycharmProjects/semantic-segmentation-annotation/test_data/img/1000_cam-image_array_.jpg"
im1 = cv2.imread(fname1, cv2.IMREAD_COLOR)
im2 = cv2.imread(fname2, cv2.IMREAD_COLOR)
#image1 = ImageTk.PhotoImage(Image.open(fname1))
#image2 = ImageTk.PhotoImage(Image.open(fname2))
image1 = ImageTk.PhotoImage(Image.fromarray(im1))
image2 = ImageTk.PhotoImage(Image.fromarray(im2))

# set first image on canvas
image_id = canvas.create_image(0, 0, anchor='nw', image=image1)

root.mainloop()
