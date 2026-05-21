from datetime import datetime, timedelta

import pytest
from eapp import dao,db
from eapp.enums import StatusRegistration
from eapp.models import Student, Registration, StudentHistory, Course, Section
from tests.test_base import create_student,test_app,test_session,create_course,create_sestion,create_semester,create_student_history
from eapp.dao import register_course

def test_register_course_success(create_student,create_course,create_sestion,create_semester):
    create_sestion.course_id = create_course.id
    create_sestion.semester_id = create_semester.id
    db.session.commit()

    success, message = register_course(
        create_student.id,
        create_sestion.id
    )

    print(message)
    assert success is True
    assert message == "Đăng ký thành công!"

    reg = Registration.query.filter_by(
        student_id=create_student.id,
        section_id=create_sestion.id
    ).first()

    assert reg is not None
    assert reg.status == StatusRegistration.REGISTRATION

def test_register_course_already_completed(create_student,create_course,
                                           create_sestion,create_semester,create_student_history):
    create_sestion.course_id = create_course.id
    create_sestion.semester_id = create_semester.id

    success, message = register_course(
        create_student.id,
        create_sestion.id
    )

    assert success is False
    assert message == "Bạn đã hoàn thành môn này rồi!"

def test_register_course_max_25_credits(create_student, create_semester):
    for i in range(5):
        course = Course(course_code=f"KTPM{i}",course_name="Test",credits=5)
        db.session.add(course)
        db.session.flush()

        section = Section(section_code=f"S{i}",lecturer="A",room="P201",day_of_week=1,
            period_start=1,period_end=2,max_capacity=50,midterm=False,course_id=course.id,
            semester_id=create_semester.id)
        db.session.add(section)
        db.session.flush()

        reg = Registration(
            student_id=create_student.id,
            section_id=section.id,
            status=StatusRegistration.REGISTRATION
        )
        db.session.add(reg)

    db.session.commit()

    new_course = Course(
        course_code="OVER",
        course_name="Over",
        credits=3
    )
    db.session.add(new_course)
    db.session.flush()

    new_section = Section(section_code="OVER_SEC",lecturer="B",room="P202",day_of_week=2,period_start=3,
        period_end=4,max_capacity=50,midterm=False,course_id=new_course.id,semester_id=create_semester.id)
    db.session.add(new_section)
    db.session.commit()

    success, message = register_course(create_student.id, new_section.id)

    assert success is False
    assert message == "Đăng ký tối đa 25 tín chỉ!"


def test_register_course_full_capacity(create_student,create_course,create_sestion,create_semester):
    create_sestion.course_id = create_course.id
    create_sestion.semester_id = create_semester.id
    create_sestion.max_capacity = 1

    db.session.commit()

    student2 = Student(student_id='2351050999',name='Student 2',
        email='student2@gmail.com',password='123456',role='STUDENT',active=True
    )

    db.session.add(student2)
    db.session.commit()

    reg = Registration(student_id=student2.id,section_id=create_sestion.id,
        status=StatusRegistration.REGISTRATION
    )

    db.session.add(reg)
    db.session.commit()

    success, message = register_course(
        create_student.id,
        create_sestion.id
    )

    assert success is False
    assert message == "Lớp đã đủ số lượng sinh viên!"

def test_register_course_after_deadline(create_student,create_course,create_sestion,create_semester):
    create_sestion.course_id = create_course.id
    create_sestion.semester_id = create_semester.id

    create_semester.registration_deadline = datetime.now() - timedelta(days=1)

    db.session.commit()

    success, message = register_course(
        create_student.id,
        create_sestion.id
    )

    assert success is False
    assert message == "Đã hết hạn đăng ký!"

def test_register_course_without_prerequisite(create_student,create_course,create_sestion,create_semester):
    prerequisite_course = Course(
        course_code='CTDL',
        course_name='Cấu trúc dữ liệu',
        credits=3
    )

    db.session.add(prerequisite_course)
    db.session.commit()

    create_course.prerequisites.append(prerequisite_course)

    create_sestion.course_id = create_course.id
    create_sestion.semester_id = create_semester.id

    db.session.commit()

    success, message = register_course(
        create_student.id,
        create_sestion.id
    )

    assert success is False
    assert message == (
        f"Chưa hoàn thành môn tiên quyết: "
        f"'{prerequisite_course.course_name}'!"
    )

def test_cannot_register_conflict_schedule(create_student,create_course,create_semester,create_sestion):
    create_sestion.course_id = create_course.id
    create_sestion.semester_id = create_semester.id
    create_sestion.room = "P201"
    create_sestion.day_of_week = 3
    create_sestion.period_start = 1
    create_sestion.period_end = 3

    db.session.commit()

    reg = Registration(
        student_id=create_student.id,
        section_id=create_sestion.id,
        status=StatusRegistration.REGISTRATION
    )
    db.session.add(reg)
    db.session.commit()

    section_b = Section(
        section_code="KTPM_B",
        lecturer="GV B",
        room="P202",
        day_of_week=3,
        period_start=2,
        period_end=4,
        max_capacity=50,
        course_id=create_course.id,
        semester_id=create_semester.id
    )

    db.session.add(section_b)
    db.session.commit()

    success, message = register_course(
        create_student.id,
        section_b.id
    )

    assert success is False
    assert "Trùng lịch" in message