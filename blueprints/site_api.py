from flask import Blueprint, jsonify, request, url_for, send_from_directory, make_response

from data.groups import Group
from data.groups_to_students import GroupToStudent
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
        groups = db_sess.query(Group).filter(Group.teacher_id == teacher.id).all()
        for index in range(len(groups)):
            groups[index] = groups[index].to_dict()
            groups[index]["avatar"] = url_for("student_avatar", student_id=groups[index]["id"])
        dict_obj = {
                "groups": teacher_dict,
                "students": groups
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


@blueprint.route('/api/get_groups/<teacher_id>')
def get_groups(teacher_id):
    db_sess = db_session.create_session()
    groups = [group.to_dict() for group in db_sess.query(Group).filter(Group.teacher_id == teacher_id).all()]
    if all(groups):
        json_obj = {
            "groups": groups
        }
        return jsonify(json_obj)
    return jsonify({
        "groups": None
    })


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
                 ['student_name', 'content', 'teacher_id', 'login', 'password', 'group_id']):
        return jsonify({'error': 'Bad request'})
    else:
        student_name = request.json["student_name"]
        teacher_id = request.json["teacher_id"]
        group_id = request.json["group_id"]
        login = login_generator.generate_login(student_name)
        db_sess = db_session.create_session()
        student = Student()
        student.name = student_name
        student.login = login
        student.teacher_id = teacher_id
        student.password = password_generator.generate_password()
        db_sess.add(student)
        db_sess.commit()
        student = db_sess.query(Student).filter(Student.login == login).first()
        group_to_stud = GroupToStudent()
        group_to_stud.group_id = group_id
        group_to_stud.student_id = student.id
        db_sess.add(group_to_stud)
        db_sess.commit()

    return jsonify({"operation": "OK"})


@blueprint.route('/api/add_portfolio')
def add_portfolio_api():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['name', 'level', 'student_id', 'user_id', 'result', 'result', 'file_uuid']):
        return jsonify({'error': 'Bad request'})
    else:
        db_sess = db_session.create_session()
        port = Portfolio()
        port.name = request.json["name"]
        port.level = request.json["level"]
        port.student_id = request.json["student_id"]
        port.subject = request.json["subject"]
        port.date = request.json["date"]
        port.result = request.json["result"]
        port.file_uuid = request.json["random_uuid"]
        db_sess.add(port)
        db_sess.commit()
        return jsonify({"operation": "OK"})



@blueprint.route("/api/delete_student/<student_id>")
def delete_student_api(student_id):
    db_sess = db_session.create_session()
    db_sess.query(Student).filter(Student.id == student_id).delete()
    db_sess.commit()
    return jsonify({"operation": "OK"})

@blueprint.route("/api/teacher-registration")
def teacher_registration():
    if not request.json:
        return jsonify({'operation': 'Empty request'})
    elif not all(key in request.json for key in
                 ['name', 'level', 'student_id', 'user_id', 'result', 'result', 'file_uuid']):
        return jsonify({'operation': 'Bad request'})
    else:
        db_sess = db_session.create_session()
        teacher = Teacher()
        teacher.name = request.json["name"]
        teacher.login = request.json["login"]
        teacher.password = request.json["password"]
        teacher.post = request.json["post"]
        db_sess.add(teacher)
        db_sess.commit()
        return jsonify({"operation": "OK"})




