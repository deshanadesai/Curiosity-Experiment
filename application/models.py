from application import db

class profiles(db.Model):
    number_code = db.Column('number_code',db.Integer, primary_key=True)
    group = db.Column(db.Integer)
    timestamp = db.Column(db.TIMESTAMP)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(1))
    language = db.Column(db.String(50))
    english = db.Column(db.Integer)
    grade = db.Column(db.String(10))
    background = db.Column(db.String(10))
    medium = db.Column(db.String(10))
    phone = db.Column(db.String(10))
    q1 = db.Column(db.Integer)
    q2 = db.Column(db.Integer)
    q3 = db.Column(db.Integer)
    q4 = db.Column(db.Integer)
    q5 = db.Column(db.Integer)
    q6 = db.Column(db.Integer)
    q7 = db.Column(db.Integer)

    def __init__(self,number_code,group,age,gender,language,english,grade,background,medium,phone,q1,q2,q3,q4,q5,q6,q7):
        self.timestamp = datetime.datetime.now()
        self.number_code = number_code
        self.group = group
        self.age = age
        self.gender = gender
        self.language = language
        self.english = english
        self.grade = grade
        self.background = background
        self.medium = medium
        self.phone = phone
        self.q1 = q1
        self.q2 = q2
        self.q3 = q3
        self.q4 = q4
        self.q5 = q5
        self.q6 = q6
        self.q7 = q7

    def __repr__(self):
        return '<User %r>' % self.number_code




class students(db.Model):
    record_num = db.Column('record_number', db.TIMESTAMP, primary_key = True)
    uid = db.Column(db.Integer, primary_key = True)
    question_number = db.Column(db.Integer)
    group = db.Column(db.Integer)
    curiosity_rating = db.Column(db.Integer)  
    certainty_rating = db.Column(db.Integer)
    answer = db.Column(db.String(50))
    time_page_1 = db.Column(db.Float)
    time_page_2 = db.Column(db.Float)
    time_page_3 = db.Column(db.Float)
    time_page_4 = db.Column(db.Float)
    time_page_5 = db.Column(db.Float)
    time_page_6 = db.Column(db.Float)
    reward = db.Column(db.Integer)

    def __init__(self, uname,question_number,group,curiosity_rating,certainty_rating,answer,time_page_1,time_page_2,time_page_3,time_page_4,time_page_5,time_page_6,reward):
        self.record_num = datetime.datetime.now()
        self.uid = uname
        self.question_number=question_number
        self.group = group
        self.curiosity_rating = curiosity_rating
        self.certainty_rating = certainty_rating
        self.answer = answer
        self.time_page_1 = time_page_1
        self.time_page_2 = time_page_2
        self.time_page_3 = time_page_3
        self.time_page_4 = time_page_4
        self.time_page_5 = time_page_5
        self.time_page_6 = time_page_6
        self.reward = reward

    def __repr__(self):
        return '<User %r>' % self.record_num

