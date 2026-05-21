from datetime import datetime, timedelta

from eapp import db
from eapp.dao import cancel_course
from eapp.enums import StatusRegistration
from eapp.models import Registration
from tests.test_base import create_student,test_app,test_session,create_course,create_sestion,create_semester,create_student_history


def test_cancel_course_not_owner(create_student,create_course,create_sestion,create_semester):

    create_sestion.course_id = create_course.id
    create_sestion.semester_id = create_semester.id

    db.session.commit()

    reg = Registration(student_id=999,section_id=create_sestion.id,status=StatusRegistration.REGISTRATION
    )

    db.session.add(reg)
    db.session.commit()

    success, message = cancel_course(
        create_student.id,
        reg.id
    )

    assert success is False
    assert message == "Không tìm thấy đăng ký!"

def test_cancel_course_after_2_weeks(create_student,create_course,create_sestion,create_semester):
        create_sestion.course_id = create_course.id
        create_sestion.semester_id = create_semester.id

        create_semester.start_date = datetime.now().date() - timedelta(days=15)

        db.session.commit()

        reg = Registration(student_id=create_student.id,section_id=create_sestion.id,status=StatusRegistration.REGISTRATION
        )

        db.session.add(reg)
        db.session.commit()

        success, message = cancel_course(
            create_student.id,
            reg.id
        )

        assert success is False
        assert "Đã quá thời hạn huỷ!" in message

def test_cancel_course_after_midterm(create_student,create_course,create_sestion,create_semester):
    create_sestion.course_id = create_course.id
    create_sestion.semester_id = create_semester.id

    db.session.commit()

    reg = Registration(student_id=create_student.id,section_id=create_sestion.id,status=StatusRegistration.REGISTRATION
    )

    db.session.add(reg)
    db.session.commit()

    create_sestion.midterm = True
    db.session.commit()

    success, message = cancel_course(
        create_student.id,
        reg.id
    )

    assert success is False
    assert "Không thể huỷ" in message
    assert "giữa kỳ" in message