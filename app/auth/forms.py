from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import Company, Employee


class CompanyAccount(FlaskForm):
    company_name = StringField('Company Name', validators=[DataRequired()])
    company_email = StringField('Company Email', validators=[DataRequired(),
                                                             Email()])
    admin_first_name = StringField('First name', validators=[DataRequired()])
    admin_last_name = StringField('Last name', validators=[DataRequired()])
    admin_email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_two = PasswordField('Confirm Password',
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


class EmployeeAccount(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_two = PasswordField('Confirm Password',
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


class Login(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
