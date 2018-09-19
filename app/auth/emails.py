from flask import render_template, current_app
from app.emails import send_email


def send_password_reset_email(employee):
    token = employee.get_reset_password_token()
    send_email('[CompensationManagementSystem] Reset Your Password',
              sender=app.config['ADMINS'][0],
              recipients=[employee.email],
              text_body=render_template('emails/reset_password.txt',
                                         employee=employee, token=token),
              html_body=render_template('emails/reset_password.html',
                                        employee=employee, token=token))
