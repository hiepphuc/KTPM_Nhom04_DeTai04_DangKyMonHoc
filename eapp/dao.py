from models import *
import hashlib

def load_student_by_id(id):
    return Student.query.get(id)

def login(student_id, password):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    return Student.query.filter(Student.student_id == student_id.strip(),
                             Student.password == password).first()

def register(name, email, password, student_id):
    s = Student(
        name=name,
        email=email,
        student_id=student_id,
        role=Role.STUDENT,
        active=True,
        created_at=datetime.now(),
        password=str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    )
    db.session.add(s)
    db.session.commit()

def get_student_by_studentid(student_id):
    return Student.query.filter(Student.student_id == student_id.strip()).first()

def get_student_by_email(email):
    return Student.query.filter(Student.email == email.strip()).first()

