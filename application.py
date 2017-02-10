'''
Simple Flask application to test deployment to Amazon Web Services
Uses Elastic Beanstalk and RDS

Author: Scott Rodkey - rodkeyscott@gmail.com

Step-by-step tutorial: https://medium.com/@rodkey/deploying-a-flask-application-on-aws-a72daba6bb80
'''
import datetime
import csv
import random
import time
from flask import Flask, session, redirect, url_for, escape, request, render_template, Response
from application import db
#from application.models import Data
#from application.forms import EnterDBInfo, RetrieveDBInfo

# Elastic Beanstalk initalization
application = Flask(__name__)
application.debug=True
# change this to your own value
application.secret_key = 'cC1YCIWOj9GgWspgNEo2'   

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

# GLOBAL VARIABLE INITIALIZATION

f=open('questions.csv','rb')
questions = f.readlines()
f.close()
f=open('ans.csv','rb')
answers = f.readlines()
f.close()
f = open('info.tsv','rb')
reader = csv.reader(f, dialect=csv.excel_tab)
information=[]
for row in reader:
    information.append(str(row))

# BEGIN APP.

@application.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('page1'))
    return render_template('login.html')

@application.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if len(request.form['code'])!=5:
            return render_template('login.html')
        session['username'] = int(request.form['code'])
        session['group'] = int(request.form['group'])
        session['counter'] = 0
        session['time_page_1'] = 0
        session['time_page_2'] = 0        
        session['time_page_3'] = 0        
        session['time_page_4'] = 0
        session['time_page_5'] = 0
        session['time_page_6'] = 0     
        session['pointer_time'] = 0
        session['reward'] = 0
        session['curiosity'] = 0
        session['certainty'] = 0
        session['answer'] = ''

        print session['username']
        return redirect(url_for('index'))
    return render_template('login.html')

@application.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

@application.route('/show_all')
def show_all():
   return render_template('show_all.html', students = students.query.all() )

@application.route('/waitpage')
def wait():
    '''
    def generate():
        #yield 'waiting 5 seconds\n'

        for i in range(1, 101):
            time.sleep(0.05)

            if i % 10 == 0:
                yield '{}\n'.format('*')

        #yield 'done\n'

    return Response(generate(), mimetype='text/html')'''
    now = time.time()
    return render_template('blank.html', time=now)

@application.route('/page1', methods=['GET','POST'])
def page1(x=None, y=None):
    counter = session['counter']
    qn = questions[counter]

    if request.method=='POST':
        if request.form['choice'] =='moreinfo':
            now = time.time()
            session['time_page_6'] = (now-session['pointer_time'])
            print("%s seconds page 6 " % session['time_page_6'])
        
            record = students(session['username'],session['counter'],session['group'], session['curiosity'], session['certainty'], session['answer'], session['time_page_1'],session['time_page_2'],session['time_page_3'],session['time_page_4'],session['time_page_5'],session['time_page_6'],session['reward'])
            # Enter session data into database.
            db.session.add(record)
            db.session.commit()

    # User is entering for the first time.
    session['pointer_time'] = time.time()
    #print("%s" % start_time)
    return render_template('question.html', qn=qn, group=session['group'], reward=session['reward'])

@application.route('/page2', methods=['GET','POST'])
def page2(qn_number=None):
    if request.method == 'POST':
        button = request.form['continue']
        if button == "submit":
            print "CURIOSITY: ",button
            
            now = time.time()
            session['time_page_1'] = (now-session['pointer_time'])
            print("%s seconds page 1" % session['time_page_1'])
            session['pointer_time'] = now

            return render_template('curiosity.html', group=session['group'], reward=session['reward'])
    return render_template('404.html'), 404

@application.route('/page3', methods=['GET','POST'])
def page3(qn_number=None):
    if request.method == 'POST':
        session['curiosity'] = int(request.form['choice'])
        now = time.time()
        session['time_page_2'] = (now-session['pointer_time'])
        print("%s seconds page 2" % session['time_page_2'])
        session['pointer_time'] = now
        return render_template('certainty.html',group=session['group'], reward=session['reward'])
    return render_template('404.html'), 404

@application.route('/page4', methods=['GET','POST'])
def ans(qn_number=None):
    if request.method == 'POST':
        session['certainty'] = int(request.form['choice'])
        now = time.time()
        session['time_page_3'] = (now-session['pointer_time'])
        print("%s seconds page 3 " % session['time_page_3'])
        session['pointer_time'] = now  
        return render_template('answer.html', group=session['group'], reward=session['reward'], counter=session['counter'], minimum=2)
    return render_template('404.html'), 404

@application.route('/stop', methods=['GET','POST'])
def stop(qn_number=None):
    if request.method=='POST':
        text = request.form['ans']
        session['answer'] = text
        return render_template('stop.html',ans=ans)
    return render_template('404.html'),404

@application.route('/quit', methods=['GET','POST'])
def quit():
    if request.method=='POST':
        if request.form['choice']=='stop':
            return redirect(url_for('logout'))
    return render_template('404.html'),404

@application.route('/page5', methods=['GET','POST'])
def show(qn_number=None):
    if request.method == 'POST':
        if 'ans' in request.form:
            text = request.form['ans']
            session['answer']=text

        now = time.time()
        session['time_page_4'] = (now-session['pointer_time'])
        print("%s seconds page 4 " % session['time_page_4'])
        session['pointer_time'] = now  

        counter = session['counter']
        qn = questions[counter]
        ans = answers[counter].split(",")

        if session['group']==2:
            if session['answer'] in ans:
                session['reward'] +=5
        elif session['group']==1:
            session['reward']+=5

        return render_template('show_answer.html',qn=qn,ans=ans[0], group=session['group'], reward=session['reward'])
    return render_template('404.html'), 404

@application.route('/page6',methods=['GET','POST'])
def moreinfo(qn_number=None):
    if request.method == 'POST':
        text = request.form['choice']

        now = time.time()
        session['time_page_5'] = (now-session['pointer_time'])
        print("%s seconds page 5 " % session['time_page_5'])
        session['pointer_time'] = now  

        if text == 'moreinfo':
            counter = session['counter']
            info = str(information[counter])
            session['counter']+=1
            return render_template('more_info.html',info=info, group=session['group'], reward=session['reward'])
        if text == 'next':
            session['counter']+=1
            record = students(session['username'],session['counter'],session['group'], session['curiosity'], session['certainty'], session['answer'], session['time_page_1'],session['time_page_2'],session['time_page_3'],session['time_page_4'],session['time_page_5'],session['time_page_6'],session['reward'])
            # Enter session data into database.
            print (session['username'],session['counter'],session['group'], session['curiosity'], session['certainty'], session['answer'], session['time_page_1'],session['time_page_2'],session['time_page_3'],session['time_page_4'],session['time_page_5'],session['time_page_6'],session['reward'])
            db.session.add(record)
            db.session.commit()
            return redirect(url_for('page1'))

    return render_template('404.html'), 404

@application.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404        

if __name__ == '__main__':
    application.run(host='0.0.0.0')
