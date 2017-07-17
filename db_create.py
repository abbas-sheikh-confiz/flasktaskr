import sqlite3
from _config import DATABASE_PATH

print(DATABASE_PATH)

with sqlite3.connect(DATABASE_PATH) as connection:
	# get a cursor object used to execute SQL commands
	c = connection.cursor()

	# create the table
	c.execute("DROP TABLE if exists tasks")
	c.execute("""CREATE TABLE tasks(task_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, due_date TEXT NOT NULL,
				 priority INTEGER NOT NULL, status INTEGER not NULL)""")

	# insert new tasks in the system
	c.execute("INSERT INTO tasks (name, due_date, priority, status) VALUES(?, ?, ?, ?)", ('Finish this tutorial', '07/18/2017', 10, 1))
	c.execute("INSERT INTO tasks (name, due_date, priority, status) VALUES('Finish Real Python Course 2', '09/18/2017', 10 , 1)")
