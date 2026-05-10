from flask import  Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)

app.secret_key='ABCDENADA@#%^@##@&#^WSF'
app.config["SQLALCHEMY_DATABASE_URI"] ="mysql+pymysql://root:root@localhost/coursedb?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

login_manager = LoginManager(app)
db = SQLAlchemy(app)


