# project/db_migrate.py

import sqlite3
from _config import DATABASE_PATH

from views import db

from datetime import datetime

with sqlite3.connect(DATABASE_PATH) as connection:
	c = connection.cursor()

	# rename the tasks table
	c.execute("ALTER TABLE tasks RENAME TO old_tasks")

	# recreate new tasks table with updated schema
	db.create_all()

	# retreive data from old schema
	c.execute("SELECT name, due_date, priority, status FROM old_tasks ORDER BY task_id ASC")
	data = [(row[0], row[1], row[2], row[3], datetime.now(), 1) for row in c.fetchall()]

	# insert data to tasks table
	c.executemany("INSERT INTO tasks (name, due_date, priority, status, posted_date, user_id) VALUES(?, ?, ?, ?, ?, ?)", data)

	# delete old_tasks table
	c.execute("DROP TABLE old_tasks")