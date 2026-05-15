from models import *
from datetime import datetime, date, timedelta
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
    existing_active = Registration.query.filter_by(
        student_id=student_id,
        section_id=section_id,
        status=StatusRegistration.REGISTRATION
    ).first()

    section = Section.query.get(section_id)
    semester = section.semester
    course = section.course

    if datetime.now() > semester.registration_deadline:
        return False, ("Đã hết hạn đăng ký!")


    da_hoc = StudentHistory.query.filter(
        StudentHistory.student_id == student_id,
        StudentHistory.course_id == course.id,
        StudentHistory.poin != None,
        StudentHistory.poin >= 5.0
    ).first()
    if da_hoc:
        return False, "Bạn đã hoàn thành môn này rồi!"

    if existing_active:
        return False, "Bạn đã đăng ký lớp này rồi!"

    so_dang_ky = Registration.query.filter_by(
        section_id=section_id,
        status=StatusRegistration.REGISTRATION
    ).count()
    if so_dang_ky >= section.max_capacity:
        return False, "Lớp đã đủ số lượng sinh viên!"

    dang_hoc = Registration.query.join(Section).filter(
        Registration.student_id == student_id,
        Registration.status == StatusRegistration.REGISTRATION,
        Section.semester_id == semester.id
    ).all()

    for reg in dang_hoc:
        s = reg.section
        if s.day_of_week == section.day_of_week:
            if not (section.period_end < s.period_start or
                    section.period_start > s.period_end):
                return False, (f"Trùng lịch với môn '{s.course}' "
                               f"(Thứ {s.day_of_week}, "
                               f"Tiết {s.period_start}-{s.period_end})!")

    tong_tc = sum(r.section.course.credits for r in dang_hoc)
    if tong_tc + course.credits > 25:
        return False, "Đăng ký tối đa 25 tín chỉ!"

    # if tong_tc+course.credits <12:
    #     return False,"Đăng ký tối thiểu 12 tín chỉ!"


    section = Section.query.get(section_id)
    so_dang_ky = Registration.query.filter_by(
        section_id=section_id,
        status=StatusRegistration.REGISTRATION
    ).count()
    if so_dang_ky >= section.max_capacity:
        return False, "Lớp đã đủ số lượng sinh viên!"

    existing_cancelled = Registration.query.filter_by(
        student_id=student_id,
        section_id=section_id,
        status=StatusRegistration.CANCELED
    ).first()

    if existing_cancelled:
        existing_cancelled.status            = StatusRegistration.REGISTRATION
        existing_cancelled.registration_time = datetime.now()
        existing_cancelled.cancel_time       = None
    else:
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

    section = reg.section
    semester = section.semester

    if section.midterm:
        return False, f"Không thể huỷ môn '{section.course}' vì đã thi giữa kỳ!"

    ngay_het_han_huy = semester.start_date + timedelta(weeks=2)
    if date.today() > ngay_het_han_huy:
        return False, (
            f"Đã quá thời hạn huỷ! "
        )

    dang_hoc = Registration.query.join(Section).filter(
        Registration.student_id == student_id,
        Registration.status == StatusRegistration.REGISTRATION,
        Section.semester_id == semester.id
    ).all()

    tong_tc_hien_tai = sum(r.section.course.credits for r in dang_hoc)
    tc_mon_huy = section.course.credits
    tc_sau_khi_huy = tong_tc_hien_tai - tc_mon_huy

    if tc_sau_khi_huy < 12:
        return False, (
            f"Không thể huỷ! Đăng ký tối thiểu 12 tín chỉ"
        )

    reg.status = StatusRegistration.CANCELED
    reg.cancel_time = datetime.now()
    db.session.commit()
    return True, "Huỷ đăng ký thành công!"

def get_all_semesters():
    return Semester.query.all()

def get_student_history(student_id):
    return StudentHistory.query.filter_by(student_id=student_id).all()