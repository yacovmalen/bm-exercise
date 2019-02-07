import datetime
from unittest.mock import MagicMock, Mock, patch

from flask import json

import Routes
import unittest

from Resources.Errors import EntityNotFound, BadRequestError
from Tests.data_api_tests import DataTeacher, DataApi
from Tests.data_utils import clear_test_database, set_test_database_data, remove_fields_from_test_data


class TestApiTeachers(unittest.TestCase):
    def setUp(self):
        Routes.app.testing = True
        self.app = Routes.app.test_client()
        self.token = {'SECURITY_TOKEN_AUTHENTICATION_KEY': DataApi.API_TOKEN['api_token']}

        datetime_mock = Mock(wraps=datetime)
        datetime_mock.datetime.utcnow = MagicMock(return_value=datetime.datetime(2019, 2, 1, 9, 00, 00))
        patch('Utils.MongoUtil.datetime', new=datetime_mock).start()

    def tearDown(self):
        super().tearDown()
        clear_test_database('teachers')
        clear_test_database('students')
        clear_test_database('courses')
        clear_test_database('grades')

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        set_test_database_data('users', DataApi.API_TOKEN)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        clear_test_database('users')

    def test_create_new_teacher(self):
        res = self.app.post('/api/v1/teacher', data=dict(
            first_name='Jon',
            last_name='Doe',
            email='jon@test.com'
        ), headers=self.token)
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(201, res.status_code)
        self.assertDictEqual(data, DataTeacher.TEST_TEACHER_1)

    def test_update_teacher_without_id(self):
        set_test_database_data('teachers', DataTeacher.TEST_TEACHER_1_INS)
        res = self.app.put('/api/v1/teacher', data=dict(
            first_name='Jon',
            email='Doe@test.com'
        ), headers=self.token)
        self.assertEqual(501, res.status_code)

    def test_update_teacher(self):
        set_test_database_data('teachers', DataTeacher.TEST_TEACHER_1_INS)
        res = self.app.put('/api/v1/teacher/1', data=dict(
            first_name='Jon',
            last_name='Doe',
            email='Doe@test.com'
        ), headers=self.token)
        self.assertEqual(204, res.status_code)

    def test_delete_teacher(self):
        set_test_database_data('teachers', DataTeacher.TEST_TEACHER_1_INS)
        res = self.app.delete('/api/v1/teacher/1', data=dict(
            first_name='Jon',
            last_name='Doe',
            email='jon@test.com'
        ), headers=self.token)
        self.assertEqual(204, res.status_code)

    def test_update_non_exist_teacher(self):
        set_test_database_data('teachers', DataTeacher.TEST_TEACHER_1_INS)
        with self.assertRaises(EntityNotFound) as err:
            res = self.app.put('/api/v1/teacher/9999', data=dict(
                first_name='Jon',
                last_name='Doe',
                email='jon@email.com'
            ), headers=self.token)
        self.assertIn('EntityNotFound', err.exception.__repr__())

    def test_delete_non_exist_teacher(self):
        set_test_database_data('teachers', DataTeacher.TEST_TEACHER_1_INS)
        with self.assertRaises(EntityNotFound) as err:
            res = self.app.delete('/api/v1/teacher/9999', data=dict(
                first_name='Jon',
                last_name='Doe',
                email='jon@email.com'
            ), headers=self.token)
        self.assertIn('EntityNotFound', err.exception.__repr__())

    def test_create_teacher_first_name_only(self):
        set_test_database_data('teachers', DataTeacher.TEST_TEACHER_1_INS)
        with self.assertRaises(BadRequestError) as err:
            res = self.app.post('/api/v1/teacher', data=dict(
                first_name='Jon',
                email='Doe@test.com',
            ), headers=self.token)
        self.assertIn('BadRequestError', err.exception.__repr__())

    def test_create_teacher_bad_email_address(self):
        set_test_database_data('teachers', DataTeacher.TEST_TEACHER_1_INS)
        with self.assertRaises(BadRequestError) as err:
            res = self.app.post('/api/v1/teacher', data=dict(
                first_name='Jon',
                last_name='Doe',
                email='1212'
            ), headers=self.token)
        self.assertIn('BadRequestError', err.exception.__repr__())

    def test_get_teacher(self):
        set_test_database_data('teachers', DataTeacher.TEST_TEACHER_1_INS)
        res = self.app.get('/api/v1/teacher/1', headers=self.token)
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(200, res.status_code)
        self.assertDictEqual(data[0], DataTeacher.TEST_TEACHER_1)

    def test_get_non_existent_teacher(self):
        set_test_database_data('teachers', DataTeacher.TEST_TEACHER_1_INS)
        with self.assertRaises(EntityNotFound) as err:
            res = self.app.get('/api/v1/teacher/9999', headers=self.token)
        self.assertIn('EntityNotFound', err.exception.__repr__())


if __name__ == '__main__':
        unittest.main()
