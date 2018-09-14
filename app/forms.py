from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import (StringField, PasswordField, BooleanField, SubmitField,
                    TextAreaField, IntegerField, DateField, FloatField, 
                    FileField)
from wtforms.validators import (DataRequired, ValidationError, Email, EqualTo, 
                               Length, NumberRange)
from wtforms.fields.html5 import DateField, IntegerField
from app.models import Company, Employee, Record


class CompanyAccount(FlaskForm):
    company_name = StringField('Company Name', validators=[DataRequired()])
    company_email = StringField('Comapny Email', validators=[DataRequired(),
                                                             Email()])
    admin_first_name = StringField('First name', validators=[DataRequired()])
    admin_last_name = StringField('Last name', validators=[DataRequired()])
    admin_email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_two = PasswordField('Confrim Password',
                                validators=[DataRequired(),
                                            EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_company_name(self, company_name):
        """
        Check availability of company name
        """
        company = Company.query.filter_by(
            company_name=company_name.data
        ).first()
        if company is not None:
            raise ValidationError('This Company is already registered.')

    def validate_company_email(self, company_email):
        """
        Check availability of company email
        """
        company_email = Company.query.filter_by(
            email=company_email.data
        ).first()
        if company_email is not None:
            raise ValidationError('This email is already registered to a\
                                  company.')


class Login(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class EmployeeAccount(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_two = PasswordField('Confrim Password',
                                validators=[DataRequired(),
                                            EqualTo('password')])
    submit = SubmitField('Create')
    
    def validate_email(self, email):
        """
        Check availability of email (used for employee login)
        """
        user = Employee.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('This email is already in use. Please choose\
                                  another.')

class RecordForm(FlaskForm):
    qtr = IntegerField('Quarter', validators=[DataRequired(),
                                              NumberRange(1,4)])
    gross = FloatField('Weekly Sales', validators=[DataRequired()],
                         description='Amount in euros and cents.')
    amount = FloatField('Bonus Amount', validators=[DataRequired()],
                         description='Amount in euros and cents.')
    msr = IntegerField('MSR', validators=[DataRequired(), NumberRange(0,100)],
                      description='% round up or down.')
    timestamp = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Create')
 

class UploadRota(FlaskForm):
    upload = FileField('pdf File', validators=[FileRequired(),
                                          FileAllowed(['pdf'],
                                          'pdf files only!')])
    submit = SubmitField('Upload File')
