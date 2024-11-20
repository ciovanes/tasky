import customtkinter as ctk
from utils import *
from enum import Enum
from tkinter import ttk
import tkinter as tk
from validator import Validator
from tkinter import messagebox
from datetime import datetime
import random as rd


class ColorMode(Enum):
    DARK = 'dark'
    LIGHT = 'light'


class TaskState(Enum):
    DOING = 'doing'
    DONE = 'done'


class TaskPriority(Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'


"""
    TODO
"""
class EditTaskFrame(ctk.CTkToplevel):

    WIDTH = 400
    HEIGHT = 300

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry(f'{self.WIDTH}x{self.HEIGHT}')
        self.title('Edit task')

        center_window(self, self.WIDTH, self.HEIGHT)

        self.label = ctk.CTkLabel(self, text="ToplevelWindow")
        self.label.pack(padx=20, pady=20)


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
        self.logo_img = getImage('./media/logo.png', 50, 50)
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
        # self.view_frame = view_frame

        # row and column configure
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.grid_columnconfigure(0, weight=1, uniform='equal')
        self.grid_columnconfigure(1, weight=1, uniform='equal')
        self.grid_columnconfigure(2, weight=1, uniform='equal')
        self.grid_columnconfigure(3, weight=1, uniform='equal')

        # widgets
        # task name
        ctk.CTkLabel(self, text='*Task name:').grid(row=0, column=0)
        self.task_name = ctk.CTkEntry(self, placeholder_text='Task name')
        self.task_name.grid(row=1, column=0, padx=20)

        self.error_task_name = ctk.CTkLabel(self, text='', text_color='red')
        self.error_task_name.grid(row=2, column=0)

        # task priority
        priority_values = [TaskPriority.LOW.value,
                           TaskPriority.MEDIUM.value,
                           TaskPriority.HIGH.value]
        ctk.CTkLabel(self, text='Priorities:').grid(row=0, column=1)
        self.task_priority = ctk.CTkComboBox(self, values=priority_values)
        self.task_priority.grid(row=1, column=1)

        # task due date
        ctk.CTkLabel(self, text='Due date:').grid(row=0, column=2)
        self.due_date = ctk.CTkEntry(self, placeholder_text='dd/mm/aaaa')
        self.due_date.grid(row=1, column=2)

        self.error_due_date = ctk.CTkLabel(self, text='', text_color='red')
        self.error_due_date.grid(row=2, column=2)

        # create task
        self.create_task = ctk.CTkButton(self, text='Create task', command=self.get_new_task)
        self.create_task.grid(row=1, column=3)

        self.validator = Validator()


    def get_new_task(self):
        name = self.task_name.get()
        priority = self.task_priority.get()
        state = TaskState.DOING.value
        due_date = self.due_date.get()
        creation_date = datetime.now().strftime('%d/%m/%Y')

        print(name)
        if not self.validator.validate_task_name(name):
            name_error_msg = self.validator.get_errors()[0]
            generate_text(self, self.error_task_name, name_error_msg, 1500)
            return

        if not self.validator.validate_due_date(due_date):
            date_error_msg = self.validator.get_errors()[0]
            generate_text(self, self.error_due_date, date_error_msg, 1500)
            return

        print(f'Task name: {name}, Task priority: {priority}, Task due date: {due_date}')
        self.master.view_frame.add_new_row(name, priority, state, due_date, creation_date)

        self.clear_entry()

    def clear_entry(self):
        self.task_name.delete(0, 'end')
        self.due_date.delete(0, 'end')


class ViewFrame(ctk.CTkFrame):

    total_tasks = 0
    complete_tasks = 0

    def __init__(self, master, **kwards):
        super().__init__(master, **kwards)

        # row and column configure
        self.grid_rowconfigure(0, weight=1)

        self.grid_columnconfigure(0, weight=1)

        # widgets
        columns = ('name', 'priority', 'state', 'due_date', 'creation_date')
        self.tree = ttk.Treeview(self, columns=columns, show='headings')

        # define headings
        self.tree.heading(columns[0], text='Task')
        self.tree.heading(columns[1], text='Priority')
        self.tree.heading(columns[2], text='State')
        self.tree.heading(columns[3], text='Due date')
        self.tree.heading(columns[4], text='Creation date')

        # configure columns
        self.tree.column(columns[1], width=100)
        self.tree.column(columns[2], width=70)

        self.tree.grid(row=0, column=0, sticky='nsew')

        data = self.generate_sample_data()

        for d in data:
            self.tree.insert('', tk.END, values=d)

        self.tree_scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.tree_scrollbar.set)
        self.tree_scrollbar.grid(row=0, column=1, sticky='ns')

    def generate_sample_data(self):
        data = []
        priorities = [TaskPriority.LOW.value, TaskPriority.MEDIUM.value, TaskPriority.HIGH.value]
        states = [TaskState.DOING.value, TaskState.DONE.value]
        for n in range(1, 10):
            self.total_tasks += 1
            act_sate = rd.choice(states)
            if (act_sate == TaskState.DONE.value):
                self.complete_tasks += 1
            data.append((f'task {n}', f'{rd.choice(priorities)}', f'{act_sate}', '', datetime.now().strftime('%d/%m/%Y')))
        return data

    def add_new_row(self, name, priority, state, due_date, creation_date):
        self.total_tasks += 1
        self.tree.insert('', 'end', values=(name, priority, state, due_date, creation_date))
        self.master.bottom_frame.update_labels()

    def delete_row(self):
        items = self.tree.selection()

        if not items:
            messagebox.showinfo(title='EY', message='You need to select an item to delete it')
            return

        for i in items:
            self.total_tasks -= 1

            item_values = self.tree.item(i)['values']
            # print(item_values[2])

            if item_values[2] == TaskState.DONE.value:
                self.complete_tasks -= 1

            self.tree.delete(i)
            self.master.bottom_frame.update_labels()

        generate_text(self, self.master.bottom_frame.info_label, 'Task deleted!', 1500)

    def complete_task(self):
        items = self.tree.selection()

        if not items:
            messagebox.showinfo(title='EY', message='You need to select an item to complete it')
            return

        for i in items:
            item_values = self.tree.item(i)['values']

            if item_values[2] == TaskState.DOING.value:
                new_value = (item_values[0], item_values[1], TaskState.DONE.value, item_values[3], item_values[4])
                self.tree.item(i, values=new_value)
                print('se ha actualizado la task')
                self.complete_tasks += 1
                self.master.bottom_frame.update_labels()

                generate_text(self, self.master.bottom_frame.info_label, 'Task completed!', 1500)

    def get_total_tasks(self):
        return self.total_tasks

    def get_complete_tasks(self):
        return self.complete_tasks


class BottomFrame(ctk.CTkFrame):

    def __init__(self, master, **kwards):
        super().__init__(master, **kwards)

        # row and column configure
        self.grid_rowconfigure(0, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # left frame
        self.left_frame = ctk.CTkFrame(self)
        self.left_frame.grid(row=0, column=0, sticky='w')

        self.left_frame.grid_columnconfigure(0, weight=1)
        self.left_frame.grid_columnconfigure(1, weight=1)
        self.left_frame.grid_columnconfigure(2, weight=1)
        self.left_frame.grid_columnconfigure(3, weight=1)
        self.left_frame.grid_columnconfigure(4, weight=1)

        self.left_frame.grid_columnconfigure(0, weight=1)

        # left frame widgets
        ctk.CTkLabel(self.left_frame, text='').grid(row=0, column=0, padx=10)
        self.delete_button = ctk.CTkButton(self.left_frame, text='X', corner_radius=20, width=10,
                                           command=self.master.view_frame.delete_row)
        self.delete_button.grid(row=0, column=1, sticky='w', padx=10)

        self.edit_button= ctk.CTkButton(self.left_frame, text='E', corner_radius=20, width=10,
                                        command=self.open_edit_frame)
        self.edit_button.grid(row=0, column=2, sticky='w', padx=5, pady=5)

        self.done_button= ctk.CTkButton(self.left_frame, text='D', corner_radius=20, width=10,
                                        command=self.master.view_frame.complete_task)
        self.done_button.grid(row=0, column=3, sticky='w', padx=10)

        self.info_label = ctk.CTkLabel(self.left_frame, text='', text_color='green')
        self.info_label.grid(row=0, column=4, sticky='w', padx=10)


        # right frame
        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.grid(row=0, column=1, sticky='e')

        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_columnconfigure(1, weight=1)

        self.right_frame.grid_rowconfigure(0, weight=1)

        # right frame widgets
        self.task_counter = ctk.CTkLabel(self.right_frame, text='')
        self.task_counter.grid(row=0, column=0, sticky='e', padx=20, pady=5)

        self.done_tasks_counter = ctk.CTkLabel(self.right_frame, text='')
        self.done_tasks_counter.grid(row=0, column=1, sticky='e', padx=10)

        self.update_labels()


    def update_labels(self):
        task_counter_text = f'Total tasks: {self.master.view_frame.get_total_tasks()}'
        self.task_counter.configure(text=task_counter_text)

        done_tasks_counter_text = f'Complete tasks: {self.master.view_frame.get_complete_tasks()}'
        self.done_tasks_counter.configure(text=done_tasks_counter_text)

    def open_edit_frame(self):
       edit_frame_tl =  EditTaskFrame(self)


class App(ctk.CTk):

    WIDTH = 950
    HEIGHT = 550
    TITLE = 'Tasky'

    def __init__(self):
        super().__init__()

        self.title(self.TITLE)
        self.geometry(f'{self.WIDTH}x{self.HEIGHT}')
        center_window(self, self.WIDTH, self.HEIGHT)

        # widgets
        self.top_frame = TopFrame(master=self)
        self.top_frame.pack(fill='x')

        self.create_task_frame = CreateTaskFrame(master=self)
        self.create_task_frame.pack(fill='x')

        self.view_frame = ViewFrame(master=self)
        self.view_frame.pack(fill='both', expand=True, padx=20)

        self.bottom_frame = BottomFrame(master=self)
        self.bottom_frame.pack(fill='both', padx=20)

        ctk.CTkLabel(self, text='', height=10).pack()


if __name__ == '__main__':
    app = App()
    app.mainloop()
