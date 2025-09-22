# A notebook. It holds notes

from dataclasses import dataclass
from Note import Note, datetime
import json

class Notebook:
    
    titlesUsed = []

    def __init__(self, title : str = "Untitled Notebook", notes : list = []):
        while title in Notebook.titlesUsed:
            title += "2"
        self.title = title
        self.notes = []

    def add_note(self, note : Note):
        note.notebook = self.title
        self.notes.append(note)

    def to_dict(self):
        my_dict = {}

        for attributeName in dir(self):
            # don't put dunder methods or dunder attributes in the dictionary
            if attributeName.endswith("__"):
                continue
            
            # don't put methods in the dictionary
            attribute = getattr(self, attributeName)
            if callable(attribute):
                continue

            value = getattr(self, attributeName)
            
            # making sure that attribut
            if attributeName == "notes":
                continue
            my_dict[attributeName] = value
        return my_dict
    
    def to_json(self):
        return json.dumps(self.to_dict())

if __name__ == "__main__":
    notebook = Notebook("E")
    note = Note("The First Note", datetime.today(), "This is the first note!", None)
    notebook.add_note(note)
    print(notebook.to_json())
    print(note.to_json())