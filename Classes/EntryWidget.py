# this is a class to make displaying Entries easier.

import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import Frame
import sys
from pathlib import Path

from Event import Event
from ToDo import ToDo
from PlannerEntry import PlannerEntry

class EntryWidget:
    def __init__(self, master = None, entry : Event | ToDo | PlannerEntry = None):
        if entry is None:
            entry = PlannerEntry(color="#FF0000")
        self.entry = entry

        self.frame = ttk.Frame(master, height=50)

        myStyle = ttk.Style()
        self.styleName = f"{self.entry.name}.TFrame"
        myStyle.configure(self.styleName, foreground="red")
        self.frame.config(style=self.styleName)
    
    def default_pack(self):
        self.frame.pack(fill="x", expand=True, anchor="n", padx=5, pady=5)