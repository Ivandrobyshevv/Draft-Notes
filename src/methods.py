import datetime
import json
from json import JSONDecodeError


class Method:
    def __init__(self):
        self.__date_now = datetime.datetime.now()
        self.pk = 1
        self.to_json = {}
        self.date = f'{self.__date_now.day}/{self.__date_now.month}/{self.__date_now.year}'
        self.time = f'{self.__date_now.hour}:{self.__date_now.minute}'

    def render_note(self, title, body):
        """Рендер заметки"""
        note = {}
        self.update_pk()
        note['title'] = title
        note['body'] = body
        note['date'] = self.date
        note['time'] = self.time
        self.to_json[self.pk] = note
        self.save_json()

    def get_note_all(self):
        """Получение всех заметок"""
        notes: dict = self.read_json()
        return notes

    def filter_date_notes(self, date: str):
        """Фильтрует заметки по дате"""
        notes_list = []
        file_json = self.read_json()
        for key, value in file_json.items():
            if value['date'] == date:
                notes_list.append({key: file_json.get(key)})
        if len(notes_list) < 1:
            return "Записей с такой датой нет"
        return notes_list

    def correct_note(self, pk, title, body):
        """Изменение заметки"""
        file_json = self.read_json()
        file_json[pk]['title'] = title
        file_json[pk]['body'] = body
        file_json[pk]['date'] = self.date
        file_json[pk]['time'] = self.time
        self.write_json(file_json)

    def update_pk(self):
        """Обновления первичного ключа"""
        file_json = self.read_json()
        if file_json is None:
            self.pk = 1
        else:
            last_pk = max(map(int, file_json))
            self.pk = last_pk + 1

    def save_json(self):
        """Сохранение заметки в notes.json"""
        file_json_dict: dict = self.read_json()
        if file_json_dict is None:
            json_data = self.to_json
        else:
            json_data = file_json_dict | self.to_json
        self.write_json(json_data)

    def delete_json(self, pk):
        """Удаление заметки из списка"""
        data_json = self.read_json()
        if data_json is not None:
            delete_note = data_json.pop(pk, 'Значения с таким ключом нет')
            self.write_json(data_json)
            return delete_note
        return "Заметок нет создайте"

    @staticmethod
    def write_json(json_data):
        with open('notes.json', 'w') as file_json:
            json.dump(json_data, file_json)

    @staticmethod
    def read_json():
        try:
            with open('notes.json', 'r') as file_json:
                return json.load(file_json)
        except JSONDecodeError:
            return None
