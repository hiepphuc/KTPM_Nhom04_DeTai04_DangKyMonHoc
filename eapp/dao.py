from eapp.models import *
from datetime import datetime, date, timedelta
import hashlib


def load_student_by_id(id):
    return Student.query.get(int(id))

def login(student_id, password):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    return Student.query.filter(
        Student.student_id == student_id.strip(),
        Student.password   == password
    ).first()

def register(name, email, password, student_id):
    if Student.query.filter_by(student_id=student_id).first():
        raise ValueError("Mã số sinh viên đã tồn tại!")

    if Student.query.filter_by(email=email).first():
        raise ValueError("Email đã được sử dụng!")


    s = Student(
        name=name, email=email, student_id=student_id,
        role=Role.STUDENT, active=True, created_at=datetime.now(),
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
    section  = Section.query.get(section_id)
    semester = section.semester
    course   = section.course

    if datetime.now() > semester.registration_deadline:
        return False, "Đã hết hạn đăng ký!"

    da_hoc = StudentHistory.query.filter(
        StudentHistory.student_id == student_id,
        StudentHistory.course_id  == course.id,
        StudentHistory.poin       != None,
        StudentHistory.poin       >= 5.0
    ).first()
    if da_hoc:
        return False, "Bạn đã hoàn thành môn này rồi!"

    for mon_tq in course.prerequisites:
        da_pass = StudentHistory.query.filter(
            StudentHistory.student_id == student_id,
            StudentHistory.course_id == mon_tq.id,
            StudentHistory.poin != None,
            StudentHistory.poin >= 5.0
        ).first()
        if not da_pass:
            return False, f"Chưa hoàn thành môn tiên quyết: '{mon_tq.course_name}'!"

    existing_active = Registration.query.filter_by(
        student_id=student_id,
        section_id=section_id,
        status=StatusRegistration.REGISTRATION
    ).first()
    
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
        Registration.status     == StatusRegistration.REGISTRATION,
        Section.semester_id     == semester.id
    ).all()

    for reg in dang_hoc:
        s = reg.section
        if int(s.day_of_week) == int(section.day_of_week):
            if not (int(section.period_end)   < int(s.period_start) or
                    int(section.period_start) > int(s.period_end)):
                return False, (
                    f"Trùng lịch với môn '{s.course}' "
                )

    tong_tc = sum(r.section.course.credits for r in dang_hoc)
    if tong_tc + course.credits > 25:
        return False, "Đăng ký tối đa 25 tín chỉ!"

    canh_bao = None

    if tong_tc + course.credits < 12:
        canh_bao = (
            f"Đăng ký thành công! "
            f"Cần đăng ký tối thiểu 12 tín chỉ."
        )

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
        db.session.add(Registration(
            student_id=student_id,
            section_id=section_id,
            status=StatusRegistration.REGISTRATION
        ))

    db.session.commit()
    if canh_bao:
        return True, canh_bao

    return True, "Đăng ký thành công!"


def cancel_course(student_id, registration_id):
    reg = Registration.query.filter_by(
        id=registration_id,
        student_id=student_id
    ).first()
    if not reg:
        return False, "Không tìm thấy đăng ký!"

    section  = reg.section
    semester = section.semester

    if section.midterm:
        return False, f"Không thể huỷ môn '{section.course}' vì đã thi giữa kỳ!"

    ngay_het_han_huy = semester.start_date + timedelta(weeks=2)
    if date.today() > ngay_het_han_huy:
        return False, f"Đã quá thời hạn huỷ! Chỉ được huỷ trước {ngay_het_han_huy.strftime('%d/%m/%Y')}."

    dang_hoc = Registration.query.join(Section).filter(
        Registration.student_id == student_id,
        Registration.status     == StatusRegistration.REGISTRATION,
        Section.semester_id     == semester.id
    ).all()
    tong_tc        = sum(r.section.course.credits for r in dang_hoc)
    tc_sau_khi_huy = tong_tc - section.course.credits

    if tc_sau_khi_huy < 12:
        return False, f"Không thể huỷ! Sau khi huỷ chỉ còn {tc_sau_khi_huy} TC, thấp hơn 12 TC tối thiểu."

    reg.status      = StatusRegistration.CANCELED
    reg.cancel_time = datetime.now()
    db.session.commit()
    return True, "Huỷ đăng ký thành công!"

def get_all_semesters():
    return Semester.query.all()

def get_student_history(student_id):
    history    = StudentHistory.query.filter_by(student_id=student_id).all()
    registered = Registration.query.filter_by(
        student_id=student_id,
        status=StatusRegistration.REGISTRATION
    ).all()
    return history, registered