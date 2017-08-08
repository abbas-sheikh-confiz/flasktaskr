# db_create.py

from datetime import date


from project import db
from project.models import Task, User


# create the database and the db table
db.create_all()

# insert data
db.session.add(
	User("admin", "admin@gmail.com", "lahore", "admin")
	)

db.session.add(Task("Finish this tutorial", date(2017, 10, 22), 10, date(2017, 8, 8), 1, 1))
db.session.add(Task("Finish Real Python", date(2017, 10, 21), 10, date(2017, 8, 8), 1, 1))

# commit the changes
db.session.commit()
