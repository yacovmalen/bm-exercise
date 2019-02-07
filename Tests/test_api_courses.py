import datetime
import json
import unittest
from unittest.mock import Mock, MagicMock, patch

import Routes
from Resources.Errors import EntityNotFound
from Tests.data_api_tests import DataCourse, DataStudent, DataTeacher, DataApi
from Tests.data_utils import clear_test_database, remove_fields_from_test_data, set_test_database_data


class TestApiCourses(unittest.TestCase):
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

    def test_create_new_course(self):
        set_test_database_data('students', DataStudent.TEST_STUDENT_1_INS)
        set_test_database_data('students', DataStudent.TEST_STUDENT_2_INS)
        set_test_database_data('teachers', DataTeacher.TEST_TEACHER_1_INS)

        res = self.app.post('/api/v1/course', data=dict(
            name='Super Course',
            teacher_id='1',
            student_ids="1, 2"
        ), headers=self.token)
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(201, res.status_code)
        self.assertDictEqual(data, DataCourse.TEST_COURSE_1)

    def test_create_new_course_student_not_exist(self):
        set_test_database_data('students', DataStudent.TEST_STUDENT_1_INS)
        set_test_database_data('teachers', DataTeacher.TEST_TEACHER_1_INS)

        with self.assertRaises(EntityNotFound) as err:
            res = self.app.post('/api/v1/course', data=dict(
                name='Super Course',
                teacher_id='1',
                student_ids="1, 2"
            ), headers=self.token)
        self.assertIn('EntityNotFound', err.exception.__repr__())

    def test_create_new_course_teacher_not_exist(self):
        set_test_database_data('students', DataStudent.TEST_STUDENT_1_INS)
        set_test_database_data('students', DataStudent.TEST_STUDENT_2_INS)

        with self.assertRaises(EntityNotFound) as err:
            res = self.app.post('/api/v1/course', data=dict(
                name='Super Course',
                teacher_id='1',
                student_ids="1, 2"
            ), headers=self.token)
        self.assertIn('EntityNotFound', err.exception.__repr__())

    def test_add_students_to_course(self):
        set_test_database_data('students', DataStudent.TEST_STUDENT_1_INS)
        set_test_database_data('students', DataStudent.TEST_STUDENT_2_INS)
        set_test_database_data('students', DataStudent.TEST_STUDENT_3_INS)
        set_test_database_data('teachers', DataTeacher.TEST_TEACHER_1_INS)
        set_test_database_data('courses', DataCourse.TEST_COURSE_1_INS)

        res = self.app.put('/api/v1/course/1', data=dict(
            student_ids="3"
        ), headers=self.token)
        self.assertEqual(204, res.status_code)

    def test_add_non_existent_students_to_course(self):
        set_test_database_data('students', DataStudent.TEST_STUDENT_1_INS)
        set_test_database_data('students', DataStudent.TEST_STUDENT_2_INS)
        set_test_database_data('teachers', DataTeacher.TEST_TEACHER_1_INS)
        set_test_database_data('courses', DataCourse.TEST_COURSE_1_INS)

        with self.assertRaises(EntityNotFound) as err:
            res = self.app.put('/api/v1/course/1', data=dict(
                student_ids="3"
            ), headers=self.token)
        self.assertIn('EntityNotFound', err.exception.__repr__())
        self.assertIn('[3]', err.exception.__repr__())

    def test_update_to_course_without_id(self):
        res = self.app.put('/api/v1/course', data=dict(
            student_ids="3"
        ), headers=self.token)
        self.assertEqual(501, res.status_code)

    def test_remove_students_from_course(self):
        set_test_database_data('courses', DataCourse.TEST_COURSE_1_INS)

        res = self.app.put('/api/v1/course/1', data=dict(
            remove_student_ids="1"
        ), headers=self.token)
        self.assertEqual(204, res.status_code)

    def test_delete_course(self):
        set_test_database_data('courses', DataCourse.TEST_COURSE_1_INS)

        res = self.app.delete('/api/v1/course/1', headers=self.token)
        self.assertEqual(204, res.status_code)

    def test_update_non_exist_course(self):
        set_test_database_data('students', DataStudent.TEST_STUDENT_3_INS)

        with self.assertRaises(EntityNotFound) as err:
            res = self.app.put('/api/v1/course/999', data=dict(student_ids="3"), headers=self.token)
        self.assertIn('EntityNotFound', err.exception.__repr__())
        self.assertIn('999', err.exception.__repr__())

    def test_delete_non_exist_course(self):
        with self.assertRaises(EntityNotFound) as err:
            res = self.app.delete('/api/v1/course/999', headers=self.token)
        self.assertIn('EntityNotFound', err.exception.__repr__())
        self.assertIn('999', err.exception.__repr__())

    def test_get_course(self):
        set_test_database_data('courses', DataCourse.TEST_COURSE_1_INS)
        res = self.app.get('/api/v1/course/1', headers=self.token)
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(200, res.status_code)
        self.assertDictEqual(data[0], DataCourse.TEST_COURSE_1)

    def test_get_non_existent_course(self):
        with self.assertRaises(EntityNotFound) as err:
            res = self.app.get('/api/v1/course/999', headers=self.token)
        self.assertIn('EntityNotFound', err.exception.__repr__())
