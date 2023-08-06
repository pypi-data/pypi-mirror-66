from pathlib import Path
import json
import os


class LocalStorage:
    def __init__(self):
        self.validate_storage_path()

    name = "Local Storage"
    storage_path = Path(str(Path.home())+"/.takemeto")

    def validate_storage_path(self):
        if self.storage_path.exists():
            return True
        else:
            self.make_new_storage()

    @property
    def destinations(self):
        return self.read()

    def read(self):
        return json.loads(self.storage_path.read_bytes())

    def write(self, content):
        with self.storage_path.open(mode='w+') as f:
            f.write(content)

    def make_new_storage(self):
        self.write("{}")
