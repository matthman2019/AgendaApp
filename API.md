# API

## PlannerEntry

PlannerEntry is a class that stores an entry in a planner. It just is - it can't be checked off.
It doesn't repeat, it's just a one-time thing.
Do note that you can use greater than, less than, etc. on PlannerEntrys. They compare their occurance in time.
So if event2 happens after event1, event2 > event1.

Attributes
- name : str = the name of the entry.
- description : str = a longer description of the entry.
- occurance : datetime.datetime = a datetime object that represents when this entry is
- color : str = a hexdecimal code for the color of this entry. This is mostly for stylistic purposes.

"occurance" is a weird name, but I can't use date or time for the attribute since that conflicts with the datetime module.

## Event(PlannerEntry)

Event inherits from PlannerEntry since it is an entry

## ToDo(PlannerEntry)

ToDo is a class that inherits PlannerEntry. It is an entry, but unlike an entry, it CAN be checked off - like a todo in a schedule!
It does not repeat though.

Attributes
- completed : bool = whether the event has been completed or not

Inherited Attributes
- name : str = the name of the event.
- description : str = a longer description of the event.
- occurance : datetime.datetime = a datetime object that represents when this event is
- color : str = a hexdecimal code for the color of this event. This is mostly for stylistic purposes.

## Note

A Note is, well, a note. It just holds text.

Attributes
- title : str = the title of the note
- lastEdit : datetime.datetime = the last time the note was saved
- body : str = the contents of the note
- notebook : int | None = the ID of the notebook that this note belongs to. Can be None.

## Notebook

A collection of Notes.

Attributes
- title : str = The name of the Notebook
- id : int = the ID of the notebook. Must be unique.
- notes : list (NOT SAVED) = this list is the notes that are inside the notebook. It is generated at runtime for ease in programming.
