"""
Mongo Connection Class - creates and maintains a connector mongo and utils to access and update the database
"""
import datetime

from bson.json_util import dumps, loads
from pymongo import MongoClient
from Resources.Errors import EntityAlreadyExistsError, DatabaseError, EntityNotFound


class MongoConnector(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client['school']
        self.connectors = {'student': StudentConnector(self.db),
                           'teacher': TeacherConnector(self.db),
                           'course': CourseConnector(self.db),
                           'grade': GradeConnector(self.db)}


class EntityConnector(object):
    def __init__(self, mongo_connection):
        self.conn = mongo_connection
        self.collection = None

    def create_entity(self, entity):
        if 'entity_id' not in entity or not entity['entity_id']:
            entity['entity_id'] = self.get_last_id() + 1
        elif self._is_exist(entity['entity_id']):
            raise EntityAlreadyExistsError('Entity already exists', None)

        response = self._insert_or_update(entity, upsert=True)

        if '_id' in response:
            del response['_id']

        return response

    def get_one_or_all_entities(self, entity):
        entity.update({'delete_date': {'$exists': False}})
        docs = self.collection.find(entity, {"_id": 0})

        if not docs or docs.count() == 0:
            raise EntityNotFound('No entity {} found'.format(entity), None)
        return list(docs)

    def delete_entity(self, entity, hard_delete=False):
        entity.update({'delete_date': datetime.datetime.utcnow()})
        return self.update_entity(entity)

    def update_entity(self, entity):
        response = self._insert_or_update(entity, upsert=False)

        if response == 'null' or not response:
            raise EntityNotFound('No entity {} found'.format(entity), None)

        return [res for res in response]

    def get_last_id(self):
        l_id = 0
        try:
            latest_id = self.collection.find().sort([('entity_id', -1)]).limit(1)
        except Exception as e:
            print(e)
            return 0
        for item in latest_id:
            l_id = item['entity_id']

        return l_id

    def _insert_or_update(self, entity, upsert=False):
        now = datetime.datetime.utcnow()
        entity.update({'last_update': now})

        return self.collection.find_and_modify(
            {'entity_id': entity['entity_id'], 'delete_date': {'$exists': False}},
            {
                '$set': entity,
                '$setOnInsert': {'creation_date': now}
            },
            upsert=upsert,
            new=True
        )

    def _hard_delete(self, query):
        try:
            return self.collection.remove(query)
        except Exception as e:
            print(e)
            raise DatabaseError('Database error', e)

    def _is_exist(self, entity_id):
        try:
            return self.collection.find_one({'entity_id': entity_id, 'delete_date': {'$exists': False}})
        except Exception as e:
            print(e)
            raise DatabaseError('Database error', e)


class StudentConnector(EntityConnector):
    def __init__(self, mongo_connection):
        super().__init__(mongo_connection)
        self.collection = self.conn['students']


class TeacherConnector(EntityConnector):
    def __init__(self, mongo_connection):
        super().__init__(mongo_connection)
        self.collection = self.conn['teachers']


class CourseConnector(EntityConnector):
    def __init__(self, mongo_connection):
        super().__init__(mongo_connection)
        self.collection = self.conn['courses']

    def add_course_students(self, model):
        add_students = {"$push": {"student_entity_ids": {"$each": model.entity["student_entity_ids"]}}}

        return self.collection.update(
            {'entity_id': model.entity['entity_id'], 'delete_date': {'$exists': False}},
            add_students
        )

    def remove_course_students(self, model):
        remove_students = {"$pull": {"student_entity_ids": {"$in": model.entity["delete_student_entity_ids"]}}}

        return self.collection.update(
            {'entity_id': model.entity['entity_id'], 'delete_date': {'$exists': False}},
            remove_students
        )

    @staticmethod
    def check_if_students_exist(student_db, model):
        # Check if students exists
        students = student_db.get_one_or_all_entities({"entity_id": {"$in": model.entity['student_entity_ids']}})

        if not set([student['entity_id'] for student in students]) == set(model.entity['student_entity_ids']):
            raise EntityNotFound('No entity {} found'.format(students), None)

        return True

    def get_course_sizes(self):
        result = self.collection.aggregate([{
            '$project': {
                '_id': 0,
                'name': 1,
                'number_of_students': {
                    '$cond': {
                        'if': {'$isArray': "$student_entity_ids"},
                        'then': {'$size': "$student_entity_ids"}, 'else': 0
                    }
                }
            }
        }], cursor={'batchSize': 0})
        return list(result)


class GradeConnector(EntityConnector):
    def __init__(self, mongo_connection):
        super().__init__(mongo_connection)
        self.collection = self.conn['grades']

    def delete_grade(self, entity):
        return self._hard_delete(entity)

    def create_entity(self, entity):
        if self._is_grade_exist(entity['student_entity_id'], entity['course_entity_id']):
            raise EntityAlreadyExistsError('Entity already exists', None)

        response = self._insert_or_update(entity, upsert=True)
        return dumps(response)

    def _is_grade_exist(self, student_id, course_id):
        try:
            return self.collection.find_one({'student_entity_id': student_id, 'course_entity_id': course_id, 'delete_date': {'$exists': False}})
        except Exception as e:
            print(e)
            raise DatabaseError('Database error', e)

    def _insert_or_update(self, entity, upsert=False):
        now = datetime.datetime.utcnow()
        entity.update({'last_update': now})

        return self.collection.find_and_modify(
            {'student_entity_id': entity['student_entity_id'],
             'course_entity_id': entity['course_entity_id'],
             'delete_date': {'$exists': False}
             },
            {
                '$set': entity,
                '$setOnInsert': {'creation_date': now}
            },
            upsert=upsert,
            new=True
        )

    def get_highest_avg_student(self):
        result = self.collection.aggregate([{
            '$group': {
                '_id': "$student_entity_id",
                'highest_avg': {
                    '$avg': "$grade"
                }
            }
        }], cursor={'batchSize': 0})
        return list(result)

    def get_lowest_avg_course(self):
        result = self.collection.aggregate([{
            '$group': {
                '_id': "$course_entity_id",
                'lowest_avg': {
                    '$avg': "$grade"
                }
            }
        }], cursor={'batchSize': 0})
        return list(result)
