from flask import (render_template, flash, redirect, url_for,
                   request, abort, send_file, jsonify, current_app)
from flask_login import current_user, login_required
from app import db
from app.main.forms import RecordForm, UploadRota
from app.auth.forms import EmployeeAccount
from app.main import bp
from app.models import Company, Employee, Record, Rota
from datetime import datetime
from io import BytesIO


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_active = datetime.utcnow()
        db.session.commit()


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    user = Employee.query.filter_by(id=current_user.id).first_or_404()
    company = Company.query.get(int(user.company_id))
    records = Record.query.filter_by(company_id=company.id).order_by(
        Record.timestamp.desc()).paginate(page,
                                          current_app.config['RECORDS_PER_PAGE'],
                                          False)
    rotas = Rota.query.filter_by(company_id=company.id)
    next_url = url_for('main.index', page=records.next_num) \
        if records.has_next else None
    prev_url = url_for('main.index', page=records.prev_num) \
        if records.has_prev else None
    if user.is_admin:
        form = EmployeeAccount()
        form_record = RecordForm()
        form_file_upload = UploadRota()
        return render_template('dashboard.html', title='Dashboard',
                               company=company, records=records.items,
                               rotas=rotas, form=form, form_record=form_record,
                               form_file_upload=form_file_upload, next_url=next_url,
                               prev_url=prev_url)
    return render_template('index.html', title='Home', company=company,
                           records=records, rotas=rotas)

@bp.route('/employee/create', methods=['GET', 'POST'])
@login_required
def employee():
    user = Employee.query.filter_by(id=current_user.id).first_or_404()
    company = Company.query.get(int(user.company_id))
    if user.is_admin:
        form = EmployeeAccount()
        if form.validate_on_submit():
            employee = Employee(first_name=form.first_name.data,
                                last_name=form.last_name.data, email=form.email.data,
                                member_of=company)
            employee.set_password(form.password.data)
            db.session.add(employee)
            db.session.commit()
            flash('Employee has been added to your account.')
            return redirect(url_for('main.index'))
        flash('Employee could not be created.')
        return redirect(url_for('main.index'))
    return redirect(url_for('main.index'))


@bp.route('/analytics')
@login_required
def analytics():
    user = Employee.query.filter_by(id=current_user.id).first_or_404()
    company = Company.query.get(int(user.company_id))
    rotas = Rota.query.filter_by(company_id=company.id)
    return render_template('index.html', company=company, rotas=rotas,
                           title='Home')


@bp.route('/record/create', methods=['GET', 'POST'])
@login_required
def record():
    user = Employee.query.filter_by(id=current_user.id).first_or_404()
    company = Company.query.get(int(user.company_id))
    if user.is_admin:
        form = RecordForm()
        if form.validate_on_submit():
            record = Record(qtr=form.qtr.data, gross=form.gross.data,
                            amount=form.amount.data, msr=form.msr.data,
                            timestamp=form.timestamp.data, bonus=company)
            db.session.add(record)
            db.session.commit()
            flash('Record has been created.')
            return redirect(url_for('main.index'))
        flash('An error occurred.')
        return redirect(url_for('main.index'))
    return redirect(url_for('main.index'))


@bp.route('/upload/file', methods=['GET', 'POST'])
@login_required
def upload_file():
    user = Employee.query.filter_by(id=current_user.id).first_or_404()
    company = Company.query.get(int(user.company_id))
    if user.is_admin:
        form = UploadRota()
        if form.validate_on_submit():
            file_upload = form.upload.data
            _file = Rota(file_name=file_upload.filename,
                         file_data=file_upload.read(), weekly_rota=company)
            db.session.add(_file)
            db.session.commit()
            flash('Rota has been uploaded successfully.')
            return redirect(url_for('main.index'))
        flash('An error occurred. Please ensure correct file format.')
        return redirect(url_for('main.index'))
    return redirect(url_for('main.index'))


@bp.route('/download/file<int:id>')
@login_required
def file_download(id):
    data = Rota.query.get_or_404(id)
    return send_file(BytesIO(data.file_data), attachment_filename='Rota.pdf',
                     as_attachment=False)


@bp.route('/delete/rota<int:id>', methods=['GET', 'POST'])
@login_required
def delete_rota(id):
    rota = Rota.query.get_or_404(id)
    if not current_user.is_admin:
        abort(404)
    db.session.delete(rota)
    db.session.commit()
    flash('Rota has been deleted.')
    return redirect(url_for('main.index'))


@bp.route('/delete/record<int:id>', methods=['GET', 'POST'])
@login_required
def delete_record(id):
    record = Record.query.get_or_404(id)
    if not current_user.is_admin:
        abort(404)
    db.session.delete(record)
    db.session.commit()
    flash('Record has been deleted.')
    return redirect(url_for('main.index'))


@bp.route('/delete/employee<int:id>', methods=['GET', 'POST'])
@login_required
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    if not current_user.is_admin:
        abort(404)
    db.session.delete(employee)
    db.session.commit()
    flash('Employee has been deleted.')
    return redirect(url_for('main.index'))


@bp.route('/delete/record/all<int:id>', methods=['GET', 'POST'])
@login_required
def delete_all_records(id):
    employee = Employee.query.get_or_404(id)
    if not employee.is_admin:
        abort(404)
    company = Company.query.get(int(employee.company_id))
    Record.query.filter_by(company_id=company.id).delete()
    db.session.commit()
    flash('All records have now been deleted.')
    return redirect(url_for('main.index'))


# api end points
@bp.route('/record/api')
@login_required
def record_api():
    user = Employee.query.filter_by(id=current_user.id).first_or_404()
    company = Company.query.get(int(user.company_id))
    records = Record.query.filter_by(company_id=company.id).order_by(
        Record.timestamp)
    bonus_arr, msr_arr, date_arr = list(), list(), list()
    for row in records:
        bonus_arr.append(row.amount)
        msr_arr.append(row.msr)
        date_arr.append(str(row.timestamp)[:10])
    return jsonify({'bonus': bonus_arr, 'date': date_arr,
                    'msr': msr_arr})


# api end points
@bp.route('/record/qtr/api')
@login_required
def record_qtr_api():
    user = Employee.query.filter_by(id=current_user.id).first_or_404()
    company = Company.query.get(int(user.company_id))
    records = Record.query.filter_by(company_id=company.id).order_by(
        Record.timestamp)
    qtr1, qtr2, qtr3, qtr4 = 0, 0, 0, 0
    for row in records:
        if row.qtr == 1:
            qtr1 += row.amount
        elif row.qtr == 2:
            qtr2 += row.amount
        elif row.qtr == 3:
            qtr3 += row.amount
        elif row.qtr == 4:
            qtr4 += row.amount
    return jsonify({'qtr1': qtr1, 'qtr2': qtr2, 'qtr3': qtr3, 'qtr4': qtr4})
