import hashlib
from datetime import datetime

import pytest
from flask import Flask

from eapp import app as flask_app, db
from eapp.enums import Role
from eapp.models import Student, Semester, Course, Section, StudentHistory


def create_app():
    app=Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    db.init_app(app)

    return app

@pytest.fixture
def test_app():
    app=create_app()
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def test_session(test_app):
    yield db.session
    db.session.rollback()

@pytest.fixture
def create_student(test_app):
        s = Student(
                student_id='2351050135',
                name='Phúc',
                email='2351050135phuc@gmail.com',
                password=str(hashlib.md5("123456".encode('utf-8')).hexdigest()),
                role=Role.STUDENT,
                active=True,
                created_at=datetime.now()
            )
        db.session.add(s)
        db.session.commit()
        db.session.refresh(s)
        return s

@pytest.fixture
def create_semester(test_app):
    se = Semester(name="Học kỳ 3", start_date=datetime.now(),
                  end_date=datetime(2026,11,21),
                  registration_deadline=datetime(2026,6,20))
    db.session.add(se)
    db.session.commit()
    db.session.refresh(se)
    return se

@pytest.fixture
def create_course(test_app):
    c = Course(course_code='KTPM1', course_name='Kiểm thử phần mềm02', credits='3')

    db.session.add(c)
    db.session.commit()
    db.session.refresh(c)
    return c

@pytest.fixture
def create_sestion(test_app,create_semester,create_course):
    sec = Section(section_code='KTPM02', lecturer='phuc',
                  room='P201', day_of_week='3', period_start=1, period_end=1,
                    max_capacity=50,
                  midterm=False,course_id=create_course.id,
                    semester_id=create_semester.id)

    db.session.add(sec)
    db.session.commit()
    db.session.refresh(sec)

    return sec

@pytest.fixture
def create_student_history(test_app,create_semester,create_course,create_student):
    history = StudentHistory(student_id=create_student.id,
                             course_id=create_course.id,semester_id=create_semester.id, poin=8.0)

    db.session.add(history)
    db.session.commit()
    db.session.refresh(history)

    return history
