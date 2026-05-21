import hashlib
from datetime import datetime

import pytest

from eapp.models import Student
from eapp.dao import register
from tests.test_base import create_student,test_app,test_session
from eapp.enums import Role

def test_register_success(test_session):
    register(name='phuc', email='hoanghongphuc@gmail.com', student_id='2351050135',
        password='123456')

    s=Student.query.filter(Student.email=='hoanghongphuc@gmail.com').first()

    assert s
    assert s.name == 'phuc'
    assert s.password == str(hashlib.md5('123456'.encode('utf-8')).hexdigest())

def test_existing_studentid(test_session):
    register(name='phuc', email='hoanghongphuc1@gmail.com', student_id='2351050136',
             password='123456')

    with pytest.raises(ValueError):
        register(name='phuc', email='hoanghongphuc1@gmail.com', student_id='2351050136',
                 password='123456')