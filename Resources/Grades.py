from flask import make_response, jsonify
from flask_restful import Resource

from Resources.Errors import BadRequestError
from Utils.Authentication import is_authenticated
from Utils.DataModels import DataModelGrade


class Grade(Resource):
    decorators = [is_authenticated]

    def __init__(self, **kwargs):
        self.student_db = kwargs['db_conn'].connectors['student']
        self.grade_db = kwargs['db_conn'].connectors['grade']
        self.course_db = kwargs['db_conn'].connectors['course']

    def get(self, student_entity_id=None, course_entity_id=None, grade=None):
        if not student_entity_id and not course_entity_id:
            return make_response('Missing entity_id - Method not implemented', 501)

        if grade:
            raise BadRequestError('Grade should not be included in GET request')

        model = DataModelGrade(_id=student_entity_id, course_id=course_entity_id, grade=grade)  # Data validation

        return make_response(jsonify(self.grade_db.get_one_or_all_entities(model.__dict__())), 200)

    def post(self, student_entity_id=None, course_entity_id=None, grade=None):
        if not student_entity_id and not course_entity_id and not grade:
            return make_response('Missing part of api path - Method not implemented', 501)

        model = DataModelGrade(_id=student_entity_id, course_id=course_entity_id, grade=grade)  # Data validation

        # Check if student entity exists
        if student_entity_id:
            self.student_db.get_one_or_all_entities({"entity_id": model.entity['student_entity_id']})

        # Check if course entity exists
        if course_entity_id:
            self.course_db.get_one_or_all_entities({"entity_id": model.entity['course_entity_id']})

        return make_response(jsonify(self.grade_db.create_entity(model.__dict__())), 201)

    def put(self, student_entity_id=None, course_entity_id=None, grade=None):
        if not student_entity_id and not course_entity_id and not grade:
            return make_response('Missing part of api path - Method not implemented', 501)

        model = DataModelGrade(_id=student_entity_id, course_id=course_entity_id, grade=grade)  # Data validation

        return make_response(jsonify(self.grade_db.update_entity(model.__dict__())), 204)

    def delete(self, student_entity_id=None, course_entity_id=None, grade=None):
        if not student_entity_id and not course_entity_id:
            return make_response('Missing student entity_id - Method not implemented', 501)

        model = DataModelGrade(_id=student_entity_id, course_id=course_entity_id, grade=grade)  # Data validation

        return make_response(jsonify(self.grade_db.delete_grade(model.__dict__())), 204)
