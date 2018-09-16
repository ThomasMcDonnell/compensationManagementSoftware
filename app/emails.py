from flask_mail import Message
from flask import render_template 
from threading import Thread
from app import app, mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_mail(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()

def send_password_reset_email(employee):
    token = employee.get_reset_password_token()
    send_mail('[CompensationManagementSystem] Reset Your Password', 
              sender=app.config['ADMINS'][0],
              recipients=[employee.email],
              text_body=render_template('emails/reset_password.txt',
                                         employee=employee, token=token),
              html_body=render_template('emails/reset_password.html',
                                        employee=employee, token=token))
