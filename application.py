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
# from application.models import Data
# from application.forms import EnterDBInfo, RetrieveDBInfo

# Elastic Beanstalk initalization
application = Flask(__name__)
application.debug=True
# change this to your own value
application.secret_key = 'cC1YCIWOj9GgWspgNEo2'   

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

MAX_QUESTIONS = len(questions)

# BEGIN APP.

@application.route('/')
def index():
	if 'username' in session:
		return redirect(url_for('page1'))
	try:
		message=request.args.get('message')
	except:
		message=''
	print "Login message: ",message
	return render_template('login.html',message=message)

@application.route('/signup', methods=['GET', 'POST'])
def signup():
	return render_template('signup.html')

@application.route('/consent', methods=['GET', 'POST'])
def consent():
	if request.method == 'POST':
		try:
			message=request.form['message']
		except:
			message=''
		print "Consent message: ",message
		return redirect(url_for('index',message=message))
	try:
		message=request.args.get('message')
	except:
		message=''
	#print "Consent message: ",message
	return render_template('consent.html',message=message)

@application.route('/store_profile', methods=['GET', 'POST'])
def store_profile():
	if request.method == 'POST':
		numbercode = int(request.form['code'])
		group = int(request.form['group'])
		age = int(request.form['age'])
		gender = request.form['gender']
		language = request.form['language']
		english = int(request.form['eng'])
		grade = request.form['grade']
		background = request.form['background']
		medium = request.form['medium']
		phone = request.form['phone']
		q1 = int(request.form['q1'])
		q2 = int(request.form['q2'])
		q3 = int(request.form['q3'])
		q4 = int(request.form['q4'])
		q5 = int(request.form['q5'])
		q6 = int(request.form['q6'])
		q7 = int(request.form['q7'])
		profile = profiles(numbercode,group, age, gender, language, english, grade, background, medium, phone,q1,q2,q3,q4,q5,q6,q7)
		print (numbercode,group, age, gender, language, english, grade, background, medium, phone,q1,q2,q3,q4,q5,q6,q7)
		try:
			db.session.add(profile)		
			db.session.commit()
			print "added"
			message = 'Successful Signup. Please login!'
			return redirect(url_for('consent',message=message))
		except:
			db.session.rollback()
			message = 'Invalid number code. Please try again!'
			return redirect(url_for('index',message=message))
	return render_template('404.html')

@application.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		numbercode = int(request.form['code'])
		user = profiles.query.filter_by(number_code=numbercode).first()
		if user is None:
			message = 'Incorrect code. Please signup before login.'
			return redirect(url_for('index',message=message))
		if user.group != int(request.form['group']):
			message = 'Incorrect Group Number. Please Enter Correct Group.'
			return redirect(url_for('index',message=message))
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

@application.route('/quit_message')
def quit_message():
	message=request.args.get('message')
	session.pop('username', None)
	return render_template('gameover.html',message=message)


@application.route('/show_all')
def show_all():
   return render_template('show_all.html', students = students.query.all() )


@application.route('/show_users')
def show_users():
   return render_template('show_users.html', profiles = profiles.query.all() )

@application.route('/waitpage')
def wait():
	#time.sleep(3)
	now = time.time()
	session['pointer_time'] = now
	#now = time.time()
	#return render_template('blank.html', time=now)
	return render_template('certainty.html',group=session['group'], reward=session['reward'])

@application.route('/page1', methods=['GET','POST'])
def page1(x=None, y=None):
	counter = session['counter']
	global MAX_QUESTIONS
	if counter>=MAX_QUESTIONS:
		message = 'Congratulations! The game is over. Thank you for playing.'
		return redirect(url_for('quit_message',message=message))
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
        return redirect(url_for('wait'))
        #return render_template('certainty.html',group=session['group'], reward=session['reward'])
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
			message = 'Congratulations! The game is over. Thank you for playing.'
			return redirect(url_for('quit_message',message=message))
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
