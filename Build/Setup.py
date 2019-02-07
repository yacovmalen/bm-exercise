import os
import time
import urllib
from sys import argv

import docker as docker
from docker.errors import ImageNotFound

from Tests.data_api_tests import DataStudent, DataGrade, DataCourse, DataApi, DataTeacher
from Tests.data_utils import set_test_database_data

DOCKER_TAG = 'code_example'
HEALTH_CHECK_URL = 'http://localhost:5000/api/v1/isalive'
HEALTH_TIMEOUT_SECS = 20


def docker_build():
    print('Starting Project Docker Build')
    base_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
    os.chdir(base_path)

    client = docker.APIClient(base_url='unix://var/run/docker.sock')

    stream = client.build(path=base_path, dockerfile='Build/Dockerfile',
                          tag=DOCKER_TAG, buildargs={}, decode=True)
    for s in stream:
        try:
            print(s['stream'].strip())
        except Exception as e:
            print('output error {}'.format(e))
            print(s)
            raise Exception(s)


def docker_start():
    client = docker.from_env()
    try:
        res = client.containers.get('mongodb')
        print('Database already started... starting server')
    except:
        print('Start the mongo database')
        res = client.containers.run('mongo:3.6', name='mongodb', detach=True, network='host', ports={'27017': 27017})

    state = res.status
    timeout = 0
    while not state == 'running' and timeout <= HEALTH_TIMEOUT_SECS:
        print('\rChecking database state{}'.format('.' * int((timeout % 4))), end="")
        state = client.containers.get(res.id).status
        time.sleep(1)
        timeout += 1

    if timeout >= HEALTH_TIMEOUT_SECS:
        print('\nFailed to start database')
        exit(1)
    else:
        print('\nDatabase successfully started')

    insert_initial_test_data()

    try:
        client.images.get(DOCKER_TAG)
    except ImageNotFound as e:
        docker_build()

    try:
        client.containers.run(DOCKER_TAG, detach=True, network='host', ports={'5000': 5000})
    except Exception as e:
        print('Failed to start docker with error {}'.format(e))
        exit(1)

    timeout = 0
    while app_health() != 200 and timeout <= HEALTH_TIMEOUT_SECS:
        print('\rRunning health check{}'.format('.' * int((timeout % 4))), end="")
        time.sleep(1)
        timeout += 1

    if timeout >= HEALTH_TIMEOUT_SECS:
        print('\nFailed to start server')
        exit(1)
    else:
        print('\nServer successfully started')
        exit(0)


def docker_stop():
    client = docker.from_env()
    all_dockers = client.containers.list(all=True)
    for container in all_dockers:
        client.containers.get(container.name).remove(force=True)
    print('Docker images stopped and removed {}'.format(all_dockers))


def app_health():
    try:
        req = urllib.request.Request(HEALTH_CHECK_URL, headers={'SECURITY_TOKEN_AUTHENTICATION_KEY': DataApi.API_TOKEN['api_token']})
        r = urllib.request.urlopen(req)
        return r.getcode()
    except Exception as e:
        return None


def insert_initial_test_data():
    set_test_database_data('teachers', DataTeacher.TEST_TEACHER_1_INS)
    set_test_database_data('students', DataStudent.TEST_STUDENT_1_INS)
    set_test_database_data('courses', DataCourse.TEST_COURSE_1_INS)
    set_test_database_data('grades', DataGrade.TEST_GRADE_1_STUDENT_1)
    set_test_database_data('grades', DataGrade.TEST_GRADE_2_STUDENT_1)
    set_test_database_data('grades', DataGrade.TEST_GRADE_3_STUDENT_1)
    set_test_database_data('users', DataApi.API_TOKEN)


if __name__ == '__main__':
    if len(argv) >= 2 and argv[1] not in ['start', 'stop']:
        print('Usage: python Setup.py <start|stop> <build>')
        exit(1)

    if len(argv) == 2 and argv[1] == 'stop':
        docker_stop()
        exit(0)
    elif len(argv) == 3 and argv[2] == 'build':
        docker_build()

    docker_start()

