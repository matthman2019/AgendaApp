# A note is, well, a note. Like a page in a notebook, it has a title and a body.

from datetime import datetime
from dataclasses import dataclass

@dataclass
class Note:
    title : str = "Untitled Note"
    lastedit : datetime = datetime.today()
    body : str = ""
    notebook : int | None = None