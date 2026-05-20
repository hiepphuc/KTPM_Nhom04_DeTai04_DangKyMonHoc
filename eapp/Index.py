import hashlib

import flask_login

from eapp import admin, dao
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user
from eapp import app
from eapp import login_manager

from eapp.enums import Role
from eapp.models import Student


@app.context_processor
def inject_user():
    return dict(current_user=current_user)

@login_manager.user_loader
def load_user(id):
    return dao.load_student_by_id(id)

@app.route('/')
def home_page():
    return render_template('layout/index.html')

@app.route('/student-history')
@flask_login.login_required
def student_history():
    history, registered = dao.get_student_history(current_user.id)
    return render_template('layout/student_history.html',
                           history=history,
                           registered=registered)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        student_id = request.form.get('student_id','').strip()
        password = request.form.get('password','').strip()

        sv = dao.login(student_id=student_id, password=password)

        if sv:
            login_user(sv)

            target = request.args.get('next')
            return redirect(target if target else url_for('home_page'))
        else:
            flash('Mã số sinh viên hoặc mật khẩu không đúng', 'danger')
            return redirect(url_for('login'))

    return render_template('layout/login.html')

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated and current_user.role == Role.ADMIN:
        return redirect('/admin')

    if request.method == 'POST':
        student_id = request.form.get('student_id', '').strip()
        password   = request.form.get('password', '')
        password_md5 = hashlib.md5(password.encode('utf-8')).hexdigest()

        sv = Student.query.filter_by(
            student_id=student_id,
            password=password_md5,
            role=Role.ADMIN
        ).first()

        if sv:
            flask_login.login_user(sv)
            return redirect('/admin')
        else:
            flash('Sai thông tin hoặc không có quyền admin!', 'danger')

    return render_template('admin/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name','').strip()
        email = request.form.get('email','').strip()
        student_id = request.form.get('student_id','').strip()
        password = request.form.get('password','')
        password_confirm = request.form.get('password_confirm','')

        if password != password_confirm:
            return render_template('layout/register.html', err_msg="Mật khẩu không khớp!")

        try:
            dao.register(
                name=name,
                student_id=student_id,
                email=email,
                password=password,
            )
            flash('Đăng ký thành công! Vui lòng đăng nhập.', 'success')
            return redirect(url_for('login'))
        except ValueError as e:  # ← bắt ValueError riêng
                return render_template('layout/register.html', err_msg=str(e))
        except Exception:
                return render_template('layout/register.html',
                                   err_msg="Không thể đăng ký, vui lòng thử lại!")


    return render_template('layout/register.html')

@app.route('/logout')
def logout_process():
    logout_user()
    return redirect('/login')

@app.route('/register-course', methods=['GET', 'POST'])
@flask_login.login_required
def register_course():
    semesters  = dao.get_all_semesters()
    semester_id = request.args.get('semester_id', type=int)

    sections       = []
    my_registrations = []

    if semester_id:
        sections         = dao.get_sections_by_semester(semester_id)
        my_registrations = dao.get_registered_sections(current_user.id)

    return render_template('layout/register_course.html',
                           semesters=semesters,
                           sections=sections,
                           my_registrations=my_registrations,
                           semester_id=semester_id)


@app.route('/register-course/add', methods=['POST'])
@flask_login.login_required
def add_registration():
    section_id  = request.form.get('section_id',  type=int)
    semester_id = request.form.get('semester_id', type=int)

    ok, msg = dao.register_course(current_user.id, section_id)
    flash(msg, 'success' if ok else 'danger')
    return redirect(url_for('register_course', semester_id=semester_id))


@app.route('/register-course/cancel', methods=['POST'])
@flask_login.login_required
def cancel_registration():
    registration_id = request.form.get('registration_id', type=int)
    semester_id     = request.form.get('semester_id',     type=int)

    ok, msg = dao.cancel_course(current_user.id, registration_id)
    flash(msg, 'success' if ok else 'danger')
    return redirect(url_for('register_course', semester_id=semester_id))

if __name__=="__main__":
    app.run(debug=True)