# Class API

## Event

Event is a class that stores an event in a planner. It just is - it can't be checked off.
It doesn't repeat, it's just a one-time thing.
Do note that you can use greater than, less than, etc. on Events. They compare their occurance in time.
So if event2 happens after event1, event2 > event1.

Attributes
- name : str = the name of the entry.
- description : str = a longer description of the entry.
- occurance : datetime.datetime = a datetime object that represents when this entry is
- color : str = a hexdecimal code for the color of this entry. This is mostly for stylistic purposes.

"occurance" is a weird name, but I can't use date or time for the attribute since that conflicts with the datetime module.

Quick note - I used to call the Event class "PlannerEntry."
If you see something in comments about an "entry" I'm probably talking about an Event.

## RepeatingEvent(Event)

Event inherits from Event since it is an event.
It can repeat. Booyah.

- repeats : bool = whether the event repeats or not
- repeatTime : timedelta = the time between repeats (i.e. one week, one month, one year, etc)

## ToDo(Event)

ToDo is a class that inherits Event. It is an event, but unlike an event, it CAN be checked off - like a todo in a schedule!
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
- notebook : str | None = the ID of the notebook that this note belongs to. Can be None.

- iid : str = This is used by tkinter. I use this to save the IID of the tkinter widget that represents this note.

## Notebook

A collection of Notes.

Attributes
- title : str = The name of the Notebook. Must be unique.
- notes : list (NOT SAVED) = this list is the notes that are inside the notebook. It is generated at runtime for ease in programming.

- iid : str = This is like Note's attribute iid. It's used to identify the widget that represents this notebook.


# Network API

Since we'll be sending notes over the network, we'll need some protocol.

I'll refer to the person sending the note as the sender and the person receiving the note as the receiver.
The receiver hosts the TCP socket server, the sender connects and sends the JSON for a note.
The receiver then responds back to the sender and closes the connection. (This step exists to let the sender know if their note was sent successfully)

## Sender Messages

The sender just needs to send the JSON for the thing it wants to send. Nothing complicated.
Use the Note.to_json() method for ease.

## Receiving Responses

### busy

The receiver is currently busy processing something previously sent from the sender's IP address, so it dropped the note sent.
(This is to prevent people from spamming notes and overwhelming users.)

### success

Successfully sent!

### failjson

Bad json was sent, so the send failed.