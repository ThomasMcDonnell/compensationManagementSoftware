from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.auth import bp
from app.auth.forms import (CompanyAccount, EmployeeAccount, Login,
                            ResetPasswordRequestForm, ResetPasswordForm)
from app.models import Company, Employee
from app.auth.emails import send_password_reset_email


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = Login()
    if form.validate_on_submit():
        user = Employee.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Email or Password.')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
            return redirect(next_page)
    return render_template('auth/login.html', title='Login', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@bp.route('/register', methods=['GET', 'POST'])
def company_registration():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = CompanyAccount()
    if form.validate_on_submit():
        company = Company(company_name=form.company_name.data,
                          email=form.company_email.data)
        admin = Employee(email=form.admin_email.data,
                         first_name=form.admin_first_name.data,
                         last_name=form.admin_last_name.data,
                         is_admin=True, member_of=company)
        admin.set_password(form.password.data)
        db.session.add(company, admin)
        db.session.commit()
        flash('Your company has been registered sucessfully.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)


@bp.route('/reset/password/request', methods=['GET', 'POST'])
def password_reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        employee = Employee.query.filter_by(email=form.email.data).first()
        if employee:
            send_password_reset_email(employee)
            flash('An email has been sent to the address you have provided.')
            return redirect(url_for('auth.login'))
        flash('Invalid email. There is not such email registered.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html',
                           title='Password Reset', form=form)


@bp.route('/reset/password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    employee = Employee.verify_reset_password_token(token)
    if not employee:
        flash('Invalid Token or Reset Password Expired')
        return redirect(url_for('auth.login'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        employee.set_password(form.password.data)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)
