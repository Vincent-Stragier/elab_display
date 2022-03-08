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

import yaml

from datetime import datetime
from time import sleep


SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_PATH, 'config.yml')

config = yaml.safe_load(open(CONFIG_FILE, 'r'))

IMAGES_PATH = os.path.join(SCRIPT_PATH, config['images_folder'])
ICON_PATH = os.path.join(IMAGES_PATH, config['icon_path'])
LOGO_PATH = os.path.join(IMAGES_PATH, config['logo_path'])
PAGE_NAME = config['facebook_page_name']

ENABLE_EMOJI = config['enable_emoji']
PHONE_EMOJI = config['phone']['emoji']
PHONE_ALTERNATIVE_TEXT = config['phone']['text']
PHONE_NBR = PHONE_EMOJI if ENABLE_EMOJI else PHONE_ALTERNATIVE_TEXT
PHONE_NBR = fs.add_emoji(PHONE_NBR)
PHONE_NBR = fs.add_emoji(f'{PHONE_NBR}{config["phone"]["number"]}')
# print(config)
# print(PHONE_NBR)
# exit()

# electroLAB's green
RGB_TUPLE = tuple(config['header_and_footer_color'])
HEADER_AND_FOOTER_COLOR = '#%02x%02x%02x' % RGB_TUPLE

APP_TITLE = config['app_title']

POST_KEY = bytes(config['bytes_post_key'], 'utf8').decode('utf8')

FONT_FAMILY = config['font']['family']
FONT_SIZE = config['font']['size']
DISPLAY_CURSOR = config['cursor']


class FullscreenWindow:
    def __init__(self, post_text_Queue):
        self.tk = Tk()
        self.tk.title(APP_TITLE)
        self.tk.config(cursor=DISPLAY_CURSOR)
        try:
            self.tk.wm_iconbitmap(ICON_PATH)
        except Exception:
            pass
        self.font = tkFont.Font(family=FONT_FAMILY, size=FONT_SIZE)
        self.tk.bind('<F11>', self.toggle_fullscreen)
        self.tk.bind('<Escape>', self.end_fullscreen)

        # Set variables
        self.screen_width = self.tk.winfo_screenwidth()
        self.screen_height = self.tk.winfo_screenheight()
        self.post_text = post_text_Queue
        self.post = StringVar()
        self.time = StringVar()
        self.previous_date = ''
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
            background=HEADER_AND_FOOTER_COLOR,
            anchor=CENTER,
            height=int(self.screen_height/4.5),
            width=self.screen_width,
            relief=None,
            compound='center').grid(column=0, row=0, sticky='nsew'))

        # Post information (body)
        self.lbl_list.append(Label(
            self.frame,
            textvariable=self.post,
            background='white',
            anchor='center',
            font=self.font,
            relief=None,
            compound='center',
            height=9).grid(column=0, row=1, sticky='nsew'))

        # Time
        self.lbl_list.append(Label(
            self.frame,
            textvariable=self.time,
            background='white',
            anchor='center',
            font=self.font,
            relief=None,
            compound='center',
            height=3).grid(column=0, row=2, sticky='nsew'))

        # Footer
        self.lbl_list.append(Label(
            self.frame,
            image=self.img,
            background=HEADER_AND_FOOTER_COLOR,
            anchor=CENTER,
            height=int(self.screen_height/4.5),
            width=self.screen_width,
            relief=None,
            compound='center').grid(column=0, row=3, sticky='nsew'))

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
        self.tk.attributes('-fullscreen', self.state)

    # Toggle fullscreen mode
    def toggle_fullscreen(self, event=None):
        self.state = not self.state
        self.tk.attributes('-fullscreen', self.state)

    # Exit fullscreen mode
    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes('-fullscreen', self.state)

    # Update
    def update(self):
        utc_datetime = datetime.now()

        # Update each second
        while (self.previous_date == utc_datetime):
            sleep(0.01)
            utc_datetime = datetime.now()

        self.previous_date = utc_datetime
        self.time.set(self.previous_date.strftime('%d/%m/%Y %H:%M:%S'))
        while self.post_text.full():
            self.post.set(self.post_text.get())

        # Render the update
        self.tk.update()
        # Call the function in 10 ms
        self.tk.after(10, self.update)


def main(post_Queue):
    w = FullscreenWindow(post_Queue)
    w.tk.mainloop()


def update_post(
        post_queue,
        update_delay: int,
        page_name: str = PAGE_NAME,
        key: str = POST_KEY,
        enable_emoji: bool = ENABLE_EMOJI,
        phone: str = PHONE_NBR):
    post_queue.put('')
    post_text = ''
    like_count = 0

    while True:
        try:
            temp = fs.get_matching_post(
                page_name=page_name,
                key=key,
                enable_emoji=enable_emoji)

            if temp != post_text or like_count != fs.get_likes_count(page_name):
                like_count = fs.get_likes_count(page_name)
                post_text = fs.get_matching_post(
                    page_name=page_name,
                    key=key,
                    enable_emoji=enable_emoji)

                post_queue.put(f'{post_text}\n\n{phone}\n\n '
                               f'Nombre de likes: {like_count}')

        except Exception as error:
            print(error)
            if '(Pas de connexion)\n' not in post_text:
                post_text = f'(Pas de connexion)\n{post_text}'
        sleep(update_delay)


if __name__ == '__main__':
    # Create a Queue and post update process
    post_Queue = mp.Queue(1)
    process_handler = mp.Process(
        target=update_post, args=(post_Queue, config['update_delay']))
    process_handler.start()

    # Pass the Queue as argument for the GUI
    main(post_Queue)

    # Kill the process
    process_handler.terminate()
