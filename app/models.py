from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from hashlib import md5
from app import db, login


class Employee(UserMixin, db.Model):

    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    last_active = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))

    def set_password(self, password):
        """
        Generate password hash
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Check password against hash
        """
        return check_password_hash(self.password_hash, password)

    def user_type(self):
        """
        Determine User permissions (admin=True or admin=False)
        """
        return self.is_admin

    def __repr__(self):
        return f'Employee: {self.first_name} {self.last_name}'


class Company(db.Model):

    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    employees = db.relationship('Employee', backref='member_of', lazy='dynamic')
    records = db.relationship('Record', backref='bonus', lazy='dynamic')
    rota = db.relationship('Rota', backref='weekly_rota', lazy='dynamic')

    def __repr__(self):
        return f'Store: {self.company_name}'


class Record(db.Model):

    __tablename__ = 'record'

    id = db.Column(db.Integer, primary_key=True)
    gross = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    qtr = db.Column(db.Integer)
    msr = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))

    def __repr__(self):
        return f'Record: {self.id}, Amount: {self.amount}, Notes: {self.notes}'


class Rota(db.Model):

    __tablename__ = 'rota'

    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(300))
    file_data = db.Column(db.LargeBinary)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))

    def __repr__(self):
        return f'Rota: {self.file_name}'


@login.user_loader
def user_loader(id):
    """
    Given *user_id*, return the associated User object.
    param: unicode user id: id user to retrieve
    """
    return Employee.query.get(int(id))
