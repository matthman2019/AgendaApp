# Event inherits from PlannerEntry. It is an entry.
# But it can repeat itself. This makes it useful for storing holidays, for instance.

from PlannerEntry import PlannerEntry
from datetime import datetime, timedelta
from calendar import isleap

class Event(PlannerEntry):
    def __init__(self, 
                name : str = "Untitled Entry", 
                description : str = "This entry has no description yet!",
                occurance : datetime = datetime.today() + timedelta(1.0),
                color : str = "#FF0000",
                repeats : bool = True,
                repeatTime : timedelta = None):
        
        super().__init__(name, description, occurance, color)
        self.repeats : bool = repeats
        self.repeatTime : timedelta = repeatTime
        if repeatTime is None:
            # we set the default repeat time to one year. 366 days if a leap year, 365 otherwise
            if isleap(occurance.year):
                self.repeatTime = timedelta(366)
            else:
                self.repeatTime = timedelta(365)

if __name__ == "__main__":
    event1 = Event("First event!")
    print(event1.to_json())

    