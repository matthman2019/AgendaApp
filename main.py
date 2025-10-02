import calendar
import datetime
import time
from random import randint
import sys
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import Label, Frame, Button, Checkbutton
from ttkbootstrap import dialogs, scrolled, widgets, colorutils
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.dialogs.colorchooser import ColorChooserDialog
from ttkbootstrap.constants import *

sys.path.append("Classes")
sys.path.append("Saves")

from RepeatingEvent import RepeatingEvent
from Event import Event
from ToDo import ToDo
from Notebook import Notebook
from Note import Note
from DataManager import save_objects, read_entries, read_notebooks, read_notes, delete_object
from EntryWidget import EntryWidget

# list setup
entryList = read_entries()
entryList.sort()
notebookList = read_notebooks()
noteList = read_notes()

def get_notebook_by_title(title:str) -> Notebook:
    for notebook in notebookList:
        if notebook.title == title:
            return notebook
    return None

# make untitled notebook if necessary
UNTITLED = "Untitled"
untitledNotebook = get_notebook_by_title(UNTITLED)
if untitledNotebook == None:
    untitledNotebook = Notebook(UNTITLED)
    notebookList.insert(0, untitledNotebook)

# parent notes to notebooks
# if the notebook doesn't exist, parent them to untitled notebook
def refresh_notebook_notes():
    for notebook in notebookList:
        notebook.notes = []
    for note in noteList:
        localNotebook = get_notebook_by_title(note.notebook)
        if localNotebook == None:
            note.notebook = UNTITLED
            untitledNotebook.notes.append(note)
        else:
            localNotebook.notes.append(note)
refresh_notebook_notes()
    

def save_lists():
    global entryList, notebookLabel, noteList
    save_objects(entryList); save_objects(notebookList); save_objects(noteList)

root = ttk.Window(title="Notes App", themename="sandstone")
root.geometry("800x800")
rootNotebook = ttk.Notebook(root, style="sandstone")
rootNotebook.pack(fill=BOTH, expand=True)

upcomingFrame = Frame(rootNotebook)
calendarFrame = Frame(rootNotebook)
newEventFrame = Frame(rootNotebook)
noteFrame = Frame(rootNotebook)
rootNotebook.add(upcomingFrame, text="Upcoming")
rootNotebook.add(calendarFrame, text="Calendar")
rootNotebook.add(newEventFrame, text="New Event")
rootNotebook.add(noteFrame, text="Notebook")

# upcoming frame
upcomingFrameLabel = Label(upcomingFrame, text="Upcoming Events")
upcomingFrameLabel.pack()
upcomingEventsFrame = scrolled.ScrolledFrame(upcomingFrame, autohide=True)
upcomingEventsFrame.pack(expand=True, fill=BOTH)
# calendar frame
calendarFrameLabel = Label(calendarFrame, text="Calendar of Events")
calendarFrameLabel.pack()
# new event frame
newEventLabel = Label(newEventFrame, text="New Event")
newEventLabel.grid(row=0, column=0, columnspan=2)
# notebook frame
notebookLabel = Label(noteFrame, text="Notes")
notebookLabel.grid(row=0, column=0, columnspan=1)

# handle notebook tab changes
currentlyOpenTab = "Upcoming"
def tab_changed(event : tk.Event):
    notebook : ttk.Notebook = event.widget
    selectedTabText = notebook.tab(notebook.select(), "text")

    # show upcoming events
    if selectedTabText == "Upcoming":
        display_event_list()
rootNotebook.bind("<<NotebookTabChanged>>", tab_changed)

# display entries in upcomingEventsFrame
def display_event_list():
    global entryList

    # while this is defined in EntryWidget class, I'm going to override this method to make deleting work.
    def remove_from_entry_list(entry : EntryWidget):
        del entryList[entryList.index(entry.entry)]
        delete_object(entry.entry)
        display_event_list()
    
    for widget in upcomingEventsFrame.winfo_children():
        widget.destroy()
    entryList.sort()
    for entry in entryList:
        eventFrame = EntryWidget(master=upcomingEventsFrame, entry=entry)
        eventFrame.default_pack()
        eventFrame.onDeleteCallback = remove_from_entry_list

# calendar tab (eventually)

# new event tab
# row 1: name
eventNameLabel = Label(newEventFrame, text="Event Name")
eventNameLabel.grid(row=1, column=0)
eventNameEntry = ttk.Entry(newEventFrame)
eventNameEntry.grid(row=1, column=1)

# row 2: event description
eventDescriptionLabel = Label(newEventFrame, text="Description")
eventDescriptionLabel.grid(row=2, column=0)
eventDescriptionTextbox = scrolled.ScrolledText(newEventFrame, height=5, width=50, autohide=True)
eventDescriptionTextbox.grid(row=2, column=1, sticky="WE")

# row 3: occurance
eventOccuranceLabel = Label(newEventFrame, text="Occurance")
eventOccuranceLabel.grid(row=3, column=0)
eventDateChooser = widgets.DateEntry(newEventFrame, popup_title="Choose Date")
eventDateChooser["state"] = "normal"
eventDateChooser.grid(row=3, column=1)

# row 4: color
newEventColor = 'FF0000'
def chooseNewColor():
    global newEventColor, eventColorButton
    cd = ColorChooserDialog(root, "Choose a color for the new event")
    cd.show()
    newEventColor = cd.result.hex
    print(newEventColor)
    eventColorButtonStyle.configure("NewEventButton.TButton", background=newEventColor)
eventColorLabel = Label(newEventFrame, text="Color")
eventColorLabel.grid(row=4, column=0)
eventColorButtonStyle = ttk.Style()
eventColorButtonStyle.configure("NewEventButton.TButton", background=newEventColor)
eventColorButton = Button(newEventFrame, text="Click me to select a color", command=chooseNewColor)
eventColorButton.grid(row=4, column=1)

# row 5: can be completed?
eventCompletedLabel = Label(newEventFrame, text="Can this event be completed?")
eventCompletedLabel.grid(row=5, column=0)
eventCompletedBoolVar = tk.BooleanVar(newEventFrame, value=True)
eventCompletedButton = Checkbutton(newEventFrame, bootstyle='round-toggle', variable=eventCompletedBoolVar)
eventCompletedButton.grid(row=5, column=1)

# row 6: make new event!
def complete_new_event():
    # name
    eventName = eventNameEntry.get()
    if eventName.strip(" ") == "":
        Messagebox.show_error("You need to give your event a name!", "Could not make event", root, alert=False)
        return
    # description (can be none)
    eventDescription = eventDescriptionTextbox.get("1.0", "end-1c")
    # occurance
    eventOccurance = eventDateChooser.get_date()
    # color
    eventColor = newEventColor
    # if the event can be completed, make a ToDo
    if eventCompletedBoolVar.get():
        newEvent = ToDo(eventName, eventDescription, eventOccurance, eventColor, False)
    
    # otherwise, just make an Event
    else:
        newEvent = Event(eventName, eventDescription, eventOccurance, eventColor)
    
    entryList.append(newEvent)

    eventNameEntry.delete(0, tk.END)
    eventDescriptionTextbox.delete("1.0", tk.END)
    # let's not reset color
    # I can't reset date
    eventCompletedBoolVar.set(True)

    Messagebox.show_info("Success! Event created.", "Event created successfully", root)
        
eventFinishButton = Button(newEventFrame, text="Complete Event!", command=complete_new_event)
eventFinishButton.grid(row=6, column=0, columnspan=2, sticky="EW")

# notebook tab
notebookView = ttk.Treeview(noteFrame, selectmode=BROWSE)

def refresh_notebook_treeview():
    refresh_notebook_notes()
    notebookView.delete(*notebookView.get_children())
    for notebook in notebookList:
        notebook.iid = notebookView.insert("", END, text=notebook.title)
        for note in notebook.notes:
            note.iid = notebookView.insert(notebook.iid, END, text=note.title)

refresh_notebook_treeview()
notebookView.grid(row=1, column=0, sticky=NS)

noteScrolledtext = scrolled.ScrolledText(noteFrame, autohide=True)
noteScrolledtext.grid(row=1, column=1)

def set_scrolled_text(text : str):
    noteScrolledtext.delete("1.0", tk.END)
    noteScrolledtext.insert("1.0", text)

selectedObject : Notebook | Note = None
def load_note(event : tk.Event):
    global selectedObject
    # first save current note
    if isinstance(selectedObject, Note):
        selectedObject.body = noteScrolledtext.get("1.0", END)

    selectedIID = notebookView.selection()[0]
    selectedItem = notebookView.item(selectedIID)
    for notebook in notebookList:
        if notebook.iid != selectedIID:
            continue
        selectedObject = notebook
        set_scrolled_text("This is a notebook!")
        return
    for note in noteList:
        if note.iid != selectedIID:
            continue
        selectedObject = note
        set_scrolled_text(note.body)
        return
    selectedObject = None
    raise Warning(f"No notebook or note found with iid {selectedIID}!")

            
notebookView.bind("<<TreeviewSelect>>", load_note)


# run tkinter and handle closing
def on_close():
    message = Messagebox.yesno("Do you want to quit?", "Quit")
    if message == "Yes":
        save_lists()
        root.destroy()
root.protocol("WM_DELETE_WINDOW", on_close)
try:
    root.mainloop()
except Exception as e:
    save_lists()
    Messagebox.show_error("AgendaApp had an error! Your data was saved. Please report this! \nError Callback: {e}", "Crash")
except KeyboardInterrupt:
    root.destroy()
    save_lists()
    print("\nData saved successfully.")
finally:
    print("Quit successfully.")