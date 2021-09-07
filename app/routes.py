from flask import render_template, flash, redirect, url_for, request
from app import app,db

from app.forms import ClassForm, RegistrationForm
from app.models import Class, Major, Student

@app.before_first_request
def initDB(*args, **kwargs):
    db.create_all()
    if Major.query.count() ==0:
        majors = [{'name' : 'Cpts', 'department': 'School of EECS'} , 
        {'name' : 'SE', 'department': 'School of EECS'}, 
        {'name' : 'EE', 'department': 'School of EECS'}, 
        {'name' : 'ME', 'department': 'Mechanical Engineering'},
        {'name' : 'MATH', 'department': 'Mathematics'}]
        for t in majors:
            db.session.add(Major(name=t['name'], department = t['department']))
            db.session.commit()

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    allclasses = Class.query.order_by(Class.major).all()
    return render_template('index.html', title="Course List", classes = allclasses)

@app.route('/createclass/', methods=['GET','POST'])
def createclass():
    cform = ClassForm()
    if cform.validate_on_submit():
        newClass = Class(coursenum = cform.coursenum.data, title = cform.title.data, major = cform.major.data.name )
        db.session.add(newClass)
        db.session.commit()
        flash('Class "' + newClass.major + '-' + newClass.coursenum + '" is created')
        return redirect(url_for('index'))
    return render_template( 'create_class.html', form = cform)

@app.route('/register', methods=['GET', 'POST'])
def register():
    rform = RegistrationForm()
    if rform.validate_on_submit():
        student =Student(username=rform.username.data, email=rform.email.data,firstname=rform.firstname.data, lastname=rform.lastname.data, address=rform.address.data)
        student.set_password(rform.password.data)
        db.session.add(student)
        db.session.commit()
        flash('Congratulations, you are registered!')
        return redirect(url_for('index'))
    return render_template('register.html', form = rform)