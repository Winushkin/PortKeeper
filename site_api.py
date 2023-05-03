from flask import Blueprint, jsonify, request
from database import DataBase
from added_files import login_generator, password_generator

db = DataBase("database/base.sqlite3")
db.create_tables()

blueprint = Blueprint(
    'site_api',
    __name__,
    template_folder='templates'
)



@blueprint.route('/api/get_student_by_student_id/<login>/<password>')
def get_student_api(login, password):
    return jsonify([dict(x) for x in [db.get_student(login, password)]])

@blueprint.route('/api/get_teacher_by_teacher_id/<login>/<password>')
def teacher_login_api(login, password):
    return jsonify([dict(x) for x in [db.get_teacher(login, password)]])

@blueprint.route('/api/classes/teacher_id')
def classes_api(teacher_id):
    return (jsonify([dict(x) for x in [db.get_teacher_by_teacher_id(teacher_id)]]),
            jsonify([dict(x) for x in [db.get_students_by_teacher_id(teacher_id)]]))

@blueprint.route('/api/profile/student_id')
def profile(student_id):
    return (jsonify([dict(x) for x in [db.get_student_by_student_id(student_id)]]))

@blueprint.route('/api/add_student')
def add_student():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['student_name', 'content', 'teacher_id', 'login', 'password']):
        return jsonify({'error': 'Bad request'})
    else:
        student_name = request.json["student_name"]
        student_class = request.json["student_class"]
        teacher_id = request.json["teacher_id"]
        login = login_generator.generate_login(student_name)
        password = password_generator.generate_password()

        db.insert_student(student_name, login, password, teacher_id, student_class, 0)

@blueprint.route('/api/add_portfolio')
def add_portfolio():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['name', 'level', 'student_id', 'user_id', 'result', 'result', 'random_uuid']):
        return jsonify({'error': 'Bad request'})
    else:
        name = request.json["name"]
        level = request.json["level"]
        student_id = request.json["student_id"]
        subject = request.json["subject"]
        date = request.json["date"]
        result = request.json["result"]
        random_uuid = request.json["random_uuid"]
        db.insert_portfolio(name, subject, student_id, level, random_uuid, result, date)
