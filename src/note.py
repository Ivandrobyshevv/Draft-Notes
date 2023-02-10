from datetime import datetime

from src.methods import Method


class Note:
    def __init__(self):
        self.methods = Method()
        self.commands = {
            'add': self.cmd_add,
            'show': self.cmd_show,
            'delete': self.cmd_delete,
            'edit': self.cmd_edit,
            'filter': self.cmd_filter,
            'exit': self.cmd_exit
        }

    def start_program(self):
        print("Список команд:\n"
              "add - добавить запись\n"
              "show - вывести все записи\n"
              "filter - фильтровать записи по дате\n"
              "edit - изменить запись\n"
              "exit - выти из программы")
        cmd = self.get_command()
        stop = self.commands.get(cmd, False)
        if stop:
            return stop

    @staticmethod
    def get_command():
        cmd = input(">> ")
        return cmd

    def cmd_add(self):
        """Обработчик команды add"""
        title, body = self.get_data_note()
        self.methods.render_note(title, body)
        print(f"Замета {title} - успешно добавлена!")

    def cmd_show(self):
        """Обработчик команды show"""
        notes: dict = self.methods.get_note_all()
        self.show_notes(notes)

    def cmd_delete(self):
        """Обработчик команды delete"""
        pk = self.get_pk_note()
        answer = self.methods.delete_json(pk)
        print(answer)

    def cmd_edit(self):
        """Обработчик команды edit"""
        pk = self.get_pk_note()
        title, body = self.get_data_note()
        self.methods.correct_note(pk, title, body)

    def cmd_filter(self):
        """Обработчик команды filter"""
        date_note = self.get_date()
        notes = self.methods.filter_date_notes(date_note)
        if isinstance(notes, list):
            self.show_notes(notes)
        else:
            print(notes)

    @staticmethod
    def cmd_exit():
        """Обработчик команды exit"""
        print("Выход из программы")
        return True

    def get_date(self):
        """Получение даты"""
        while True:
            print("Введите дату в формате: день.месяц.год")
            date = input('>> ')
            date_list = date.split(".")
            if self.check_separator(date_list):
                if date_correct := self.check_date(date_list):
                    return date_correct
                else:
                    continue
            else:
                print("Проверти разделите межу день.месяц.год!\n"
                      f"Вы ввели - {date}")

    def check_date(self, date_list: list):
        """Проверка даты на корректность"""
        day = self.check_day(date_list[0])
        month = self.check_month(date_list[1])
        year = self.check_year(date_list[2])
        print(all([day, month, year]))
        if not all([day, month, year]):
            return False
        else:
            return f'{day}/{month}/{year}'

    @staticmethod
    def check_separator(date):
        """Проверка разделителя меду значениями даты """
        if len(date) == 3:
            return True
        return False

    @staticmethod
    def check_day(day: str):
        """Проверка дня на корректность"""
        if int(day) > 31:
            print("День не может быть больше 31\n"
                  f"Вы ввели - {day}")
            return False
        else:
            return day

    @staticmethod
    def check_month(month: str):
        """Проверка месяца на корректность"""
        if month[0] == '0':
            format_month = month[1]
        else:
            format_month = month

        if int(format_month) > 12 or int(format_month) < 1:
            print("Проверте корректность месяца, месяц должен быть от 1 до 12\n"
                  f"Вы ввели {month}")
            return False
        else:
            return format_month

    @staticmethod
    def check_year(year: str):
        """Проверка год на корректность"""
        if len(year) < 2:
            format_year = '20' + year
        else:
            format_year = year

        if int(format_year) > 2023:
            print("Значение года не может быть больше чем 2023!\n"
                  f"Вы ввели - {year}")
            return False
        else:
            return format_year

    @staticmethod
    def get_pk_note():
        """Получения pk от пользователя"""
        while True:
            value_pk = input("Введите номер идентификатора")
            if value_pk.isdigit():
                return value_pk
            else:
                continue

    @staticmethod
    def show_notes(notes):
        if isinstance(notes, dict):
            for pk, value in notes.items():
                print(f"{pk} - {value['title']}\n"
                      f"{value['body']}\n"
                      f"{value['date']} {value['time']}")
        else:
            for note in notes:
                for pk, value in note.items():
                    print(f"{pk} - {value['title']}\n"
                          f"{value['body']}\n"
                          f"{value['date']} {value['time']}")

    @staticmethod
    def get_data_note():
        """Получение информации для заметки"""
        title = input('title')
        body = input('body')
        return title, body

    @staticmethod
    def show_into():
        """Вывод названия программы"""
        print("Draft Notes")
