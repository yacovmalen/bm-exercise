from flask import make_response, jsonify
from flask_restful import Resource

from Utils.Authentication import is_authenticated


class TeacherMaxStudents(Resource):
    decorators = [is_authenticated]

    def __init__(self, **kwargs):
        self.student_db = kwargs['db_conn'].connectors['student']
        self.teacher_db = kwargs['db_conn'].connectors['teacher']
        self.course_db = kwargs['db_conn'].connectors['course']
        self.grade_db = kwargs['db_conn'].connectors['grade']

    def get(self):
        course_sizes = self.course_db.get_course_sizes()
        return make_response(jsonify(max(course_sizes, key=lambda item: item['number_of_students'])), 200)


class StudentHighestAvg(Resource):
    def __init__(self, **kwargs):
        self.student_db = kwargs['db_conn'].connectors['student']
        self.teacher_db = kwargs['db_conn'].connectors['teacher']
        self.course_db = kwargs['db_conn'].connectors['course']
        self.grade_db = kwargs['db_conn'].connectors['grade']

    def get(self):
        grade_avgs = self.grade_db.get_highest_avg_student()
        smartest_student = max(grade_avgs, key=lambda item: item['highest_avg'])
        student_obj = self.student_db.get_one_or_all_entities({'entity_id': smartest_student['_id']})
        smartest_student.update(student_obj[0])
        del smartest_student['_id']
        return make_response(jsonify(smartest_student), 200)


class CourseEasiest(Resource):
    def __init__(self, **kwargs):
        self.student_db = kwargs['db_conn'].connectors['student']
        self.teacher_db = kwargs['db_conn'].connectors['teacher']
        self.course_db = kwargs['db_conn'].connectors['course']
        self.grade_db = kwargs['db_conn'].connectors['grade']

    def get(self):
        grade_avgs = self.grade_db.get_lowest_avg_course()
        easiest_class = min(grade_avgs, key=lambda item: item['lowest_avg'])
        course_obj = self.course_db.get_one_or_all_entities({'entity_id': easiest_class['_id']})
        easiest_class.update(course_obj[0])
        del easiest_class['_id']
        return make_response(jsonify(easiest_class), 200)
