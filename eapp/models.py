from flask import Flask
from flask_login import UserMixin
from sqlalchemy import Column, Integer
from datetime import datetime
from eapp import db, app
from eapp.enums import Role, StatusRegistration


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)

class Student(BaseModel,UserMixin):
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.Enum(Role), default=Role.STUDENT, nullable=False)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    __table_args__ = {'extend_existing': True}

    def __str__(self):
        return self.name

prerequisite_table = db.Table('prerequisite',
    db.Column('course_id',       db.Integer, db.ForeignKey('course.id'), primary_key=True),
    db.Column('prerequisite_id', db.Integer, db.ForeignKey('course.id'), primary_key=True),
    extend_existing=True
)

class Course(BaseModel):
    course_code = db.Column(db.String(20), unique=True, nullable=False)
    course_name = db.Column(db.String(150), nullable=False)
    credits = db.Column(db.Integer, nullable=False)

    prerequisites = db.relationship(
        'Course',
        secondary=prerequisite_table,
        primaryjoin='Course.id == prerequisite.c.course_id',
        secondaryjoin='Course.id == prerequisite.c.prerequisite_id',
        backref='required_by'
    )

    __table_args__ = {'extend_existing': True}
    def __str__(self):
        return self.course_name


class Semester(BaseModel):
    name = db.Column(db.String(50), unique=True, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    registration_deadline = db.Column(db.DateTime, nullable=False)

    __table_args__ = {'extend_existing': True}
    def __str__(self):
        return self.name


class Section(BaseModel):
    section_code = db.Column(db.String(30), unique=True, nullable=False)
    lecturer = db.Column(db.String(100), nullable=False)
    room = db.Column(db.String(20), nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)
    period_start = db.Column(db.Integer, nullable=False)
    period_end = db.Column(db.Integer, nullable=False)
    max_capacity = db.Column(db.Integer, default=50, nullable=False)
    midterm = db.Column(db.Boolean, default=False)

    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    semester_id = db.Column(db.Integer, db.ForeignKey('semester.id'), nullable=False)

    course = db.relationship('Course', backref='sections')
    semester = db.relationship('Semester', backref='sections')

    registrations = db.relationship('Registration', backref='section', lazy=True)

    __table_args__ = {'extend_existing': True}
    def __str__(self):
        return self.section_code


class Registration(BaseModel):
    status = db.Column(db.Enum(StatusRegistration), default=StatusRegistration.REGISTRATION, nullable=False)
    registration_time = db.Column(db.DateTime, default=datetime.now)
    cancel_time = db.Column(db.DateTime, nullable=True)

    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'), nullable=False)

    student = db.relationship('Student', backref='registrations')
    __table_args__ = {'extend_existing': True}
    def __str__(self):
        return self.id


class StudentHistory(BaseModel):
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    semester_id = db.Column(db.Integer, db.ForeignKey('semester.id'), nullable=False)
    poin = db.Column(db.Float, nullable=True)

    course = db.relationship('Course', backref='history')
    semester = db.relationship('Semester', backref='history')

    student = db.relationship('Student', backref='history_records')
    __table_args__ = {'extend_existing': True}
    def __str__(self):
        return str(self.id)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        import hashlib

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

        c=Course(course_code='KTPM2',course_name='Kiểm thử phần mềm02',credits=3)
        db.session.add(c)
        db.session.commit()

        mon_tq = Course(course_code='KTPM3', course_name='Kiểm thử phần mềm 3', credits=3)
        db.session.add(mon_tq)
        db.session.commit()

        mon_chinh = Course(course_code='KTPM4', course_name='Kiểm thử phần mềm 4', credits=3)
        db.session.add(mon_chinh)
        db.session.flush()
        mon_tq = Course.query.filter_by(course_code='KTPM3').first()

        if mon_tq:
            mon_chinh.prerequisites.append(mon_tq)

        db.session.commit()

        se=Semester(name="Học kỳ 3",start_date=datetime.now(),
                    end_date=datetime(2026,11,21),
                    registration_deadline=datetime.now())
        db.session.add(se)
        db.session.commit()

        sec=Section(section_code='KTPM02',lecturer='phúc',
                    room='P201',day_of_week=3,period_start=1,period_end=1,
                    max_capacity=50,
                    midterm=False,course_id=c.id,semester_id=se.id)
        db.session.add(sec)
        db.session.commit()

        r=Registration(status=StatusRegistration.REGISTRATION,registration_time=datetime.now(),
                       cancel_time=datetime.now(),student_id='1',section_id=sec.id,)

        db.session.add(r)
        db.session.commit()

        student = StudentHistory(student_id='1', course_id=c.id, semester_id=sec.id)
        db.session.add(student)
        db.session.commit()

        student1=StudentHistory(student_id='1', course_id=mon_tq.id, semester_id=sec.id,poin=8)
        db.session.add(student1)
        db.session.commit()

        s = Student(
            student_id='2351050137',
            name='Phúc 1',
            email='2351050137phuc@gmail.com',
            password=str(hashlib.md5("123456".encode('utf-8')).hexdigest()),
            role=Role.ADMIN,
            active=True,
            created_at=datetime.now()
        )
        db.session.add(s)
        db.session.commit()