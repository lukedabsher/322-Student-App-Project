from enum import unique
from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

@login.user_loader
def load_user(id):
    return Student.query.get(int(id))
    
enrolled = db.Table('enrolled',
db.Column('studentid', db.Integer, db.ForeignKey('student.id')),
db.Column('classid', db.Integer, db.ForeignKey('class.id'))
)

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coursenum = db.Column(db.String(3))  
    title = db.Column(db.String(150))
    major = db.Column(db.String(20),db.ForeignKey('major.name'))
    roster = db.relationship(
        'Student' , secondary= enrolled,
        primaryjoin=(enrolled.c.classid == id), lazy = 'dynamic', overlaps="classes")
    
    def __repr__(self):
        return '<Class id: {} - coursenum: {}, title {}, major: {}>'.format(self.id,self.coursenum,self.title,self.major)
    def getTitle(self):
        return self.title

class Major(db.Model):
    name = db.Column(db.String(20), primary_key=True)
    department = db.Column(db.String(150))
    classes = db.relationship('Class', backref= 'coursemajor', lazy='dynamic')
    def __repr__(self):
        return '<Major name: {} - department: {}>'.format(self.name,self.department)

class Student(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64) ,unique=True,index=True)
    password_hash = db.Column(db.String(128))
    firstname = db.Column(db.String(128))
    lastname =db.Column(db.String(128))
    address = db.Column(db.String(128))
    email =  db.Column(db.String(128),unique=True,index=True)
    last_seen =  db.Column(db.DateTime, default=datetime.utcnow)
    classes = db.relationship(
        'Class' , secondary= enrolled,
        primaryjoin=(enrolled.c.studentid == id), lazy = 'dynamic', overlaps="roster")
    
    def __repr__(self):
        return '<Student {} - {}{} - {};>'.format(self.id,self.firstname, self.lastname, self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        self.password_hash = check_password_hash(password)

    def enroll(self,newclass):
        if not self.is_enrolled(newclass):
            self.classes.append(newclass)

    def unenroll(self,oldclass):
        if self.is_enrolled(oldclass):
            self.classes.remove(oldclass)

    def is_enrolled(self,newclass):
        self.classes.filter(enrolled.c.classid == newclass.id).count() > 0

    def enrolledCourses(self):
        return self.classes