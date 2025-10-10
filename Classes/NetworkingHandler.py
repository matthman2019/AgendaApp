import socket
from ttkbootstrap.dialogs import Messagebox, MessageDialog

BUSY = "busy"
SUCCESS = "success"
FAILJSON = "failjson"
UNTITLED = "Untitled"

from DataManager import dict_from_json
from Note import Note
from Notebook import Notebook

addressList = []
def handle_connection(clientConnection : socket.socket, address, noteList : list, notebookList : list) -> Note:
    def closeConnectionWithCode(code : str):
        clientConnection.send(code.encode())
        clientConnection.close()
        del addressList[addressList.index(address)]

    def get_notebook_by_title(title:str) -> Notebook:
        for notebook in notebookList:
            if notebook.title == title:
                return notebook
        return None

    # check that we're not already receiving a message from this person
    if address in addressList:
        closeConnectionWithCode(BUSY)
        return
    
    addressList.append(address)
    
    # receive the JSON
    receivedText = ''
    timesReceived = 0
    sentDict : dict = None
    sentNote : Note = None
    while sentDict is None:
        receivedText += clientConnection.recv(1024).decode()
        sentDict = dict_from_json(receivedText)
        timesReceived += 1

        if timesReceived > 1000:
            closeConnectionWithCode(FAILJSON)
            return 
    # if the Note can't be created, send FAILJSON
    try:
        sentNote = Note.from_dict(sentDict)
    except KeyError:
        closeConnectionWithCode(FAILJSON)
        return

    confirmSave = Messagebox.yesno(f"You've received a note! \n  Title: {sentNote.title}\n  Body: {sentNote.body}\n  Notebook: {sentNote.notebook}\nWould you like to save this note?", "Note Received!")

    if confirmSave != "Yes":
        Messagebox.show_info("The message was not saved.", "Note Ignored")
    
    # figure out what to do with the note's notebook
    notebookForNote = get_notebook_by_title(sentNote.notebook)
    if notebookForNote is not None:
        noteList.append(sentNote)
        closeConnectionWithCode(SUCCESS)
        return sentNote
    
    newNotebookChoice = MessageDialog(
        message=f"This note was inside a notebook named {sentNote.notebook}, which doesn't currently exist on your computer." \
        "\nWould you like to make this notebook for the note? If not, this note will be put in the untitled notebook.",
        title="New Notebook?",
        buttons=["New Notebook", "Untitled Notebook"]
        )
    
    if newNotebookChoice == "Untitled Notebook":
        sentNote.notebook = UNTITLED
        noteList.append(sentNote)
        closeConnectionWithCode(SUCCESS)
        return sentNote
    else:
        newNotebookForNote = Notebook(sentNote.notebook)
        notebookList.append(newNotebookForNote)
        noteList.append(sentNote)
        closeConnectionWithCode(SUCCESS)
        return sentNote
    

