# this is a class to make displaying Entries easier.

import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import Frame
from ttkbootstrap.dialogs import Messagebox
from typing import Callable
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

        self.frame = ttk.Frame(master, padding=4)

        self.myStyle = ttk.Style()
        self.styleName = f"{self.entry.name}.TFrame"
        self.myStyle.configure(self.styleName, foreground=self.entry.color, background=self.entry.color)
        self.frame.config(style=self.styleName)

        self.frame.columnconfigure(0, minsize=10)
        self.frame.columnconfigure(2, minsize=10)
        self.frame.columnconfigure(6, weight=1)

        self.entryLabel = ttk.Label(self.frame, text=self.entry.name, background="white", padding=4)
        self.entryLabel.grid(row=0, column=1)

        # checkbox for ToDos
        self.checkbox = None
        self.completedVar = None
        self.onDeleteCallback : Callable[[EntryWidget]] = None
        if isinstance(self.entry, ToDo):
            self.completedVar = tk.BooleanVar(value=self.entry.completed)

            def on_checkbox_toggle():
                self.entry.completed = self.completedVar.get()

            self.checkbox = ttk.Checkbutton(self.frame, text="Completed", variable=self.completedVar, command=on_checkbox_toggle)
            self.checkbox.grid(row=0, column=3)

        # delete button
        def check_delete():
            if Messagebox.yesno("Are you sure that you want to delete this entry?", "Delete Entry") == "Yes":
                self.onDeleteCallback(self)
        self.deleteButton = ttk.Button(self.frame, text="🗑️", style="danger", command=check_delete)
        self.deleteButton.grid(row=0, column=6, sticky="e")
        
    
    def default_pack(self):
        self.frame.pack(fill="x", expand=False, anchor="n", padx=5, pady=5)