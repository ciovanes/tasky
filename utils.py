import customtkinter as ctk
from PIL import Image, ImageTk
from customtkinter import CTkImage, CTkLabel

def center_window(root: ctk.CTk, width: int, height: int) -> None:
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    pos_x = int((screen_width - width) / 2)
    pos_y = int((screen_height - height) / 2)

    root.geometry(f'{pos_x}+{pos_y}')
    root.minsize(width=width, height=height)


def getImage(path_to_image: str, width: int, height: int) -> CTkImage:
    image = Image.open(path_to_image).resize((width, height), Image.LANCZOS)
    return CTkImage(image)


def generate_error_text(root, label: CTkLabel, text: str, ms: int) -> None:
    label.configure(text=text)
    root.after(ms, lambda: clear_error_text(label))


def clear_error_text(label: CTkLabel) -> None:
    label.configure(text='')
