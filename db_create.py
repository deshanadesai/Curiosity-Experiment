from application import db
from application.models import students

db.create_all()

print("DB created.")
