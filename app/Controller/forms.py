from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import  ValidationError, Length , DataRequired, Email, EqualTo
from app.Model.models import Major, Student
from flask_login import current_user

def get_major():
    return Major.query.all()

def get_majorlabel(theMajor):
    return theMajor.name

class ClassForm(FlaskForm):
    coursenum = StringField('Course Number',[Length(min=3, max=3)])
    title = StringField('Course Title' , validators=[DataRequired()])
    major = QuerySelectField('Majors', query_factory = get_major, get_label = get_majorlabel , allow_blank=False)
    submit = SubmitField('Post')

class EditForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = TextAreaField('Address', [Length(min=0, max=200)])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        student = Student.query.filter_by(email =email.data).all()
        for student in student:
            if (student.id != current_user.id):
                raise ValidationError('The email is associated with another account, Please enter a different email.')

class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')