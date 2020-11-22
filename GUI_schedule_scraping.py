import multiprocessing as mp
import facebook_scraping as fs

import sys

# Just checking your Python version to import Tkinter properly.
if sys.version_info[0] == 2:
    from Tkinter import *
    import Tkinter.font as tkFont
else:
    from tkinter import *
    import tkinter.font as tkFont

from PIL import ImageTk, Image
import os

from datetime import datetime
from time import sleep

PAGE_NAME = "electroLAB.FPMs"
ENABLE_EMOJI = False
PHONE_NBR = fs.add_emoji(":telephone_receiver:")  \
               + " : NUMÉRO DE TÉLÉPHONE DE VINCENT" \
               if ENABLE_EMOJI                       \
               else "Tél. : NUMÉRO DE TÉLÉPHONE DE VINCENT"

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
IMAGES_PATH = os.path.join(SCRIPT_PATH, "images")
ICONE_PATH = os.path.join(IMAGES_PATH, 'electroLAB.ico')
LOGO_PATH = os.path.join(IMAGES_PATH, 'electroLAB-LOGO.png')

ELAB_GREEN = "#%02x%02x%02x" % (44, 167, 106)

POST_KEY = b'\xf0\x9f\x95\x93'.decode('utf8')

class Fullscreen_Window:
    def __init__(self, post_text_Queue):
        self.tk = Tk()
        self.tk.title("electroLAB - Horaire")
        self.tk.config(cursor="none")
        try:
            self.tk.wm_iconbitmap(ICONE_PATH)
        except Exception:
            pass
        self.font = tkFont.Font(family="Helvetica", size=40)
        self.tk.bind("<F11>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)

        # Set variables
        self.screen_width = self.tk.winfo_screenwidth()
        self.screen_height = self.tk.winfo_screenheight()
        self.post_text = post_text_Queue
        self.post = StringVar()
        self.time = StringVar()
        self.previous_date = ""
        self.img = ImageTk.PhotoImage(
            Image.open(LOGO_PATH).resize(  # Logo
                (int(self.screen_height/10),  # Target width
                 int(self.screen_height/10)),  # Target height
                Image.ANTIALIAS))

        # Frame and labels
        self.frame = Frame(self.tk)
        self.lbl_list = []

        # Header
        self.lbl_list.append(Label(
            self.frame,
            image=self.img,
            background=ELAB_GREEN,
            anchor=CENTER,
            height=int(self.screen_height/4.5),
            width=self.screen_width,
            relief=None,
            compound="center").grid(column=0, row=0, sticky="nsew"))

        # Post information
        self.lbl_list.append(Label(
            self.frame,
            textvariable=self.post,
            background='white',
            anchor='center',
            font=self.font,
            relief=None,
            compound="center",
            height=9).grid(column=0, row=1, sticky="nsew"))

        # Time
        self.lbl_list.append(Label(
            self.frame,
            textvariable=self.time,
            background='white',
            anchor='center',
            font=self.font,
            relief=None,
            compound="center",
            height=3).grid(column=0, row=2, sticky="nsew"))

        # Footer
        self.lbl_list.append(Label(
            self.frame,
            image=self.img,
            background=ELAB_GREEN,
            anchor=CENTER,
            height=int(self.screen_height/4.5),
            width=self.screen_width,
            relief=None,
            compound="center").grid(column=0, row=3, sticky="nsew"))

        # Arrange grid
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_rowconfigure(3, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.pack()

        # Initialise update tasks
        self.update()

        # Set as fullscreen
        self.state = True
        self.tk.attributes("-fullscreen", self.state)

    # Toggle fullscreen mode
    def toggle_fullscreen(self, event=None):
        self.state = not self.state
        self.tk.attributes("-fullscreen", self.state)

    # Exit fullscreen mode
    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", self.state)

    # Update
    def update(self):
        utc_datetime = datetime.now()

        while(self.previous_date == utc_datetime):
            sleep(0.01)
            utc_datetime = datetime.now()

        self.previous_date = utc_datetime
        self.time.set(self.previous_date.strftime("%d/%m/%Y %H:%M:%S"))
        while self.post_text.full():
            self.post.set(self.post_text.get())

        self.tk.update()
        self.tk.after(10, self.update)


def main(post_Queue):
    w = Fullscreen_Window(post_Queue)
    w.tk.mainloop()


def update_post(
        post_queue,
        page_name=PAGE_NAME,
        key=POST_KEY,
        enable_emoji=ENABLE_EMOJI,
        phone=PHONE_NBR):
    post_queue.put("")
    post_text = ""

    while True:
        try:
            temp = fs.getPost(
                page_name=page_name,
                key=key,
                enable_emoji=enable_emoji)

            if temp != post_text:
                post_text = fs.getPost(
                    page_name=page_name,
                    key=key,
                    enable_emoji=enable_emoji)

                post_queue.put(
                    post_text + "\n\n" + phone + "\n\n Nombre de likes: " + fs.getLikeCount(page_name))

        except Exception as error:
            print(error)
            if "(Pas de connexion)\n" not in post_text:
                post_text = "(Pas de connexion)\n" + post_text
        sleep(5)


if __name__ == "__main__":
    # Create a Queue and post update process
    post_Queue = mp.Queue(1)
    process_handler = mp.Process(target=update_post, args=(post_Queue,))
    process_handler.start()

    # Pass the pipe as argument for the GUI
    main(post_Queue)

    # Kill the process
    process_handler.terminate()
