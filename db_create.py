from application import db
from application.models import students
from application.models import user_profiles

db.create_all()

print("DB created.")
