import calendar
import datetime
import time
from random import randint
import sys

sys.path.append("Classes")

import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *


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


root.mainloop()