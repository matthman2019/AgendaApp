import calendar
import datetime
import time
from random import randint
import sys
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

sys.path.append("Classes")
sys.path.append("Saves")

from Event import Event
from PlannerEntry import PlannerEntry
from ToDo import ToDo
from Notebook import Notebook
from Note import Note
from DataManager import save_object, read_entries, read_notebooks, read_notes
from EntryWidget import EntryWidget

# list setup
entryList = read_entries()
entryList.sort()
notebookList = read_notebooks()
noteList = read_notes()


root = ttk.Window(title="Notes App", themename="sandstone")
root.geometry("800x800")

notebook = ttk.Notebook(root, style="sandstone")
notebook.pack(fill=BOTH, expand=True)

upcomingFrame = ttk.Frame(notebook)
calendarFrame = ttk.Frame(notebook)
newEventFrame = ttk.Frame(notebook)
noteFrame = ttk.Frame(notebook)

notebook.add(upcomingFrame, text="Upcoming")
notebook.add(calendarFrame, text="Calendar")
notebook.add(newEventFrame, text="New Event")
notebook.add(noteFrame, text="Notebook")

# upcoming frame

upcomingFrameLabel = ttk.Label(upcomingFrame, text="Upcoming Events")
upcomingFrameLabel.pack()

# calendar frame
calendarFrameLabel = ttk.Label(calendarFrame, text="Calendar of Events")
calendarFrameLabel.pack()

# new event frame
newEventLabel = ttk.Label(newEventFrame, text="Here is will you will make new events.")
newEventLabel.pack()

# notebook frame
notebookLabel = ttk.Label(noteFrame, text="Here is where you will be able to take notes")
notebookLabel.pack()

currentlyOpenTab = "Upcoming Events"
def tab_changed(event : tk.Event):
    notebook : ttk.Notebook = event.widget
    selectedTabText = notebook.tab(notebook.select(), "text")
    print(selectedTabText)

    # show upcoming events
    if selectedTabText == "Upcoming":
        display_entry_list()

def display_entry_list():
    global entryList
    entryList.sort()
    for entry in entryList:
        eventFrame = EntryWidget(master=upcomingFrame, entry=entry)
        eventFrame.default_pack()

notebook.bind("<<NotebookTabChanged>>", tab_changed)


root.mainloop()