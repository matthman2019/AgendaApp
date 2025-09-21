import calendar
import datetime
import time
from random import randint

import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *


root = ttk.Window(title="Notes App", themename="sandstone")
root.geometry("800x800")

notebook = ttk.Notebook()
notebook.pack(fill=BOTH, expand=True)

upcomingFrame = ttk.Frame(notebook)
calendarFrame = ttk.Frame(notebook)
newEventFrame = ttk.Frame(notebook)

notebook.add(upcomingFrame, text="Upcoming")
notebook.add(calendarFrame, text="Calendar")
notebook.add(newEventFrame, text="New Event")

# upcoming frame

upcomingFrameLabel = ttk.Label(upcomingFrame, text="Upcoming Events")
upcomingFrameLabel.pack()

# calendar frame
calendarFrameLabel = ttk.Label(calendarFrame, text="Calendar of Events")
calendarFrameLabel.pack()

# new event frame
newEventLabel = ttk.Label(newEventFrame, text="Here is will you will make new events.")
newEventLabel.pack()


root.mainloop()