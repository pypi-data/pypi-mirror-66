from pathlib import Path
import json


class JReader():
    def __init__(self):
        self.dictionary_list = []
        self.value_list = []

    def json_dispenser(self, file_list) -> list:
        for file_path in file_list:
            file_name = file_path.name
            content = self.read_json_file(file_path)
            dictionary = {file_name: content}
            self.dictionary_list.append(dictionary)
        return self.dictionary_list

    def read_json_file(self, file_path) -> dict:
        with file_path.open() as f:
            j = f.read()
            content = json.loads(j)
        return content
