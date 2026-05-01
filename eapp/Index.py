from flask import Flask,render_template
from flask_login import current_user
from __init__ import app
from __init__ import login_manager
import dao,flask_login

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('layout/index.html')

@app.context_processor
def inject_user():
    return dict(current_user=current_user)

@login_manager.user_loader
def load_user(id):
    return dao.load_student_by_id(id)

@app.route('/dang-ky')
def trang_dang_ky():
    return render_template('layout/dangky.html')

@app.route('/studen-history')
def student_history():
    return render_template('layout/student_history.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('layout/login.html')

if __name__=="__main__":
    app.run(debug=True)