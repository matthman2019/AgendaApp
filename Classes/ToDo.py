# ToDo is like a PlannerEntry (see PlannerEntry.py), but it has a new property: completed!
# this boolean signifies if it has been completed or not.

from PlannerEntry import PlannerEntry
from datetime import datetime, timedelta
from calendar import isleap

class ToDo(PlannerEntry):
    def __init__(self, 
                name : str = "Untitled Entry", 
                description : str = "This entry has no description yet!",
                occurance : datetime = datetime.today() + timedelta(1.0),
                color : str = "#FF0000",
                completed : bool = False):
        
        super().__init__(name, description, occurance, color)
        self.completed = completed

if __name__ == "__main__":
    pass