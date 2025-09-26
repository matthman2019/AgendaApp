from datetime import datetime, timedelta
from dataclasses import dataclass
import json

zeroTime = timedelta(0)

# Stores an entry.
# Note that __ge__, __gt__, and such compare times.
# So if event2 happens later than event1, event2 > event1.
@dataclass
class PlannerEntry:
    name : str = "Untitled Entry"
    description : str = "This entry has no description yet!"
    occurance : datetime = datetime.today() + timedelta(1.0)
    color : str = "#FF0000"

    def to_dict(self):
        my_dict = {}

        for attributeName in dir(self):
            # don't put dunder methods or dunder attributes in the dictionary
            if attributeName.endswith("__"):
                continue
            
            # don't put methods in the dictionary
            attribute = getattr(self, attributeName)
            if callable(attribute):
                continue

            value = getattr(self, attributeName)
            
            # making sure that attribut
            if isinstance(value, datetime):
                value = value.isoformat()
            elif isinstance(value, timedelta):
                repetionTime = value
                # I got angry, so this is my solution. No fancy methods. Just storing days, seconds, and microseconds
                value = f"{str(repetionTime.days)}/{str(repetionTime.seconds)}/{str(repetionTime.microseconds)}"
            my_dict[attributeName] = value
        return my_dict
    
    def to_json(self):
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_dict(cls, dictionary:dict) -> "PlannerEntry":
        newEntry = PlannerEntry()
        newEntry.name = dictionary["name"]
        newEntry.description = dictionary["description"]
        newEntry.occurance = datetime.fromisoformat(dictionary["occurance"])
        newEntry.color = dictionary["color"]
        return newEntry
    
    def __sub__(self, other : "PlannerEntry") -> timedelta:
        return self.occurance - other.occurance
    
    def __gt__(self, other : "PlannerEntry") -> bool:
        timeDifferencce = self - other
        return (timeDifferencce > zeroTime)

    def __lt__(self, other : "PlannerEntry") -> bool:
        timeDifferencce = self - other
        return (timeDifferencce < zeroTime)
    
    def __ge__(self, other : "PlannerEntry") -> bool:
        timeDifferencce = self - other
        return (timeDifferencce >= zeroTime)
    
    def __le__(self, other : "PlannerEntry") -> bool:
        timeDifferencce = self - other
        return (timeDifferencce <= zeroTime)



if __name__ == "__main__":
    event1 = PlannerEntry("First Event!")
    event2 = PlannerEntry("Second Event!")
    event2.occurance += timedelta(2)

    print(event1 > event2)
    print(event2 > event1)
    print(event1.to_json())
    print(event2.to_dict())