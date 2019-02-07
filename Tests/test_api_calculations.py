import datetime
import json
import unittest
from unittest.mock import Mock, MagicMock, patch

import Routes
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

    def test_calculated_max_students(self):
        set_test_database_data('students', DataStudent.TEST_STUDENT_1_INS)
        set_test_database_data('students', DataStudent.TEST_STUDENT_2_INS)
        set_test_database_data('students', DataStudent.TEST_STUDENT_3_INS)
        set_test_database_data('teachers', DataTeacher.TEST_TEACHER_1_INS)
        set_test_database_data('teachers', DataTeacher.TEST_TEACHER_2_INS)
        set_test_database_data('courses', DataCourse.TEST_COURSE_1_INS)
        set_test_database_data('courses', DataCourse.TEST_COURSE_2_INS)
        set_test_database_data('courses', DataCourse.TEST_COURSE_3_INS)

        res = self.app.get('api/v1/teacher/max_students', headers=self.token)
        self.assertEqual(200, res.status_code)
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(data['name'], DataCourse.TEST_COURSE_3_INS['name'])

    def test_calculated_highest_avg(self):
        set_test_database_data('students', DataStudent.TEST_STUDENT_1_INS)
        set_test_database_data('students', DataStudent.TEST_STUDENT_2_INS)
        set_test_database_data('students', DataStudent.TEST_STUDENT_3_INS)
        set_test_database_data('courses', DataCourse.TEST_COURSE_1_INS)
        set_test_database_data('courses', DataCourse.TEST_COURSE_2_INS)
        set_test_database_data('courses', DataCourse.TEST_COURSE_3_INS)
        set_test_database_data('grades', DataGrade.TEST_GRADE_1_STUDENT_1)
        set_test_database_data('grades', DataGrade.TEST_GRADE_2_STUDENT_1)
        set_test_database_data('grades', DataGrade.TEST_GRADE_3_STUDENT_1)
        set_test_database_data('grades', DataGrade.TEST_GRADE_1_STUDENT_2)
        set_test_database_data('grades', DataGrade.TEST_GRADE_2_STUDENT_2)

        res = self.app.get('api/v1/student/highest_avg', headers=self.token)
        self.assertEqual(200, res.status_code)
        data = json.loads(res.data.decode('utf-8'))
        self.assertDictEqual(data, DataStudent.TEST_STUDENT_SMARTEST)

    def test_calculated_easiest_class(self):
        set_test_database_data('courses', DataCourse.TEST_COURSE_1_INS)
        set_test_database_data('courses', DataCourse.TEST_COURSE_2_INS)
        set_test_database_data('courses', DataCourse.TEST_COURSE_3_INS)
        set_test_database_data('grades', DataGrade.TEST_GRADE_1_STUDENT_1)
        set_test_database_data('grades', DataGrade.TEST_GRADE_2_STUDENT_1)
        set_test_database_data('grades', DataGrade.TEST_GRADE_3_STUDENT_1)
        set_test_database_data('grades', DataGrade.TEST_GRADE_1_STUDENT_2)
        set_test_database_data('grades', DataGrade.TEST_GRADE_2_STUDENT_2)

        res = self.app.get('api/v1/course/easiest', headers=self.token)
        self.assertEqual(200, res.status_code)
        data = json.loads(res.data.decode('utf-8'))
        self.assertDictEqual(data, DataCourse.TEST_COURSE_EASIEST)
