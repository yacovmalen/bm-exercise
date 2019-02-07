import datetime


class DataApi(object):
    API_TOKEN = {
        'api_token': 'ExampleAccess'
    }


class DataStudent(object):
    TEST_STUDENT_SMARTEST = {
        'highest_avg': 89.66666666666667,
        'entity_id': 1,
        'first_name': 'Jon',
        'last_name': 'Doe',
        'email': 'jon@test.com',
        'creation_date': 'Fri, 01 Feb 2019 09:00:00 GMT',
        'last_update': 'Fri, 01 Feb 2019 09:00:00 GMT'
    }

    TEST_STUDENT_1 = {
        'entity_id': 1,
        'first_name': 'Jon',
        'last_name': 'Doe',
        'email': 'jon@test.com',
        'creation_date': 'Fri, 01 Feb 2019 09:00:00 GMT',
        'last_update': 'Fri, 01 Feb 2019 09:00:00 GMT'
    }

    TEST_STUDENT_1_INS = {
        'entity_id': 1,
        'first_name': 'Jon',
        'last_name': 'Doe',
        'email': 'jon@test.com',
        'creation_date': datetime.datetime(2019, 2, 1, 9, 00, 00),
        'last_update': datetime.datetime(2019, 2, 1, 9, 00, 00)
    }

    TEST_STUDENT_2_INS = {
        'entity_id': 2,
        'first_name': 'Jane',
        'last_name': 'Dane',
        'email': 'jane@test.com',
        'creation_date': datetime.datetime(2019, 2, 1, 9, 00, 00),
        'last_update': datetime.datetime(2019, 2, 1, 9, 00, 00)
    }

    TEST_STUDENT_3_INS = {
        'entity_id': 3,
        'first_name': 'Aya',
        'last_name': 'Flaya',
        'email': 'test@test.com',
        'creation_date': datetime.datetime(2019, 2, 1, 9, 00, 00),
        'last_update': datetime.datetime(2019, 2, 1, 9, 00, 00)
    }


class DataTeacher(object):
    TEST_TEACHER_1 = {
        'entity_id': 1,
        'first_name': 'Jon',
        'last_name': 'Doe',
        'email': 'jon@test.com',
        'creation_date': 'Fri, 01 Feb 2019 09:00:00 GMT',
        'last_update': 'Fri, 01 Feb 2019 09:00:00 GMT'
    }

    TEST_TEACHER_1_INS = {
        'entity_id': 1,
        'first_name': 'Jon',
        'last_name': 'Doe',
        'email': 'jon@test.com',
        'creation_date': datetime.datetime(2019, 2, 1, 9, 00, 00),
        'last_update': datetime.datetime(2019, 2, 1, 9, 00, 00)
    }

    TEST_TEACHER_2_INS = {
        'entity_id': 2,
        'first_name': 'Jane',
        'last_name': 'Dane',
        'email': 'jan@test.com',
        'creation_date': datetime.datetime(2019, 2, 1, 9, 00, 00),
        'last_update': datetime.datetime(2019, 2, 1, 9, 00, 00)
    }


class DataCourse(object):
    TEST_COURSE_EASIEST = {
        'lowest_avg': 70.0,
        'entity_id': 1,
        'name': 'Super Course 1',
        "student_entity_ids": [1, 2],
        "teacher_entity_id": 1,
        'creation_date': 'Fri, 01 Feb 2019 09:00:00 GMT',
        'last_update': 'Fri, 01 Feb 2019 09:00:00 GMT'
    }

    TEST_COURSE_1 = {
        'entity_id': 1,
        'name': 'Super Course 1',
        "student_entity_ids": [1, 2],
        "teacher_entity_id": 1,
        'creation_date': 'Fri, 01 Feb 2019 09:00:00 GMT',
        'last_update': 'Fri, 01 Feb 2019 09:00:00 GMT'
    }

    TEST_COURSE_1_INS = {
        'entity_id': 1,
        'name': 'Super Course 1',
        "student_entity_ids": [1, 2],
        "teacher_entity_id": 1,
        'creation_date': datetime.datetime(2019, 2, 1, 9, 00, 00),
        'last_update': datetime.datetime(2019, 2, 1, 9, 00, 00)
    }

    TEST_COURSE_2_INS = {
        'entity_id': 2,
        'name': 'Super Course 2',
        "student_entity_ids": [1],
        "teacher_entity_id": 1,
        'creation_date': datetime.datetime(2019, 2, 1, 9, 00, 00),
        'last_update': datetime.datetime(2019, 2, 1, 9, 00, 00)
    }

    TEST_COURSE_3_INS = {
        'entity_id': 3,
        'name': 'Super Course 3',
        "student_entity_ids": [1, 2, 3],
        "teacher_entity_id": 2,
        'creation_date': datetime.datetime(2019, 2, 1, 9, 00, 00),
        'last_update': datetime.datetime(2019, 2, 1, 9, 00, 00)
    }


class DataGrade(object):
    TEST_GRADE_1_STUDENT_1 = {
        "course_entity_id": 1,
        "student_entity_id": 1,
        "grade": 80,
        'creation_date': datetime.datetime(2019, 2, 1, 9, 00, 00),
        'last_update': datetime.datetime(2019, 2, 1, 9, 00, 00)
    }

    TEST_GRADE_2_STUDENT_1 = {
        "course_entity_id": 2,
        "student_entity_id": 1,
        "grade": 90,
        'creation_date': datetime.datetime(2019, 2, 1, 9, 00, 00),
        'last_update': datetime.datetime(2019, 2, 1, 9, 00, 00)
    }

    TEST_GRADE_3_STUDENT_1 = {
        "course_entity_id": 3,
        "student_entity_id": 1,
        "grade": 99,
        'creation_date': datetime.datetime(2019, 2, 1, 9, 00, 00),
        'last_update': datetime.datetime(2019, 2, 1, 9, 00, 00)
    }

    TEST_GRADE_1_STUDENT_2 = {
        "course_entity_id": 3,
        "student_entity_id": 2,
        "grade": 95,
        'creation_date': datetime.datetime(2019, 2, 1, 9, 00, 00),
        'last_update': datetime.datetime(2019, 2, 1, 9, 00, 00)
    }

    TEST_GRADE_2_STUDENT_2 = {
        "course_entity_id": 1,
        "student_entity_id": 2,
        "grade": 60,
        'creation_date': datetime.datetime(2019, 2, 1, 9, 00, 00),
        'last_update': datetime.datetime(2019, 2, 1, 9, 00, 00)
    }

    TEST_GRADE_1_STUDENT_3 = {
        "course_entity_id": 3,
        "student_entity_id": 3,
        "grade": 60,
        'creation_date': datetime.datetime(2019, 2, 1, 9, 00, 00),
        'last_update': datetime.datetime(2019, 2, 1, 9, 00, 00)
    }