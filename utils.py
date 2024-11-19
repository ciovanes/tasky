import customtkinter as ctk
from PIL import Image, ImageTk


def center_window(root: ctk.CTk, width: int, height: int):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    pos_x = int((screen_width - width) / 2)
    pos_y = int((screen_height - height) / 2)

    root.geometry(f'{pos_x}+{pos_y}')
    root.minsize(width=width, height=height)


def getImage(pathToImage: str, width, height) -> ImageTk:
    image = Image.open(pathToImage).resize((width, height), Image.LANCZOS)
    return ImageTk.PhotoImage(image)
