from flask import session, flash, redirect, url_for
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from models import *
from flask_admin import Admin
from __init__ import db,app

admin = Admin(app=app,name='CourseApp Admin')


class AuthenticatedModelView(ModelView):
    def is_accessible(self)->bool:
        return current_user.is_authenticated and current_user.role == Role.ADMIN


class StudentView(AuthenticatedModelView):
    can_export = True
    can_create = False
    column_searchable_list = ['student_id', 'name', 'email']
    column_filters         = ['role', 'active']
    column_list = [
        'student_id', 'name', 'email', 'role', 'active', 'created_at'
    ]
    column_labels = {
        'student_id' : 'MSSV',
        'name'  : 'Họ tên',
        'email'      : 'Email',
        'role'       : 'Vai trò',
        'active'     : 'Hoạt động',
        'created_at' : 'Ngày tạo'
    }
    form_excluded_columns = ['password']


class CourseView(AuthenticatedModelView):
    can_export = True
    column_searchable_list = ['course_code', 'course_name']
    column_list = ['course_code', 'course_name', 'credits', 'prerequisites']
    column_labels = {
        'course_code' : 'Mã môn',
        'course_name' : 'Tên môn học',
        'credits'     : 'Tín chỉ',
        'prerequisites': 'Môn tiên quyết'
    }
    form_excluded_columns = ['sections', 'history_records', 'prereqs', 'required_by']



class SemesterView(AuthenticatedModelView):
    can_export = True
    column_list = [
        'name', 'start_date', 'end_date', 'registration_deadline'
    ]
    column_labels = {
        'name'                  : 'Tên học kỳ',
        'start_date'            : 'Ngày bắt đầu',
        'end_date'              : 'Ngày kết thúc',
        'registration_deadline' : 'Hạn đăng ký'
    }
    form_excluded_columns = ['sections', 'history_records']



class SectionView(AuthenticatedModelView):
    can_export = True
    column_searchable_list = ['section_code', 'lecturer', 'room']

    column_list = [
        'section_code', 'course', 'semester', 'lecturer',
        'room', 'day_of_week', 'period_start', 'period_end', 'max_capacity'
    ]
    column_labels = {
        'section_code' : 'Mã lớp',
        'course'       : 'Môn học',
        'semester'     : 'Học kỳ',
        'lecturer'     : 'Giảng viên',
        'room'         : 'Phòng',
        'day_of_week'  : 'Thứ',
        'period_start' : 'Tiết bắt đầu',
        'period_end'   : 'Tiết kết thúc',
        'max_capacity' : 'Sĩ số tối đa',
    }

    form_columns = [
        'section_code', 'course', 'semester', 'lecturer',
        'room', 'day_of_week', 'period_start', 'period_end', 'max_capacity'
    ]

    column_filters = ['course', 'semester']


class RegistrationView(AuthenticatedModelView):
    can_export  = True
    can_create  = False   # Admin không tự tạo đăng ký
    can_edit    = False   # Chỉ xem
    column_searchable_list = ['student_id']
    column_filters         = ['status', 'section_id']
    column_list = [
        'student_id', 'section', 'status', 'registered_time', 'cancel_time'
    ]
    column_labels = {
        'student_id'       : 'Sinh viên',
        'section_id'       : 'Lớp học phần',
        'status'        : 'Trạng thái',
        'registered_time' : 'Ngày đăng ký',
        'cancel_time'  : 'Ngày huỷ'
    }


class StudentHistoryView(AuthenticatedModelView):
    can_export = True
    column_list = [
        'student', 'course', 'semester', 'poin'
    ]
    column_labels = {
        'student'     : 'Sinh viên',
        'course'      : 'Môn học',
        'semester'    : 'Học kỳ',
        'poin' : 'Điểm cuối kỳ'
    }
    column_searchable_list = ['student_id']



admin.add_view(StudentView        (Student,         db.session, name='Sinh viên'))
admin.add_view(CourseView         (Course,          db.session, name='Môn học'))
admin.add_view(SemesterView       (Semester,        db.session, name='Học kỳ'))
admin.add_view(SectionView        (Section,         db.session, name='Lớp học phần'))
admin.add_view(RegistrationView   (Registration,    db.session, name='Đăng ký'))
admin.add_view(StudentHistoryView(StudentHistory, db.session, name='Lịch sử học tập'))