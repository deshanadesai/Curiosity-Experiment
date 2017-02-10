from application import db

class students(db.Model):
    record_num = db.Column('record_number', db.TIMESTAMP, primary_key = True)
    uid = db.Column(db.Integer)
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


