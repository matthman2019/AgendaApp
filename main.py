import datetime
from random import randint
import sys
import threading
import socket
import ipaddress
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
from DataManager import save_objects, read_events, read_notebooks, read_notes, delete_object, read_aloud_bad_files, dict_from_json
from EntryWidget import EntryWidget
from NetworkingHandler import handle_connection

# list setup
eventList, badEvents = read_events()
eventList.sort()
notebookList, badNotebooks = read_notebooks()
noteList, badNotes = read_notes()
badJsonPaths = badEvents + badNotebooks + badNotes

localhostMode = True
PORT = 25313
IP = "127.0.0.1" if localhostMode else None

UNTITLED = "Untitled"
BUSY = "busy"
# SUCCESS is already defined in ttkbootstrap
FAILJSON = "failjson"

# runs through notebookList and finds notebook with a title of title
def get_notebook_by_title(title:str) -> Notebook:
    for notebook in notebookList:
        if notebook.title == title:
            return notebook
    return None

# make untitled notebook if necessary
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
    
# saves eventList, notebookList, and noteList to the hard drive
def save_lists():
    global eventList, notebookList, noteList
    save_objects(eventList); save_objects(notebookList); save_objects(noteList)

# tkinter setup
root = ttk.Window(title="Notes App", themename="sandstone")
root.geometry("800x800")
rootNotebook = ttk.Notebook(root, style="sandstone")
rootNotebook.pack(fill=BOTH, expand=True)

# rootNotebook frame setup
upcomingFrame = Frame(rootNotebook)
newEventFrame = Frame(rootNotebook)
noteFrame = Frame(rootNotebook)
# shareFrame = Frame(rootNotebook)
rootNotebook.add(upcomingFrame, text="Upcoming")
rootNotebook.add(newEventFrame, text="New Event")
rootNotebook.add(noteFrame, text="Notebook")
# rootNotebook.add(shareFrame, text="Share Note")


# handle notebook tab changes
currentlyOpenTab = "Upcoming"
def tab_changed(event : tk.Event):
    global currentlyOpenTab
    if currentlyOpenTab == "Notebook":
        save_note()
    notebook : ttk.Notebook = event.widget
    currentlyOpenTab = notebook.tab(notebook.select(), "text")

    # show upcoming events
    if currentlyOpenTab == "Upcoming":
        display_event_list()
rootNotebook.bind("<<NotebookTabChanged>>", tab_changed)

# upcoming frame

upcomingFrameLabel = Label(upcomingFrame, text="Upcoming Events")
upcomingFrameLabel.pack()
upcomingEventsFrame = scrolled.ScrolledFrame(upcomingFrame, autohide=True)
upcomingEventsFrame.pack(expand=True, fill=BOTH)

# display entries in upcomingEventsFrame
def display_event_list():
    global eventList

    # while this is defined in EntryWidget class, I'm going to override this method to make deleting work.
    def remove_from_entry_list(entry : EntryWidget):
        del eventList[eventList.index(entry.entry)]
        delete_object(entry.entry)
        display_event_list()
    
    for widget in upcomingEventsFrame.winfo_children():
        widget.destroy()
    eventList.sort()
    for entry in eventList:
        eventFrame = EntryWidget(master=upcomingEventsFrame, entry=entry)
        eventFrame.default_pack()
        eventFrame.onDeleteCallback = remove_from_entry_list



# calendar tab (eventually)

# calendarFrameLabel = Label(calendarFrame, text="Calendar of Events")
# calendarFrameLabel.pack()



# new event tab
newEventLabel = Label(newEventFrame, text="New Event")
newEventLabel.grid(row=0, column=0, columnspan=2)

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

userSelectedDate = datetime.datetime.today()
# row 3: occurance
eventOccuranceLabel = Label(newEventFrame, text="Occurance")
eventOccuranceLabel.grid(row=3, column=0)
# eventDateChooser = widgets.DateEntry(newEventFrame)
# eventDateChooser.grid(row=3, column=1)
eventDateButton = Button(newEventFrame, text="Click on me to choose a date", command=lambda: dialogs.DatePickerDialog(root))
eventDateButton.grid(row=3, column=1)

timesClicked = 0
userSelectedDate = datetime.datetime.today()
def ask_date_with_dialog():
    global userSelectedDate, timesClicked
    if timesClicked == 0:
        # this gives a warning about the dateEntry. I think it only shows up on chromebooks with virtual linux.
        '''
        Messagebox.show_info("The window that should pop up to ask you the date generally doesn't work first try. "\
                             "It'serverSocket a very annoying bug, completely out of my control, and I can't fix it. "\
                             "If the date picking window does not show up on your first attempt, try clicking the button again. "\
                             "If that doesn't work after a few tries, restart the program. If none of that worked, you're out of luck. Sorry!")
        '''
        pass
    date = dialogs.DatePickerDialog(root)
    userSelectedDate = datetime.datetime.combine(date.date_selected, datetime.time(23, 59, 59, 0))
    timesClicked += 1
eventDateButton.config(command=ask_date_with_dialog)

# row 4: color
newEventColor = 'FF0000'
def chooseNewColor():
    global newEventColor, eventColorButton
    cd = ColorChooserDialog(root, "Choose a color for the new event")
    cd.show()
    newEventColor = cd.result.hex
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
    global userSelectedDate
    # name
    eventName = eventNameEntry.get()
    if eventName.strip(" ") == "":
        Messagebox.show_error("You need to give your event a name!", "Could not make event", root, alert=False)
        return
    # make eventName unique (add a digit at the end if necessary)
    originalEventName = eventName
    eventNameUnique = False
    numberAddingOn = 1
    while not eventNameUnique:
        eventNameUnique = True
        for event in eventList:
            if event.name == eventName:
                eventNameUnique = False
                numberAddingOn += 1
                eventName = originalEventName + str(numberAddingOn)
                break
        
        
    # description (can be none)
    eventDescription = eventDescriptionTextbox.get("1.0", "end-1c")
    # occurance
    eventOccurance = userSelectedDate
    # color
    eventColor = newEventColor
    # if the event can be completed, make a ToDo
    if eventCompletedBoolVar.get():
        newEvent = ToDo(eventName, eventDescription, eventOccurance, eventColor, False)
    
    # otherwise, just make an Event
    else:
        newEvent = Event(eventName, eventDescription, eventOccurance, eventColor)
    
    eventList.append(newEvent)

    eventNameEntry.delete(0, tk.END)
    eventDescriptionTextbox.delete("1.0", tk.END)
    # let'serverSocket not reset color
    # I can't reset date
    eventCompletedBoolVar.set(True)

    Messagebox.show_info("Success! Event created.", "Event created successfully", root)
        
eventFinishButton = Button(newEventFrame, text="Complete Event!", command=complete_new_event)
eventFinishButton.grid(row=6, column=0, columnspan=2, sticky="EW")



# notebook tab

notebookLabel = Label(noteFrame, text="Notes")
notebookLabel.grid(row=0, column=0, columnspan=1)

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

noteScrolledtext = scrolled.ScrolledText(noteFrame, autohide=True, width=50)
noteScrolledtext.grid(row=1, column=1)

def set_scrolled_text(text : str):
    noteScrolledtext.delete("1.0", tk.END)
    noteScrolledtext.insert("1.0", text)

selectedObject : Notebook | Note = None

def save_note():
    if currentlyOpenTab != "Notebook":
        return
    if isinstance(selectedObject, Note):
        selectedObject.body = noteScrolledtext.get("1.0", END)
        selectedObject.lastedit = datetime.datetime.today()

def load_note(event : tk.Event):
    global selectedObject
    # first save current note
    save_note()
    # set selectedObject (the object of the item currently selected, which is a Note or Notebook)
    try:
        selectedIID = notebookView.selection()[0]
    except IndexError:
        set_scrolled_text("")
        return
    for notebook in notebookList:
        if notebook.iid != selectedIID:
            continue
        selectedObject = notebook
        set_scrolled_text("This is a notebook!\nTry selecting a note. " \
        "If you can't see any notes, click the plus sign to the left of this notebook'serverSocket name." \
        "\nModifying this text will not break anything.")
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

# new note and notebook creation
newNotebookButton = Button(noteFrame, text="Make a New Notebook")
newNotebookButton.grid(row=2, column=0)
newNoteButton = Button(noteFrame, text="Make a New Note")
newNoteButton.grid(row=2, column=1)
deleteSelectedButton = Button(noteFrame, text="Delete Selected Item", style=DANGER)
deleteSelectedButton.grid(row=3, column=0)

# functionality for the new notebook button
def make_new_notebook():
    newNotebookRoot = ttk.Toplevel(title="New Notebook")
    
    notebookTitleLabel = Label(newNotebookRoot, text="What will the title of this notebook be?")
    notebookTitleLabel.grid(row=0, column=0, columnspan=2)
    notebookTitleEntry = ttk.Entry(newNotebookRoot)
    notebookTitleEntry.grid(row=1, column=0, columnspan=2)
    notebookTitleCreateButton = Button(newNotebookRoot, text="Create", style=SUCCESS)
    notebookTitleCreateButton.grid(row=2, column=0)
    notebookTitleCancelButton = Button(newNotebookRoot, text="Cancel", style=DANGER)
    notebookTitleCancelButton.grid(row=2, column=1)

    def fail_creation():
        newNotebookRoot.destroy()
    notebookTitleCancelButton.config(command=fail_creation)
    newNotebookRoot.protocol("WM_DELETE_WINDOW", fail_creation)

    def successful_creation():
        global notebookList
        enteredText = notebookTitleEntry.get()
        # check that the name exists and is not only spaces
        if enteredText.strip(" ") == "":
            Messagebox.show_error("You must enter a name for the notebook!", "No Notebook Name", newNotebookRoot)
            return
        # check for name repeats
        for notebook in notebookList:
            if notebook.title == enteredText:
                Messagebox.show_info("That name is already taken! No new notebook made.", "Used Notebook Name", newNotebookRoot)
                return
        # make new notebook
        newNotebook = Notebook(enteredText)
        notebookList.append(newNotebook)
        refresh_notebook_treeview()
        newNotebookRoot.destroy()
    notebookTitleCreateButton.config(command=successful_creation)

    newNotebookRoot.mainloop()
newNotebookButton.config(command=make_new_notebook)

# functionality for the new note button
def make_new_note():
    global selectedObject
    if not isinstance(selectedObject, Notebook):
        Messagebox.show_info("You need to select a notebook in the " \
                             "notebook tree that this note will be inside of!", "No notebook selected", root)
        return
    
    targetNotebook = selectedObject
    
    newNoteRoot = ttk.Toplevel(title="New Note")
    
    noteTitleLabel = Label(newNoteRoot, text="What will the title of this note be?")
    noteTitleLabel.grid(row=0, column=0, columnspan=2)
    noteTitleEntry = ttk.Entry(newNoteRoot)
    noteTitleEntry.grid(row=1, column=0, columnspan=2)
    targetNotebookLabel = Label(newNoteRoot, text=f'This note will be put in the notebook titled "{targetNotebook.title}."')
    targetNotebookLabel.grid(row=2, column=0, columnspan=2)
    noteTitleCreateButton = Button(newNoteRoot, text="Create", style=SUCCESS)
    noteTitleCreateButton.grid(row=3, column=0)
    noteTitleCancelButton = Button(newNoteRoot, text="Cancel", style=DANGER)
    noteTitleCancelButton.grid(row=3, column=1)

    def fail_creation():
        newNoteRoot.destroy()
    noteTitleCancelButton.config(command=fail_creation)
    newNoteRoot.protocol("WM_DELETE_WINDOW", fail_creation)

    def successful_creation():
        global notebookList
        enteredText = noteTitleEntry.get()
        if enteredText.strip(" ") == "":
            Messagebox.show_error("You must enter a name for the note!", "No Note Name", newNoteRoot)
            return
        for note in noteList:
            if note.title == enteredText:
                Messagebox.show_info("That name is already taken! No new note made.", "Used Note Name", newNoteRoot)
                return
        newNote = Note(enteredText, notebook=targetNotebook.title)
        noteList.append(newNote)
        refresh_notebook_treeview()
        newNoteRoot.destroy()
    noteTitleCreateButton.config(command=successful_creation)

    newNoteRoot.mainloop()

newNoteButton.config(command=make_new_note)

# functionality for delete selected item button
def check_item_delete():
    global selectedObject
    if isinstance(selectedObject, Note):
        confirmDelete = Messagebox.yesnocancel(f'Are you sure you want to delete the note titled {selectedObject.title}? This cannot be undone.', 
                               "Confirm Delete", True, rootNotebook)
        if confirmDelete == "Yes":
            del noteList[noteList.index(selectedObject)]
            refresh_notebook_treeview()
            Messagebox.show_info("Note deleted successfully.", "Success", root)
        else:
            Messagebox.show_info("The note was not deleted.", "Not Deleted", root)
    elif isinstance(selectedObject, Notebook):
        if selectedObject.title == UNTITLED:
            Messagebox.show_info("You can't delete the untitled notebook.", "You can't delete that", root)
            return
        confirmDelete = Messagebox.yesnocancel(f'Are you sure you want to delete the notebook titled {selectedObject.title}? ' \
                                                'This cannot be undone. All notes inside the notebook will be put into the Untitled Notebook.', 
                               "Confirm Delete", True, rootNotebook)
        if confirmDelete == "Yes":
            del notebookList[notebookList.index(selectedObject)]
            refresh_notebook_treeview()
            Messagebox.show_info("Notebook deleted successfully.", "Success", root)
        else:
            Messagebox.show_info("The notebook was not deleted.", "Not Deleted", root)
    else:
        Messagebox.show_info("Nothing was selected, so nothing was deleted.", "Not Deleted", root)
deleteSelectedButton.config(command=check_item_delete)

# this was originally going to be its own tab but I decided to merge it with the notebook tab

recieveButton = Button(noteFrame, text="Receive a Note")
recieveButton.grid(row=4, column=0)
sendButton = Button(noteFrame, text="Send a Note")
sendButton.grid(row=4, column=1)

def get_private_IP():
    global IP, localhostMode
    if IP is not None:
        return
    if localhostMode:
        IP = "127.0.0.1"
        return
    

    try:
        IPSocket = socket.create_connection(("1.1.1.1", 80), 5)
        IP = IPSocket.getsockname()[0]
    except TimeoutError:
        pass
    except OSError:
        pass


receivingNotes = False
# receive button functionality
def receive_notes_button_function():
    global IP, receivingNotes

    receiveRoot = ttk.Toplevel("Receive Notes")
    receiveRoot.geometry("750x400")

    progressLabel = Label(receiveRoot, text="Setting things up...")
    progressLabel.grid(row=0, column=0)

    serverSocket = None
    incomingNoteList : list[Note] = []

    def start_receiving_notes():
        global IP, PORT, receivingNotes
        nonlocal progressLabel, serverSocket, incomingNoteList
        receivingNotes = True
        
        try:
            serverSocket = socket.create_server((IP, PORT))
            serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except OSError as e:
            progressLabel.config(text="We weren't able to set up note receiving.\nTry waiting a few minutes, and try again.\n" \
            "If that doesn't work, you might not be able to share notes from this computer." \
            f"Error message: \n{e}")
            return
        
        progressLabel.config(text="Successfully set up!" \
            f"\nTell anyone who wants to send you notes this IP: {IP}\n" \
            "(This is your private IP. Only people connected to the same network as you \nwill be able to access your computer through it.)" \
            "\nWe'll create new windows as people share notes with you...")

        def socketHandler():
            nonlocal incomingNoteList

            while receivingNotes:
                clientConnection, address = serverSocket.accept()
                note = handle_connection(clientConnection, address, noteList, notebookList)
                if note:
                    incomingNoteList.append(note)
        
            # once we're done receiving notes, close the socket
            serverSocket.close()
        
        socketHandlerThread = threading.Thread(target=socketHandler)
        socketHandlerThread.start()
    
    # this stores the ID to cancel the .after() call
    check_incoming_notes_id = None
    # this function checks notes every second. It runs over and over
    def check_incoming_notes():
        nonlocal incomingNoteList, check_incoming_notes_id

        # if no notes, reset for a new check and return
        if not incomingNoteList:
            check_incoming_notes_id = receiveRoot.after(1000, check_incoming_notes)
            return
        
        for sentNote in incomingNoteList:
            confirmSave = Messagebox.yesno(f"You've received a note! \n  Title: {sentNote.title}\n  Body: {sentNote.body}\n  Notebook: {sentNote.notebook}\nWould you like to save this note?", "Note Received!")

            if confirmSave != "Yes":
                Messagebox.show_info("The message was not saved.", "Note Ignored")
            
            # figure out what to do with the note's notebook
            notebookForNote = get_notebook_by_title(sentNote.notebook)
            if notebookForNote is not None:
                noteList.append(sentNote)
                continue
            
            newNotebookChoice = dialogs.MessageDialog(
                message=f"This note was inside a notebook named {sentNote.notebook}, which doesn't currently exist on your computer." \
                "\nWould you like to make this notebook for the note? If not, this note will be put in the untitled notebook.",
                title="New Notebook?",
                buttons=["New Notebook", "Untitled Notebook"]
                )
            newNotebookChoice.show()
            
            if newNotebookChoice._result == "Untitled Notebook":
                sentNote.notebook = UNTITLED
                noteList.append(sentNote)
                continue
            else:
                newNotebookForNote = Notebook(sentNote.notebook)
                notebookList.append(newNotebookForNote)
                noteList.append(sentNote)
                continue
        
        incomingNoteList = []
        refresh_notebook_treeview()
        check_incoming_notes_id = receiveRoot.after(1000, check_incoming_notes)
    
    check_incoming_notes_id = receiveRoot.after(1000, check_incoming_notes)

    # see whether we can start receiving or not (whether private IP was obtained or not)
    def report_IP_status():
        global IP
        if IP is None:
            progressLabel.config(text="We weren't able to set up note receiving.\nAre you sure that you're connected to the internet?")
        else:
            start_receiving_notes()
            
    
    # see if we need to find private IP. otherwise, show that we're successfully set up already.
    if IP is None:
        receiveRoot.after(10, get_private_IP)
        receiveRoot.after(5700, report_IP_status)
    else:
        receiveRoot.after(10, report_IP_status)
    
    # closing behavior
    # notice that the server has to use .accept() above. That's a blocking function!
    # to break it, we're going to set receivingNotes to false and connect locally
    def on_close():
        global receivingNotes

        receivingNotes = False
        try:
            breakAcceptSocket = socket.create_connection((IP, PORT))
            breakAcceptSocket.close()
        except OSError as e:
            print(e)
        receiveRoot.after_cancel(check_incoming_notes_id)
        receiveRoot.destroy()
        
    receiveRoot.protocol("WM_DELETE_WINDOW", on_close)
    receiveRoot.mainloop()

recieveButton.config(command=receive_notes_button_function)

# send button functionality
def send_notes_button_functionality():
    global selectedObject
    if not isinstance(selectedObject, Note):
        Messagebox.show_info("Please select a note in the notebook tree to send!", "Please select a note", root)
        return
    
    sendRoot = ttk.Toplevel("Send Notes")

    sendIPLabel = Label(sendRoot, text="Send IP")
    sendIPLabel.grid(row=0, column=0)
    sendIPEntry = ttk.Entry(sendRoot)
    sendIPEntry.grid(row=0, column=1)
    sendNoteLabel = Label(sendRoot, text=f"You'll be sending your note named \"{selectedObject.title}\" to the person with this private IP.")
    sendNoteLabel.grid(row=1, column=0, columnspan=2, sticky="EW")
    sendButton = Button(sendRoot, text="Send")
    sendButton.grid(row=2, column=0)
    cancelButton = Button(sendRoot, text="Cancel", style=DANGER, command=lambda: sendRoot.destroy())
    cancelButton.grid(row=2, column=1)

    tryingToSend = False

    def send_button_functionality():
        # disallow spamming the "send" button
        nonlocal tryingToSend
        if tryingToSend:
            return
        
        # check that the IP is valid
        IPEntered = sendIPEntry.get()
        try:
            ipaddress.ip_address(IPEntered)
        except ValueError:
            Messagebox.show_error("The IP entered is unusable! Are you sure you typed it in correctly?", "Unusable IP", root)
            return
        
        if not isinstance(selectedObject, Note):
            Messagebox.show_error("Make sure you're selecting a note in the notebook tree and please try again!", "Selected item is not a note", root)
        
        save_note()
        try:
            tryingToSend = True
            sendNoteLabel.config(text="Trying to send your note...")
            sendRoot.destroy()
            s = socket.create_connection((IPEntered, PORT))
            s.send(selectedObject.to_json().encode())
            receiveCode = s.recv(1024).decode()
            
            if receiveCode == SUCCESS:
                Messagebox.show_info("The note was sent successfully! Woohoo!", "Success!", root)
            elif receiveCode == BUSY:
                Messagebox.show_info("The person receiving your note is already processing another note that you sent them! Wait a few seconds before trying to send another note.", "Receiver Busy", root)
            elif receiveCode == FAILJSON:
                Messagebox.show_error("The message failed to send: something was wrong with the message itself.\n" \
                "You did nothing wrong, but could you please report this to the developer?\n" \
                f"Please include this in your error report: {selectedObject.to_json()}", "JSON Error", root)
            else:
                Messagebox.show_info("Your note sent successfully, but the receiver returned a code that we couldn't understand. \n" \
                f"The note definitely sent to the receiver, but there's no telling if they were able to save it or not. The code was: {receiveCode}", "Unknown Response", root)

        except TimeoutError as e:
            Messagebox.show_error("Unable to send note: the connection timed out. \nAre you sure that you typed the IP in correctly and that the computer you're sending to is in receiving mode?\n" \
            f"Error code: \nTimeoutError: {e}", "Timeout Error", root)
        except OSError as e:
            Messagebox.show_error("Unable to send note: the connection didn't work. \nAre you sure that you typed the IP in correctly and that the computer you're sending to is in receiving mode?\n" \
            f"Error code: \nOSError: {e}", "OSError", root)
        except Exception as e:
            Messagebox.show_error("Something went wrong, but we're not sure what. Please report this to the developer!" \
            f"Error code: \n{e}", "Exception", root)
        finally:
            tryingToSend = False
    sendButton.config(command=send_button_functionality)


        



sendButton.config(command=send_notes_button_functionality)
# run tkinter and handle closing
def on_close():
    message = Messagebox.yesno("Do you want to quit?", "Quit")
    if message == "Yes":
        save_note()
        save_lists()
        root.destroy()
root.protocol("WM_DELETE_WINDOW", on_close)
try:
    # first, set up showing bad files (just in case we need to)
    root.after(100, lambda: read_aloud_bad_files(badJsonPaths))
    # then run!
    root.mainloop()
except Exception as e:
    save_note()
    save_lists()
    Messagebox.show_error("AgendaApp had an error! Your data was saved. Please report this! \nError Callback: {e}", "Crash")
except KeyboardInterrupt:
    root.destroy()
    save_note()
    save_lists()
    print("\nData saved successfully.")
finally:
    print("Quit successfully.")