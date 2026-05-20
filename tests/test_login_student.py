from tests.test_base import create_student
from eapp import db,dao
import pytest
from tests.test_base import create_student,test_app,test_session


def test_login_success(create_student):
    result = dao.login('2351050135', '123456')

    assert result is not None
    assert result.student_id == '2351050135'

def test_login_failure(create_student):
    result = dao.login('2351050135', 'sai')
    assert result is None