import sqlite3

class Person():
    def __init__(self, first=None, last=None, age=None):
        self.first = first
        self.last = last
        self.age = age
    
    def clone_person(self, result):
        self.first = result[0]
        self.last = result[1]
        self.age = result[2]

conn = sqlite3.connect("mydata.db")

c = conn.cursor()
'''
c.execute("""CREATE TABLE persons (
          first_name TEXT,
          last_name TEXT,
          age INTEGER
          )""")

'''

'''
c.execute("""INSERT INTO persons VALUES
          ('John', 'Smith', 25),
          ('Anna', 'Smith', 30),
          ('Mike', 'Johnson', 40)""")
'''

c.execute("""SELECT * FROM persons WHERE last_name = 'Smith'""")
person1 = Person()
person1.clone_person(c.fetchone())

print(person1.first, person1.last, person1.age)



conn.commit()
conn.close()