from flask import Flask
from sqlalchemy import Column, Integer
from datetime import datetime
from __init__ import db, app
from enums import Role, StatusRegistration


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class Student(BaseModel):
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.Enum(Role), default=Role.STUDENT, nullable=False)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now())

    # dang_ky_list = db.relationship('DangKy', backref='sinh_vien', lazy=True)
    # lich_su_list = db.relationship('LichSuHocTap', backref='sinh_vien', lazy=True


def __str__(self):
    return self.name


class Course(BaseModel):
    course_code = db.Column(db.String(20), unique=True, nullable=False)
    course_name = db.Column(db.String(150), nullable=False)
    credits = db.Column(db.Integer, nullable=False)


def __str__(self):
    return self.course_name


class Semester(BaseModel):
    name = db.Column(db.String(50), unique=True, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    registration_deadline = db.Column(db.DateTime, nullable=False)


def __str__(self):
    return self.name


class Section(BaseModel):
    section_code = db.Column(db.String(30), unique=True, nullable=False)
    lecturer = db.Column(db.String(100), nullable=False)
    room = db.Column(db.String(20), nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)  # 2=Monday … 8=Sunday
    period_start = db.Column(db.Integer, nullable=False)  # 1-15
    period_end = db.Column(db.Integer, nullable=False)  # 1-15
    max_capacity = db.Column(db.Integer, default=50, nullable=False)
    midterm = db.Column(db.Boolean, default=False)

    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    semester_id = db.Column(db.Integer, db.ForeignKey('semester.id'), nullable=False)

    registrations = db.relationship('Registration', backref='section', lazy=True)

    def __str__(self):
        return self.section_code


class Registration(BaseModel):
    status = db.Column(db.Enum(StatusRegistration), default=StatusRegistration.REGISTRATION, nullable=False)
    registration_time = db.Column(db.DateTime, default=datetime.now)
    cancel_time = db.Column(db.DateTime, nullable=True)

    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('student_id', 'section_id', name='uq_sinhvien_lophocphan'),
    )

    def __str__(self):
        return self.id


class StudentHistory(BaseModel):
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    semester_id = db.Column(db.Integer, db.ForeignKey('semester.id'), nullable=False)
    poin = db.Column(db.Float, nullable=True)

    __table_args__ = (
        db.UniqueConstraint('student_id', 'course_id', 'semester_id', name='uq_sinhvien_khoahoc_hocky'),
    )

    def str(self):
        return self.id


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        import hashlib

        s = Student(
            student_id='2351050135',
            name='Phúc',
            email='2351050135phuc@gmail.com',
            password=str(hashlib.md5("123456".encode('utf-8')).hexdigest()),
            role=Role.SINH_VIEN,
            active=True,
            created_at=datetime.now()
        )
        db.session.add(s)
        db.session.commit()

        c=Course(course_code='KTPM1',course_name='Kiểm thử phần mềm02',credits='3')
        db.session.add(c)
        db.session.commit()

        se=Semester(name="Học kỳ 3",start_date=datetime.now(),
                    end_date=datetime(2026,11,21),
                    registration_deadline=datetime.now())
        db.session.add(se)
        db.session.commit()

        sec=Section(section_code='KTPM02',lecturer='Dương Hữu Thành',
                    room='P201',day_of_week='3',period_start=1,period_end=1,
                    max_capacity=50,
                    midterm=False,course_id=c.id,semester_id=se.id)
        db.session.add(sec)
        db.session.commit()

        r=Registration(status=StatusRegister.DANG_KY,registration_time=datetime.now(),
                       cancel_time=datetime.now(),student_id='1',section_id=sec.id,)

        db.session.add(r)
        db.session.commit()

        student = StudentHistory(student_id='1', course_id=c.id, semester_id=sec.id)
        db.session.add(student)
        db.session.commit()