from pathlib import Path
import re

class NameValidator():
    def check_end_symbol(self, *args):
        pattern = r"[?*]$"
        end_with_symbol = re.search(pattern, *args)
        return end_with_symbol


class FileFinder(NameValidator):
    def __init__(self, name, recursive=True):
        self.name = name
        self.path = Path().cwd()
        self.recursive = recursive
        self.file_list = [file for file in self.get_file_list()]

    def add_star(self):
        if NameValidator.check_end_symbol(self, self.name):
            pass
        else:
            self.name += "*"
        return self.name
    
    def get_file_list(self):
        self.add_star()
        
        if self.recursive:
            self.name = "**/" + self.name
            self.file_list = self.path.glob(self.name)
        else:
            self.file_list = self.path.glob(self.name)
        return self.file_list