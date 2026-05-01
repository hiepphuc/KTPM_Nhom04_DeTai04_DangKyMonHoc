from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_user
from __init__ import app
from __init__ import login_manager
import dao,flask_login

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
def student_history():
    return render_template('layout/student_history.html')

@app.route('/register_course')
def register_course():
    return render_template('layout/register_course.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        password = request.form.get('password')

        sv = dao.login(student_id=student_id, password=password)

        if sv:
            login_user(sv)

            target = request.args.get('next')
            return redirect(target if target else url_for('home_page'))
        else:
            flash('Mã số sinh viên hoặc mật khẩu không đúng', 'danger')
            return redirect(url_for('login'))

    return render_template('layout/login.html')


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

        if dao.get_student_by_studentid(student_id):
            return render_template('layout/register.html', err_msg="Mã số sinh viên đã tồn tại!")

        if dao.get_student_by_email(email):
            return render_template('layout/register.html', err_msg="Email đã được sử dụng!")

        try:
            dao.register(
                name=name,
                student_id=student_id,
                email=email,
                password=password,
            )
            flash('Đăng ký thành công! Vui lòng đăng nhập.', 'success')
            return redirect(url_for('login'))
        except Exception as ex:
            return render_template('layout/register.html', err_msg="Không thể đăng ký, vui lòng thử lại!")

    return render_template('layout/register.html')

@app.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for('login'))

if __name__=="__main__":
    app.run(debug=True)