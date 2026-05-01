from models import *

def load_student_by_id(id):
    return Student.query.get(id)