import sys
from pathlib import Path
from datetime import datetime, timedelta
import json

if __name__ == "__main__":
    sys.path.append(str(Path(__file__).parent.parent / "Classes"))

from Event import Event
from Note import Note
from Notebook import Notebook
from PlannerEntry import PlannerEntry
from ToDo import ToDo

savePath = Path(__file__).parent

def _get_safe_name(originalString : str, folder : Path, jsonMode = False) -> str:
    returnString = originalString
    number = 2
    while (folder / (returnString + ".json")).exists():
        returnString = originalString + str(number)
        number += 1
        if number > 100000:
            raise Exception("Something is wrong. There can't be 100000 of the same note!")
    
    if jsonMode:
        returnString += ".json"
    return returnString

# saves a note!
# if newFile, a new .json file will always be created.
# otherwise, save_note can overwrite notes with the same title.
def save_object(object : Note | Notebook | Event | PlannerEntry | ToDo, newFile : bool = False) -> None:
    saveFolderName = ''
    
    if isinstance(object, Note):
        saveFolderName = "Notes"
        fileName = object.title
    elif isinstance(object, Notebook):
        saveFolderName = "Notebooks"
        fileName = object.title
    elif isinstance(object, (Event, PlannerEntry, ToDo)):
        saveFolderName = "Entries"
        fileName = object.name
    
    if newFile:
        fileName = _get_safe_name(fileName, savePath / saveFolderName)
        object.title = fileName
    
    fileName = fileName + '.json'
    
    with open(savePath / saveFolderName / fileName, 'w') as file:
        json.dump(object.to_dict(), file, indent=3)

# saves a list or tuple of objects.
def save_objects(objectList : list[object : Note | Notebook | Event | PlannerEntry | ToDo], newFile : bool = False):
    for object in objectList:
        save_object(object=object, newFile=newFile)

# reads all notes
def read_notes() -> list[Note]:
    noteSavePath = savePath / "Notes"
    noteList = []
    for noteJsonPath in noteSavePath.iterdir():
        with open(noteJsonPath, 'r') as noteJson:
            note = Note.from_dict(json.load(noteJson))
            noteList.append(note)
    return noteList

def read_notebooks() -> list[Notebook]:
    specificSavePath = savePath / "Notebooks"
    returnList = []
    for jsonPath in specificSavePath.iterdir():
        with open(jsonPath, 'r') as jsonFile:
            note = Notebook.from_dict(json.load(jsonFile))
            returnList.append(note)
    return returnList

# slightly more complicated. This one tests the attributes in the dictionary to figure out what class / subclass this Entry is.
def read_entries() -> list[PlannerEntry | Event | ToDo]:
    specificSavePath = savePath / "Entries"
    returnList = []
    for jsonPath in specificSavePath.iterdir():
        with open(jsonPath, 'r') as jsonFile:
            dictionary : dict = json.load(jsonFile)

            # test keys and figure out class
            if dictionary.__contains__("repeats"):
                entry = Event.from_dict(dictionary)
            elif dictionary.__contains__("completed"):
                entry = ToDo.from_dict(dictionary)
            else:
                entry = PlannerEntry.from_dict(dictionary)

            returnList.append(entry)
    return returnList

def delete_object(object : Note | Notebook | Event | PlannerEntry | ToDo):
    saveFolderName = ''
    
    if isinstance(object, Note):
        saveFolderName = "Notes"
        fileName = object.title
    elif isinstance(object, Notebook):
        saveFolderName = "Notebooks"
        fileName = object.title
    elif isinstance(object, (Event, PlannerEntry, ToDo)):
        saveFolderName = "Entries"
        fileName = object.name
    
    fileName += '.json'
    
    filePath = savePath / saveFolderName / fileName
    filePath.unlink()
        


if __name__ == "__main__":
    '''
    note1 = Note("This is another note")
    save_object(note1, True)
    
    print(read_notes())
    '''
    '''
    notebook = Notebook("This is a cool notebook")
    save_object(notebook, True)
    print(read_notebooks())
    '''
    '''
    save_object(Event(), True); save_object(ToDo(), True); save_object(PlannerEntry(), True)
    print(read_entries())
    '''

    # make some bogus events
    event1 = Event("First Event")
    event2 = PlannerEntry("Second Planner Entry", occurance=datetime.today() + timedelta(1))
    event3 = ToDo("Third ToDo", occurance=datetime.today() + timedelta(1))
    event4 = Event("Fourth Event", color="#0000FF", occurance= datetime.today())

    # save_object(event1); save_object(event2); save_object(event3); save_object(event4)

    for i in range(16):
        event = ToDo(f"Event {str(i)}", "This is stupid", datetime.today() + timedelta(i), f"#FF00{(i*16 + i):X}")
        save_object(event)
