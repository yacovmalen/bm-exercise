# Coding Exercise

This coding example represents a grade management system using a RESTful interface to create/update/delete a teacher,
student, or course, and create/remove grades. Also provided, are apis to receive calculated data for the highest average
student (in any course), the teacher with the most students, or the easiest course based on course average.

## Quick Start
* Requirements:
** Python==3.6
** Urllib (for startup script)
** Docker

### Running the start up script
_usage:_ python Startup.py <start|stop> <build>
- _start:_ (Default) Starts the docker container. If no docker image exists with the correct tag, automatically runs a
                       docker build
- _stop:_ Stops and removes all running docker containers
- _build:_ (Optional) Forces a new docker build

## APIs
**Baseurl** : localhost:5000/api/v1

### Basic Authentication
The api require a simple authentication api key.

In the request header, the following field is `required`:
>'SECURITY_TOKEN_AUTHENTICATION_KEY': **[__token__]**

For this test environment, a token is auto created and inserted into the database. The header key should look like:
>{'SECURITY_TOKEN_AUTHENTICATION_KEY': 'ExampleAccess'}


Apis are provide for each data model plus additional apis to get calculated data.

##### Student
---
/student

_METHOD:_ GET - Retrieves a list of all students in the database - RETURN - Object 200

_METHOD:_ POST - Creates a new student entity RETURN 201


/student/<int:entity_id>

_METHOD:_ GET - Returns the student from the id query parameter - RETURN - Object 200

_METHOD:_ PUT - Updates the student from the id query parameter -

&emsp;&emsp;&emsp;&emsp;&emsp;BODY
```javascript
{ "first_name": {"type": "string", "empty": False, "dependencies": "last_name"},
 "last_name": {"type": "string", "empty": False, "dependencies": "first_name"},
 "email": {"type": "string", "regex": "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"} <valid email>}
```
&emsp;&emsp;&emsp;&emsp;&emsp;RETURN Successful - 204

_METHOD:_ DELETE - Removes the student by id in the query parameter (soft delete - adds delete date, does not remove
                   object from the database) - RETURN 204

##### Teacher
---
/teacher

_METHOD:_ GET - Retrieves a list of all teachers in the database - RETURN - Object 200

_METHOD:_ POST - Creates a new student 

&emsp;&emsp;&emsp;&emsp;&emsp;BODY - 
```javascript 
{ "first_name": {"type": "string", "empty": False, "dependencies": "last_name"},
 "last_name": {"type": "string", "empty": False, "dependencies": "first_name"},
 "email": {"type": "string", "regex": "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"} <valid email>}
 ```
&emsp;&emsp;&emsp;&emsp;&emsp;RETURN 201

/teacher/<int:entity_id>

_METHOD:_ GET - Returns the teacher from the id query parameter - RETURN - Object 200

_METHOD:_ PUT - Updates the teacher from the id query parameter

&emsp;&emsp;&emsp;&emsp;&emsp;BODY - 
```javascript
{ "first_name": {"type": "string", "empty": False, "dependencies": "last_name"},
 "last_name": {"type": "string", "empty": False, "dependencies": "first_name"},
 "email": {"type": "string", "regex": "^[\a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"} <valid email>}
```   
&emsp;&emsp;&emsp;&emsp;&emsp;RETRUN 204

_METHOD:_ DELETE - Removes the student by id in the query parameter (soft delete - adds delete date, does not remove
                   object from the database) - RETURN 204

##### Course
---
/course

_METHOD:_ GET - Retrieves a list of all course in the database RETURN - Object 200

_METHOD:_ POST - Creates a new course entity
                Students/Teachers are validated that they exist in the database before being added to the course
                
&emsp;&emsp;&emsp;&emsp;&emsp;BODY - 
```javascript
{"name": {"type": "string"},
"student_entity_ids": {"type": "list", "schema": {"type": "integer"}},
"teacher_entity_id": {"type": "integer"}}
```
&emsp;&emsp;&emsp;&emsp;&emsp;RETURN Successful - 201

/course/<int:entity_id>

_METHOD:_ GET - Returns the course from the id query parameter - RETURN - Object 200

_METHOD:_ PUT - Updates the course from the id query parameter -

                To remove students from a course, include the _delete_student_entity_ids_ key:value in the json.
                To add students to a course, include the student_entity_ids key:value in the json.
                Students/Teachers are validated that they exist in the database before being added to the course
                
&emsp;&emsp;&emsp;&emsp;&emsp;BODY - 
```javascript
{"name": {"type": "string"},
"student_entity_ids": {"type": "list", "schema": {"type": "integer"}},
"delete_student_entity_ids": {"type": "list", "schema": {"type": "integer"}},
"teacher_entity_id": {"type": "integer"}}
```
&emsp;&emsp;&emsp;&emsp;&emsp;RETURN Successful - 204

_METHOD:_ DELETE - Removes the course by id in the query parameter (soft delete - adds delete date, does not remove
                   object from the database) - RETURN 204

##### Grade
---
/grade/student/<int:student_entity_id>

_METHOD:_ GET - Retrieves a list of all grades for all courses for the given student in the database RETURN - Object 200


/grade/course/<int:course_entity_id>

_METHOD:_ GET - Retrieves a list of all grades for all students for the given course in the database RETURN - Object 200


/grade/student/<int:student_entity_id>/course/<int:course_entity_id>

_METHOD:_ GET - Retrieves the grade for the student for the course in the the GET request RETURN - Object 200

_METHOD:_ DELETE - Removes the grade by student id and the course id in the DELETE request (hard delete -
                   removes the object from the database)- RETURN Successful - 204

/grade/student/<int:student_entity_id>/course/<int:course_entity_id>/<int:grade>

_METHOD:_ POST - Creates a new grade entity for the given student and given course id with the given grade
                Courses and students are validated that they exist in the database before being added to the course - RETURN Successful - 201

_METHOD:_ PUT - Updates the grade from the student id and course id query parameters and the given grade - RETURN Successful - 204

##### Calculated data
---
/teacher/max_students

_METHOD:_ GET - Retrieves the teacher with the highest number of students across all the teachers courses RETURN - Teacher Object 200

/student/highest_avg

_METHOD:_ GET - Retrieves the student with the highest average across all the courses RETURN - Student Object 200 - with average

/course/easiest

_METHOD:_ GET - Retrieves the course with the lowest average across all the grades with the same course id RETURN - Course Object 200 - with average
