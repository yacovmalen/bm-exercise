"""
Teacher Resources:
    1. Create new teacher - return 'EntityAlreadyExists' error
    2. Delete teacher account - return 'EntityNotFound' error
    3. Update teacher data - return 'EntityNotFound' error
    4. Get teacher from database - return 'EntityNotFound' error
"""
from flask import make_response, jsonify
from flask_restful import Resource

from Resources.RequestParams import ReqParse
from Utils.Authentication import is_authenticated
from Utils.DataModels import DataModelTeacher


class Teacher(Resource):
    decorators = [is_authenticated]

    def __init__(self, **kwargs):
        self.db = kwargs['db_conn'].connectors['teacher']
        self.args_parser = ReqParse.person()

    def get(self, entity_id=None):
        args = self.args_parser.parse_args()
        model = DataModelTeacher(_id=entity_id, **args)  # Data validation

        return make_response(jsonify(self.db.get_one_or_all_entities(model.__dict__())), 200)

    def post(self, entity_id=None):
        args = self.args_parser.parse_args()
        model = DataModelTeacher(_id=entity_id, **args)  # Data validation

        return make_response(jsonify(self.db.create_entity(model.__dict__())), 201)

    def put(self, entity_id=None):
        if not entity_id:
            return make_response('Missing entity_id - Method not implemented', 501)

        args = self.args_parser.parse_args()
        model = DataModelTeacher(_id=entity_id, **args)  # Data validation

        return make_response(jsonify(self.db.update_entity(model.__dict__())), 204)

    def delete(self, entity_id=None):
        if not entity_id:
            return make_response('Missing entity_id - Method not implemented', 501)

        args = self.args_parser.parse_args()
        model = DataModelTeacher(_id=entity_id, **args)  # Data validation

        return make_response(jsonify(self.db.delete_entity(model.__dict__())), 204)
