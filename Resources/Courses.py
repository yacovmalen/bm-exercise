"""
Course Resources:
    1. Create new course - return 'EntityAlreadyExists' error
    2. Delete course account - return 'EntityNotFound' error
    3. Update course data - return 'EntityNotFound' error
    4. Get course from database - return 'EntityNotFound' error
"""
import json

from bson.json_util import dumps, loads
from flask import make_response, jsonify
from flask_restful import Resource

from Resources.RequestParams import ReqParse
from Utils.Authentication import is_authenticated
from Utils.DataModels import DataModelCourse


class Course(Resource):
    decorators = [is_authenticated]

    def __init__(self, **kwargs):
        self.student_db = kwargs['db_conn'].connectors['student']
        self.teacher_db = kwargs['db_conn'].connectors['teacher']
        self.course_db = kwargs['db_conn'].connectors['course']
        self.args_parser = ReqParse.course()

    def get(self, entity_id=None):
        args = self.args_parser.parse_args()
        model = DataModelCourse(_id=entity_id, **args)  # Data validation

        return make_response(jsonify(self.course_db.get_one_or_all_entities(model.__dict__())), 200)

    def post(self, entity_id=None):
        args = self.args_parser.parse_args()
        model = DataModelCourse(_id=entity_id, **args)  # Data validation

        # Check if teacher entity exists
        self.teacher_db.get_one_or_all_entities({"entity_id": model.entity['teacher_entity_id']})

        # Check if students exists
        self.course_db.check_if_students_exist(self.student_db, model)

        return make_response(jsonify(self.course_db.create_entity(model.__dict__())), 201)

    def put(self, entity_id=None):
        result = None
        if not entity_id:
            return make_response('Missing entity_id - Method not implemented', 501)

        args = self.args_parser.parse_args()
        model = DataModelCourse(_id=entity_id, **args)  # Data validation

        if 'delete_student_entity_ids' in model.entity.keys():
            result = jsonify(self.course_db.remove_course_students(model))
            del model.entity['delete_student_entity_ids']

        if 'student_entity_ids' in model.entity.keys():
            self.course_db.check_if_students_exist(self.student_db, model)

            # Do not duplicated users in the array
            current_students = self.course_db.get_one_or_all_entities({'entity_id': model.entity['entity_id']})
            for s_id in model.entity['student_entity_ids']:
                if s_id in current_students[0]['student_entity_ids']:
                    model.entity['student_entity_ids'].remove(s_id)

            result = jsonify(self.course_db.add_course_students(model))

        return make_response(result, 204)

    def delete(self, entity_id=None):
        if not entity_id:
            return make_response('Missing entity_id - Method not implemented', 501)

        args = self.args_parser.parse_args()
        model = DataModelCourse(_id=entity_id, **args)  # Data validation

        return make_response(jsonify(self.course_db.delete_entity(model.__dict__())), 204)
