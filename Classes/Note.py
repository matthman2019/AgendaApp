# A note is, well, a note. Like a page in a notebook, it has a title and a body.

from datetime import datetime, timedelta
from dataclasses import dataclass, field
import json

@dataclass
class Note:
    title : str = "Untitled Note"
    lastedit : datetime = datetime.today()
    body : str = ""
    notebook : str | None = None

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
            if isinstance(value, datetime):
                value = value.isoformat()
            elif isinstance(value, timedelta):
                repetionTime = value
                # I got angry, so this is my solution. No fancy methods. Just storing days, seconds, and microseconds
                value = f"{str(repetionTime.days)}/{str(repetionTime.seconds)}/{str(repetionTime.microseconds)}"
            my_dict[attributeName] = value
        return my_dict
    
    def to_json(self):
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, dictionary : dict):
        newNote = Note()
        newNote.title = dictionary["title"]
        newNote.lastedit = datetime.fromisoformat(dictionary["lastedit"])
        newNote.body = dictionary["body"]
        newNote.notebook = dictionary["notebook"]
        return newNote
    

if __name__ == "__main__":
    note = Note("The First Note", datetime.today(), "This is the first note!", None)
    note2 = Note.from_dict(note.to_dict())
    print(note)
    print(note2)