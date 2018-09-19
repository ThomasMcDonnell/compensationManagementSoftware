from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import SubmitField, FloatField, FileField
from wtforms.fields.html5 import DateField, IntegerField
from wtforms.validators import (DataRequired, NumberRange)


class RecordForm(FlaskForm):
    qtr = IntegerField('Quarter', validators=[DataRequired(),
                                              NumberRange(1, 4)])
    gross = FloatField('Weekly Sales', validators=[DataRequired()],
                       description='Amount in euros and cents.')
    amount = FloatField('Bonus Amount', validators=[DataRequired()],
                        description='Amount in euros and cents.')
    msr = IntegerField('MSR', validators=[DataRequired(), NumberRange(0, 100)],
                       description='% round up or down.')
    timestamp = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Create')


class UploadRota(FlaskForm):
    upload = FileField('pdf File', validators=[FileRequired(),
                                               FileAllowed(['pdf'],
                                                           'pdf files only!')])
    submit = SubmitField('Upload File')
