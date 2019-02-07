from flask_restful import reqparse

person_body = reqparse.RequestParser()
course_body = reqparse.RequestParser()


class ReqParse(object):

    @classmethod
    def person(cls):
        person_body.add_argument('first_name')
        person_body.add_argument('last_name')
        person_body.add_argument('email')

        return person_body

    @classmethod
    def course(cls):
        course_body.add_argument('name')
        course_body.add_argument('student_ids')
        course_body.add_argument('remove_student_ids')
        course_body.add_argument('teacher_id')

        return course_body
