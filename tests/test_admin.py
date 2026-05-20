import hashlib
from datetime import datetime

import pytest
from pyexpat.errors import messages

from eapp.admin import SectionView
from eapp.enums import Role, StatusRegistration
from eapp.models import Student, Section, Registration
from eapp import db
from tests.test_base import create_student,test_app,test_session,create_course,create_semester,create_sestion

def create_admin(test_app):
    admin = Student(student_id='admin', name='Admin Test',email='admin@test.com',
        password=str(hashlib.md5('123456'.encode()).hexdigest()),
        role=Role.ADMIN, active=True, created_at=datetime.now()
    )
    db.session.add(admin)
    db.session.flush()
    db.session.refresh(admin)
    return admin

def test_admin_login(test_app):
    admin = create_admin(test_app)
    db.session.commit()

    assert admin.role == Role.ADMIN

def test_student_login(create_student):
    sv =create_student
    db.session.commit()

    assert sv.role != Role.ADMIN
    assert sv.role == Role.STUDENT

def section_max_capacity(create_semester):
    view = SectionView(Section, db.session)

    model = Section(section_code="KTPM",lecturer="phúc",room="P201",
        day_of_week=3,period_start=1,period_end=3,max_capacity=51
    )

    class FakeForm:
        semester = type("x", (), {"data": create_semester})()

    with pytest.raises(Exception):
        view.on_model_change(FakeForm(), model, True)

def test_section_max_capacity_valid(create_semester):
    view = SectionView(Section, db.session)

    model = Section(section_code="KTPM", lecturer="phúc", room="P201",
                    day_of_week=3, period_start=1, period_end=3, max_capacity=50
                    )

    class FakeForm:
        semester = type("x", (), {"data": create_semester})()

    view.on_model_change(FakeForm(), model, True)

def can_delete(section_id)->bool:
    count_student = Registration.query.filter_by(
        section_id=section_id,
        status=StatusRegistration.REGISTRATION
    ).count()
    return count_student == 0

def test_delete_no_student(test_app, create_sestion):
    result = can_delete(create_sestion.id)
    assert result is True

def test_delete_has_student(test_app, create_sestion, create_student):
    register = Registration(
        student_id=create_student.id,
        section_id=create_sestion.id,
        status=StatusRegistration.REGISTRATION,
        registration_time=datetime.now()
    )
    from eapp import db
    db.session.add(register)
    db.session.commit()

    result = can_delete(create_sestion.id)
    assert result is False