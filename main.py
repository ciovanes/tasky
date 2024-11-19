import customtkinter as ctk
from utils import *
from enum import Enum
from tkinter import ttk
import tkinter as tk


class ColorMode(Enum):
    DARK = 'dark'
    LIGHT = 'light'


class TopFrame(ctk.CTkFrame):

    color_mode = ColorMode.DARK.value

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

        self.theme_button = ctk.CTkButton(self, text='L', corner_radius=100, width=30, height=30, command=self.change_theme)
        self.theme_button.grid(row=0, column=1, pady=10, padx=30, sticky='ne')


    def change_theme(self):
        self.color_mode = ColorMode.LIGHT.value if (self.color_mode == ColorMode.DARK.value) else ColorMode.DARK.value
        ctk.set_appearance_mode(self.color_mode)

        theme_button_text = ColorMode.LIGHT.value if (self.color_mode == ColorMode.DARK.value) else ColorMode.DARK.value
        theme_button_text = theme_button_text[0].upper()
        self.theme_button.configure(text=theme_button_text)


class CreateTaskFrame(ctk.CTkFrame):

    def __init__(self, master, **kwards):
        super().__init__(master, **kwards)

        # row and column configure
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.grid_columnconfigure(0, weight=1, uniform='equal')
        self.grid_columnconfigure(1, weight=1, uniform='equal')
        # self.grid_columnconfigure(2, weight=1, uniform='equal')
        self.grid_columnconfigure(3, weight=1, uniform='equal')

        # widgets
        self.task_name = ctk.CTkEntry(self, placeholder_text='Task name')
        self.task_name.grid(row=0, column=0, padx=20)

        self.error_task_name = ctk.CTkLabel(self, text='', text_color='red')
        self.error_task_name.grid(row=1, column=0)

        priority_values = ['Low', 'Medium', 'Hight']
        self.task_priority = ctk.CTkComboBox(self, values=priority_values)
        self.task_priority.grid(row=0, column=1)

        self.create_task = ctk.CTkButton(self, text='Create task', command=self.get_new_task)
        self.create_task.grid(row=0, column=3)


    def get_new_task(self):
        try:
            task_name = self.task_name.get()
            task_priority = self.task_priority.get()
            assert(task_name != '')
            print(f'Task name: {task_name}, Task priority: {task_priority}')
        except AssertionError:
            self.change_error_text()

    def change_error_text(self):
        self.error_task_name.configure(text="Task name can't be blank")
        self.after(1500, self.clear_error_text)

    def clear_error_text(self):
        self.error_task_name.configure(text='')


class ViewFrame(ctk.CTkFrame):

    def __init__(self, master, **kwards):
        super().__init__(master, **kwards)

        # row and column configure
        self.grid_rowconfigure(0, weight=1)

        self.grid_columnconfigure(0, weight=1)

        # widgets
        columns = ('task_name', 'task_priority', 'task_state')
        self.tree = ttk.Treeview(self, columns=columns, show='headings')

        # define headings
        self.tree.heading(columns[0], text='Task')
        self.tree.heading(columns[1], text='Priority')
        self.tree.heading(columns[2], text='State')

        self.tree.grid(row=0, column=0, sticky='nsew')

        data = self.generate_sample_data()

        for d in data:
            self.tree.insert('', tk.END, values=d)

        self.tree_scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.tree_scrollbar.set)
        self.tree_scrollbar.grid(row=0, column=1, sticky='ns')

    def generate_sample_data(self):
        data = []
        for n in range(1, 100):
            data.append((f'task {n}', f'priority {n}', f'state {n}'))
        return data


class BottomFrame(ctk.CTkFrame):

    def __init__(self, master, **kwards):
        super().__init__(master, **kwards)

        # row and column configure
        self.grid_rowconfigure(0, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

        # widgets
        self.task_name = ctk.CTkEntry(self)
        self.task_name.grid(row=0, column=0)


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
        # self.grid_rowconfigure(0, weight=1)
        # self.grid_rowconfigure(1, weight=2)
        # self.grid_rowconfigure(2, weight=9)
        # self.grid_rowconfigure(3, weight=2)

        # self.grid_columnconfigure(0, weight=1)

        # widgets
        self.top_frame = TopFrame(master=self)
        # self.top_frame.grid(row=0, column=0, sticky='new')
        self.top_frame.pack(fill='x')

        self.create_task_frame = CreateTaskFrame(master=self)
        # self.create_task_frame.grid(row=1, column=0, sticky='new')
        self.create_task_frame.pack(fill='x')

        self.view_frame = ViewFrame(master=self)
        # self.view_frame.grid(row=2, column=0, sticky='nsew')
        self.view_frame.pack(fill='both', expand=True)

        self.bottom_frame = BottomFrame(master=self)
        # self.bottom_frame.grid(row=3, column=0, sticky='sew')
        self.bottom_frame.pack()


if __name__ == '__main__':
    app = App()
    app.mainloop()
