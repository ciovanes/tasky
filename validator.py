import re
from datetime import datetime

class Validator:

    def __init__(self):
        self.errors = []


    def validate_task_name(self, task_name: str):
        self.clear_errors()

        if task_name == '':
            error_msg = "Task name cannot be empty!"
            self.errors.append(error_msg)

        return not bool(self.errors)


    def validate_due_date(self, due_date: str):
        self.clear_errors()

        due_date = due_date.strip()

        date_regex = r'^\d{2}/\d{2}/\d{4}$'
        print(due_date)

        if not re.match(date_regex, due_date):
            error_msg = "Invalid date format! Use dd/mm/yyyy"
            self.errors.append(error_msg)
        else:
            try:
                datetime.strptime(due_date, '%d/%m/%Y')
            except ValueError:
                error_msg = "Invalid date!"
                self.errors.append(error_msg)

        return not bool(self.errors)


    def get_errors(self):
        return self.errors


    def clear_errors(self):
        self.errors.clear()
