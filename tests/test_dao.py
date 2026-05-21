from eapp.dao import load_student_by_id
from tests.test_base import create_student,test_app,test_session

def test_student(test_app,create_student):
    student_id = create_student.id
    result = load_student_by_id(student_id)

    assert result is not None
    assert result.id == student_id
    assert result.name == 'Phúc'
