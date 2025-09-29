import calendar
import datetime
import time
from random import randint
import sys
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import Label, Frame
from ttkbootstrap import dialogs, scrolled
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

def save_lists():
    global entryList, notebookLabel, noteList
    save_objects(entryList); save_objects(notebookList); save_objects(noteList)

root = ttk.Window(title="Notes App", themename="sandstone")
root.geometry("800x800")
notebook = ttk.Notebook(root, style="sandstone")
notebook.pack(fill=BOTH, expand=True)

upcomingFrame = Frame(notebook)
calendarFrame = Frame(notebook)
newEventFrame = Frame(notebook)
noteFrame = Frame(notebook)
notebook.add(upcomingFrame, text="Upcoming")
notebook.add(calendarFrame, text="Calendar")
notebook.add(newEventFrame, text="New Event")
notebook.add(noteFrame, text="Notebook")

# upcoming frame
upcomingFrameLabel = Label(upcomingFrame, text="Upcoming Events")
upcomingFrameLabel.pack()
upcomingEventsFrame = scrolled.ScrolledFrame(upcomingFrame)
upcomingEventsFrame.pack(expand=True, fill=BOTH)
# calendar frame
calendarFrameLabel = Label(calendarFrame, text="Calendar of Events")
calendarFrameLabel.pack()
# new event frame
newEventLabel = Label(newEventFrame, text="New Event")
newEventLabel.pack()
# notebook frame
notebookLabel = Label(noteFrame, text="Here is where you will be able to take notes")
notebookLabel.pack()

# handle notebook tab changes
currentlyOpenTab = "Upcoming"
def tab_changed(event : tk.Event):
    notebook : ttk.Notebook = event.widget
    selectedTabText = notebook.tab(notebook.select(), "text")

    # show upcoming events
    if selectedTabText == "Upcoming":
        display_entry_list()   
notebook.bind("<<NotebookTabChanged>>", tab_changed)

# display entries in upcomingEventsFrame
def display_entry_list():
    global entryList

    # while this is defined in EntryWidget class, I'm going to override this method to make deleting work.
    def remove_from_entry_list(entry : EntryWidget):
        del entryList[entryList.index(entry.entry)]
        delete_object(entry.entry)
        display_entry_list()
    
    for widget in upcomingEventsFrame.winfo_children():
        widget.destroy()
    entryList.sort()
    for entry in entryList:
        eventFrame = EntryWidget(master=upcomingEventsFrame, entry=entry)
        eventFrame.default_pack()
        eventFrame.onDeleteCallback = remove_from_entry_list

# calendar tab (eventually)

# new event tab
nameLabel = Label(newEventFrame, text="Event Name")



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