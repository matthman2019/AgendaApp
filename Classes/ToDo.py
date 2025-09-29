# ToDo is like a PlannerEntry (see PlannerEntry.py), but it has a new property: completed!
# this boolean signifies if it has been completed or not.

from Event import Event
from datetime import datetime, timedelta
from calendar import isleap

class ToDo(Event):
    def __init__(self, 
                name : str = "Untitled Entry", 
                description : str = "This entry has no description yet!",
                occurance : datetime = datetime.today() + timedelta(1.0),
                color : str = "#FF0000",
                completed : bool = False):
        
        super().__init__(name, description, occurance, color)
        self.completed = completed
    
    @classmethod
    def from_dict(cls, dictionary:dict) -> "ToDo":
        newEntry = ToDo()
        newEntry.name = dictionary["name"]
        newEntry.description = dictionary["description"]
        newEntry.occurance = datetime.fromisoformat(dictionary["occurance"])
        newEntry.color = dictionary["color"]
        newEntry.completed = dictionary["completed"]
        return newEntry

if __name__ == "__main__":
    todo = ToDo()
    print(todo.completed)
    print(type(ToDo.from_dict(todo.to_dict()).completed))