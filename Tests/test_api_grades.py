import datetime
import json
import unittest
from unittest.mock import Mock, MagicMock, patch

import Routes
from Resources.Errors import EntityNotFound, EntityAlreadyExistsError
from Tests.data_api_tests import DataCourse, DataStudent, DataTeacher, DataGrade, DataApi
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

    def test_get_a_grade_for_a_student_in_a_course(self):
        set_test_database_data('students', DataStudent.TEST_STUDENT_1_INS)
        set_test_database_data('courses', DataCourse.TEST_COURSE_1_INS)
        set_test_database_data('grades', DataGrade.TEST_GRADE_1_STUDENT_1)
        set_test_database_data('grades', DataGrade.TEST_GRADE_2_STUDENT_1)
        set_test_database_data('grades', DataGrade.TEST_GRADE_3_STUDENT_1)

        res = self.app.get('/api/v1/grade/student/1/course/2', headers=self.token)
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(200, res.status_code)
        self.assertEqual(1, len(data))

    def test_get_a_grade_for_a_non_existent_student(self):
        set_test_database_data('students', DataStudent.TEST_STUDENT_1_INS)
        set_test_database_data('courses', DataCourse.TEST_COURSE_1_INS)
        set_test_database_data('grades', DataGrade.TEST_GRADE_1_STUDENT_1)
        set_test_database_data('grades', DataGrade.TEST_GRADE_2_STUDENT_1)
        set_test_database_data('grades', DataGrade.TEST_GRADE_3_STUDENT_1)

        with self.assertRaises(EntityNotFound) as err:
            res = self.app.get('/api/v1/grade/student/999', headers=self.token)
        self.assertIn('EntityNotFound', err.exception.__repr__())
        self.assertIn('999', err.exception.__repr__())
        self.assertNotIn('course_entity_id', err.exception.__repr__())
        self.assertIn('student_entity_id', err.exception.__repr__())

    def test_get_a_grade_for_a_non_existent_course(self):
        set_test_database_data('students', DataStudent.TEST_STUDENT_1_INS)
        set_test_database_data('courses', DataCourse.TEST_COURSE_1_INS)
        set_test_database_data('grades', DataGrade.TEST_GRADE_1_STUDENT_1)
        set_test_database_data('grades', DataGrade.TEST_GRADE_2_STUDENT_1)
        set_test_database_data('grades', DataGrade.TEST_GRADE_3_STUDENT_1)

        with self.assertRaises(EntityNotFound) as err:
            res = self.app.get('/api/v1/grade/course/999', headers=self.token)
        self.assertIn('EntityNotFound', err.exception.__repr__())
        self.assertIn('999', err.exception.__repr__())
        self.assertIn('course_entity_id', err.exception.__repr__())
        self.assertNotIn('student_entity_id', err.exception.__repr__())

    def test_create_a_new_grade(self):
        set_test_database_data('students', DataStudent.TEST_STUDENT_1_INS)
        set_test_database_data('courses', DataCourse.TEST_COURSE_1_INS)

        res = self.app.post('/api/v1/grade/student/1/course/1/100', headers=self.token)
        self.assertEqual(201, res.status_code)

    def test_create_an_existing_grade(self):
        set_test_database_data('students', DataStudent.TEST_STUDENT_1_INS)
        set_test_database_data('courses', DataCourse.TEST_COURSE_1_INS)
        set_test_database_data('grades', DataGrade.TEST_GRADE_1_STUDENT_1)

        with self.assertRaises(EntityAlreadyExistsError) as err:
            res = self.app.post('/api/v1/grade/student/1/course/1/100', headers=self.token)
        self.assertIn('EntityAlreadyExistsError', err.exception.__repr__())

    def test_create_a_new_grade_for_non_existent_student(self):
        set_test_database_data('students', DataStudent.TEST_STUDENT_1_INS)
        set_test_database_data('courses', DataCourse.TEST_COURSE_1_INS)

        with self.assertRaises(EntityNotFound) as err:
            res = self.app.post('/api/v1/grade/student/999/course/1/100', headers=self.token)
        self.assertIn('EntityNotFound', err.exception.__repr__())
        self.assertIn('999', err.exception.__repr__())

    def test_create_a_new_grade_for_non_existent_course(self):
        set_test_database_data('students', DataStudent.TEST_STUDENT_1_INS)
        set_test_database_data('courses', DataCourse.TEST_COURSE_1_INS)

        with self.assertRaises(EntityNotFound) as err:
            res = self.app.post('/api/v1/grade/student/1/course/999/100', headers=self.token)
        self.assertIn('EntityNotFound', err.exception.__repr__())
        self.assertIn('999', err.exception.__repr__())

    def test_update_a_grade(self):
        set_test_database_data('students', DataStudent.TEST_STUDENT_1_INS)
        set_test_database_data('courses', DataCourse.TEST_COURSE_1_INS)
        set_test_database_data('grades', DataGrade.TEST_GRADE_1_STUDENT_1)

        res = self.app.put('/api/v1/grade/student/1/course/1/100', headers=self.token)
        self.assertEqual(204, res.status_code)

    def test_update_a_non_existent_grade(self):
        with self.assertRaises(EntityNotFound) as err:
            res = self.app.put('/api/v1/grade/student/1/course/1/100', headers=self.token)
        self.assertIn('EntityNotFound', err.exception.__repr__())

    def test_delete_a_grade(self):
        set_test_database_data('grades', DataGrade.TEST_GRADE_1_STUDENT_1)

        res = self.app.delete('/api/v1/grade/student/1/course/1', headers=self.token)
        self.assertEqual(204, res.status_code)

    def test_get_all_grades_for_one_student(self):
        set_test_database_data('grades', DataGrade.TEST_GRADE_1_STUDENT_1)
        set_test_database_data('grades', DataGrade.TEST_GRADE_2_STUDENT_1)
        set_test_database_data('grades', DataGrade.TEST_GRADE_3_STUDENT_1)
        set_test_database_data('grades', DataGrade.TEST_GRADE_1_STUDENT_2)
        set_test_database_data('grades', DataGrade.TEST_GRADE_1_STUDENT_3)

        res = self.app.get('/api/v1/grade/student/1', headers=self.token)
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(200, res.status_code)
        self.assertEqual(3, len(data))

    def test_get_all_grades_for_one_course(self):
        set_test_database_data('grades', DataGrade.TEST_GRADE_1_STUDENT_1)
        set_test_database_data('grades', DataGrade.TEST_GRADE_2_STUDENT_1)
        set_test_database_data('grades', DataGrade.TEST_GRADE_3_STUDENT_1)
        set_test_database_data('grades', DataGrade.TEST_GRADE_1_STUDENT_2)
        set_test_database_data('grades', DataGrade.TEST_GRADE_1_STUDENT_3)

        res = self.app.get('/api/v1/grade/course/3', headers=self.token)
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(200, res.status_code)
        self.assertEqual(3, len(data))
