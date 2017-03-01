from application import db
from application.models import students
from application.models import profiles

db.create_all()

print("DB created.")
