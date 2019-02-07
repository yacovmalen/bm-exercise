"""
Data Models for each of the entities available
"""
import json

from cerberus import Validator
from werkzeug.datastructures import MultiDict

from Resources.Errors import BadRequestError


class DataModelBase(object):
    def __init__(self, **kwargs):
        self.entity = self.create_entity(**kwargs)
        self.entity = self._drop_none_values(self.entity)

        self.validator = Validator(ignore_none_values=True)
        self.validate_data(self.entity)

    def validate_data(self, data):
        is_valid = self.validator.validate(data, self.schema)

        if not is_valid:
            raise BadRequestError(self.validator.errors)
        else:
            return is_valid

    def create_entity(self, **kwargs):
        return NotImplementedError('create_entity method is not implemented')

    def _drop_none_values(self, kwargs):
        return {k:v for k,v in kwargs.items() if v is not None}

    @property
    def schema(self):
        return AttributeError('Schema property is not defined')


class DataModelStudent(DataModelBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def create_entity(self, _id, first_name, last_name, email):
        return {
            "entity_id": _id,
            "first_name": first_name,
            "last_name": last_name,
            "email": email
        }

    @property
    def schema(self):
        return {
            "entity_id": {"type": "integer"},
            "first_name": {"type": "string", "empty": False, "dependencies": "last_name"},
            "last_name": {"type": "string", "empty": False, "dependencies": "first_name"},
            "email": {"type": "string", "regex": "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"}
        }

    def __repr__(self):
        return json.dumps(self.entity)

    def __dict__(self):
        return self.entity


class DataModelTeacher(DataModelBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def create_entity(self, _id, first_name, last_name, email):
        return {
            "entity_id": _id,
            "first_name": first_name,
            "last_name": last_name,
            "email": email
        }

    @property
    def schema(self):
        return {
            "entity_id": {"type": "integer"},
            "first_name": {"type": "string", "empty": False, "dependencies": "last_name"},
            "last_name": {"type": "string", "empty": False, "dependencies": "first_name"},
            "email": {"type": "string", "regex": "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"}
        }

    def __repr__(self):
        return json.dumps(self.entity)

    def __dict__(self):
        return self.entity


class DataModelCourse(DataModelBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def create_entity(self, _id, name=None, student_ids=None, teacher_id=None, remove_student_ids=None):
        return {
            "entity_id": _id,
            "name": name,
            "student_entity_ids": [int(s_id) for s_id in student_ids.split(',')] if student_ids else None,
            "delete_student_entity_ids": [int(s_id) for s_id in remove_student_ids.split(',')] if remove_student_ids else None,
            "teacher_entity_id": int(teacher_id) if teacher_id else None
        }

    @property
    def schema(self):
        return {
            "entity_id": {"type": "integer"},
            "name": {"type": "string"},
            "student_entity_ids": {"type": "list", "schema": {"type": "integer"}},
            "delete_student_entity_ids": {"type": "list", "schema": {"type": "integer"}},
            "teacher_entity_id": {"type": "integer"}
        }

    def __repr__(self):
        return json.dumps(self.entity)

    def __dict__(self):
        return self.entity


class DataModelGrade(DataModelBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def create_entity(self, _id, course_id, grade):
        return {
            "course_entity_id": course_id,
            "student_entity_id": _id,
            "grade": grade
        }

    @property
    def schema(self):
        return {
            "course_entity_id": {"type": "integer"},
            "student_entity_id": {"type": "integer"},
            "grade": {"type": "integer"}
        }

    def __repr__(self):
        return json.dumps(self.entity)

    def __dict__(self):
        return self.entity
