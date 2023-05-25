from flask import Blueprint, jsonify, request, url_for, send_from_directory, make_response

from functions.zipper import file_zipping, zip_delete
from functions import password_generator, login_generator

from data import db_session
from data.teachers import Teacher
from data.exams import Exam
from data.portfolio import Portfolio
from data.students import Student


UPLOAD_FOLDER = './static/files'
DOWNLOAD_FOLDER = './static/files'
ALLOWED_EXTENSIONS = ['pdf', 'png', 'jpg', 'jpeg']

blueprint = Blueprint(
    'site_api',
    __name__,
    template_folder='templates'
)



 #______________________________________________GET_________________________________________________________________
@blueprint.route('/api/get_student/<login>/<password>')
def get_student_api(login, password):
    db_sess = db_session.create_session()
    student = db_sess.query(Student).filter(Student.login == login, Student.password == password).first()
    if student:
        dict_obj = student.to_dict()
        dict_obj["avatar"] = url_for("student_avatar", student_id=student.id)
        return jsonify(dict_obj)
    return jsonify({
        "operation": None
    })


@blueprint.route('/api/get_teacher/<login>/<password>')
def get_teacher_api(login, password):
    db_sess = db_session.create_session()
    teacher = db_sess.query(Teacher).filter(Teacher.login == login, Teacher.password == password).first()
    if teacher:
        dict_obj = teacher.to_dict()
        dict_obj["avatar"] = url_for("teacher_avatar", teacher_id=teacher.id)
        return jsonify(dict_obj)
    return jsonify({
        "Operation": None
    })


@blueprint.route('/api/classes/<teacher_id>')
def classes_api(teacher_id):
    db_sess = db_session.create_session()
    teacher = db_sess.query(Teacher).filter(Teacher.id == teacher_id).first()
    if teacher:
        teacher_dict = teacher.to_dict()
        teacher_dict["avatar"] = url_for("teacher_avatar", teacher_id=teacher_id)
        students = db_sess.query(Student).filter(Student.teacher_id == teacher_id).all()
        for index in range(len(students)):
            students[index] = students[index].to_dict()
            students[index]["avatar"] = url_for("student_avatar", student_id=students[index]["id"])
        dict_obj = {
                "teacher": teacher_dict,
                "students": students
        }
        return jsonify(dict_obj)

    return jsonify({
        "Operation": None
    })


@blueprint.route('/api/profile/<string:student_id>')
def profile_api(student_id):
    db_sess = db_session.create_session()
    student = db_sess.query(Student).filter(Student.id == student_id).first()
    portfolio = db_sess.query(Portfolio).filter(Portfolio.student_id == student_id).all()
    port_list = [item.to_dict() for item in portfolio]
    for item in port_list:
        item["request"] = url_for("show_document", filename=item["file_uuid"])

    dict_obj = {
            "student":
                     student.to_dict(),
            "portfolio":
                     port_list
            }

    return jsonify(dict_obj)


@blueprint.route('/api/get_exams/<student_id>')
def get_exams(student_id):
    db_sess = db_session.create_session()
    exams = db_sess.query(Exam).filter(Exam.student_id == student_id).all()
    if exams:
        exams = [exam.to_dict() for exam in exams]
        for exam in exams:
            exam.pop("student_id")
        dict_obj = {
                    "exams": exams
                    }

        return jsonify(dict_obj)
    return jsonify({
        "exams": None
    })


@blueprint.route('/api/download_all/<student_id>')
def download_all(student_id):
    db_sess = db_session.create_session()
    portfolio = db_sess.query(Portfolio).filter(Portfolio.student_id == student_id).all()
    archive = file_zipping(portfolio)
    zip_sender = send_from_directory(DOWNLOAD_FOLDER, archive, as_attachment=True)

    h = make_response(open("./static/files/" + archive, "rb"))
    h.headers['Content_Type'] = 'files/zip'
    json_obj = {
                "request": url_for("show_api_document", h=h)
               }
    zip_delete(archive)
    return jsonify(json_obj)


@blueprint.route('/api/download_one/')
def download_one():
    pass


 #______________________________________________POST________________________________________________________________
@blueprint.route('/api/add_student')
def add_student_api():
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
    return jsonify({"operation": "OK"})

@blueprint.route('/api/add_portfolio')
def add_portfolio_api():
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
        return jsonify({"operation": "OK"})




@blueprint.route("/api/delete_student/<student_id>")
def delete_student_api(student_id):
    db.delete_student_by_id(student_id)
    return jsonify({"operation": "OK"})




