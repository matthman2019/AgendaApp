# A notebook. It holds notes

from dataclasses import dataclass
from Note import Note, datetime
import json

titlesUsed = []

class Notebook:

    def __init__(self, title : str = "Untitled Notebook", notes : list = []):
        global titlesUsed
        while title in titlesUsed:
            title += "2"
        self.title = title
        self.notes = []
    
    def __str__(self):
        return f"Notebook: {self.title}"

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

    @classmethod
    def from_dict(cls, dictionary:dict) -> "Notebook":
        newNotebook = Notebook()
        newNotebook.title = dictionary["title"]
        return newNotebook



if __name__ == "__main__":
    notebook = Notebook("E")
    note = Note("The First Note", datetime.today(), "This is the first note!", None)
    notebook.add_note(note)
    print(notebook.to_json())
    print(note.to_json())