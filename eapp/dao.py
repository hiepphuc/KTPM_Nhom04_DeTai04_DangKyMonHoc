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

def get_all_sections():
    return Section.query.all()

def get_sections_by_semester(semester_id):
    return Section.query.filter_by(semester_id=semester_id).all()

def get_registered_sections(student_id):
    return Registration.query.filter_by(
        student_id=student_id,
        status=StatusRegistration.REGISTRATION
    ).all()

def register_course(student_id, section_id):
    existing = Registration.query.filter_by(
        student_id=student_id,
        section_id=section_id
    ).first()
    if existing:
        return False, "Bạn đã đăng ký lớp này rồi!"

    section = Section.query.get(section_id)
    registrations = Registration.query.filter_by(
        section_id=section_id,
        status=StatusRegistration.REGISTRATION
    ).count()
    if registrations >= section.max_capacity:
        return False, "Lớp đã đủ số lượng sinh viên!"

    reg = Registration(
        student_id=student_id,
        section_id=section_id,
        status=StatusRegistration.REGISTRATION
    )
    db.session.add(reg)
    db.session.commit()
    return True, "Đăng ký thành công!"

def cancel_course(student_id, registration_id):
    reg = Registration.query.filter_by(
        id=registration_id,
        student_id=student_id
    ).first()
    if not reg:
        return False, "Không tìm thấy đăng ký!"

    reg.status = StatusRegistration.CANCELED
    reg.cancel_time = datetime.now()
    db.session.commit()
    return True, "Huỷ đăng ký thành công!"

def get_all_semesters():
    return Semester.query.all()