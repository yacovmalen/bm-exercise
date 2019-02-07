"""
Routes file - Manage api routes mapped to application functions
Apis are created using Flask-RESTful
"""
from flask import Flask, Blueprint
from flask_restful import Api

from Resources.Calculations import TeacherMaxStudents, StudentHighestAvg, CourseEasiest
from Resources.Courses import Course
from Resources.Errors import ErrorDefinitions
from Resources.Grades import Grade
from Resources.Health import HealthCheck
from Resources.Students import Student
from Resources.Teachers import Teacher
from Utils.MongoUtil import MongoConnector


# Server application creation and setup
app = Flask(__name__)
version_one = Blueprint('api', __name__, url_prefix='/api/v1')
api_v_one = Api(version_one, errors=ErrorDefinitions.errors)
app.register_blueprint(version_one)
# End server setup

db_conn = MongoConnector()  # Create a database connection


# Health Check
api_v_one.add_resource(HealthCheck, '/isalive')

###
# Student Apis
###
api_v_one.add_resource(Student, '/student', '/student/<int:entity_id>', resource_class_kwargs={'db_conn': db_conn})

###
# Teacher Apis
###
api_v_one.add_resource(Teacher, '/teacher', '/teacher/<int:entity_id>', resource_class_kwargs={'db_conn': db_conn})

###
# Course Apis
###
api_v_one.add_resource(Course, '/course', '/course/<int:entity_id>', resource_class_kwargs={'db_conn': db_conn})

###
# Grade Apis
###
api_v_one.add_resource(Grade, '/grade/student/<int:student_entity_id>',
                              '/grade/course/<int:course_entity_id>',
                              '/grade/student/<int:student_entity_id>/course/<int:course_entity_id>',
                              '/grade/student/<int:student_entity_id>/course/<int:course_entity_id>/<int:grade>',
                       resource_class_kwargs={'db_conn': db_conn})

###
# Calculation Apis
###
api_v_one.add_resource(TeacherMaxStudents, '/teacher/max_students', resource_class_kwargs={'db_conn': db_conn})
api_v_one.add_resource(StudentHighestAvg, '/student/highest_avg', resource_class_kwargs={'db_conn': db_conn})
api_v_one.add_resource(CourseEasiest, '/course/easiest', resource_class_kwargs={'db_conn': db_conn})


if __name__ == '__main__':
    app.run(debug=False)
