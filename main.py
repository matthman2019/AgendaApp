import calendar
import datetime
import time
from random import randint
import sys
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import dialogs
from ttkbootstrap.constants import *

sys.path.append("Classes")
sys.path.append("Saves")

from Event import Event
from PlannerEntry import PlannerEntry
from ToDo import ToDo
from Notebook import Notebook
from Note import Note
from DataManager import save_objects, read_entries, read_notebooks, read_notes
from EntryWidget import EntryWidget

# list setup
entryList = read_entries()
entryList.sort()
notebookList = read_notebooks()
noteList = read_notes()

def save_lists():
    save_objects(entryList); save_objects(notebookList); save_objects(noteList)


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

# handle notebook tab changes
currentlyOpenTab = "Upcoming"
def tab_changed(event : tk.Event):
    notebook : ttk.Notebook = event.widget
    selectedTabText = notebook.tab(notebook.select(), "text")
    print(selectedTabText)

    # show upcoming events
    if selectedTabText == "Upcoming":
        display_entry_list()
notebook.bind("<<NotebookTabChanged>>", tab_changed)

# display entries in upcomingFrame
def display_entry_list():
    global entryList
    entryList.sort()
    for entry in entryList:
        eventFrame = EntryWidget(master=upcomingFrame, entry=entry)
        eventFrame.default_pack()

# calendar tab (eventually)

# new event tab




# run tkinter and handle closing
def on_close():
    message = dialogs.Messagebox.yesno("Do you want to quit?", "Quit")
    if message == "Yes":
        save_lists()
        root.destroy()
root.protocol("WM_DELETE_WINDOW", on_close)
try:
    root.mainloop()
except Exception as e:
    save_lists()
    dialogs.Messagebox.show_error("AgendaApp had an error! Your data was saved. Please report this! \nError Callback: {e}", "Crash")
except KeyboardInterrupt:
    root.destroy()
    save_lists()
    print("\nData saved successfully.")
finally:
    print("Quit successfully.")