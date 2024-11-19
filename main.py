import customtkinter as ctk
from utils import *


class TopFrame(ctk.CTkFrame):

    def __init__(self, master, **kwards):
        super().__init__(master, **kwards)

        self.configure(height=50)

        # row and column configure
        self.grid_rowconfigure(0, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # widgets
        self.logo_img = getImage('./media/logo.png', 30, 30)
        self.logo = ctk.CTkLabel(self, text='', image=self.logo_img)
        self.logo.grid(row=0, column=0, pady=10, padx=30, sticky='nw')



class App(ctk.CTk):

    WIDTH = 950
    HEIGHT = 550
    TITLE = 'Tasky'

    def __init__(self):
        super().__init__()

        self.title(self.TITLE)
        self.geometry(f'{self.WIDTH}x{self.HEIGHT}')
        center_window(self, self.WIDTH, self.HEIGHT)

        # row and column configure
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.grid_columnconfigure(0, weight=1)

        # widgets
        self.top_frame = TopFrame(master=self, width=10)
        self.top_frame.grid(row=0, column=0, sticky='new')


if __name__ == '__main__':
    app = App()
    app.mainloop()
