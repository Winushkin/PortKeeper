# from flask import Blueprint, jsonify, request, url_for, send_from_directory, make_response
# import os
#
# from added_files.zipper import file_zipping, zip_delete
# from database import DataBase
# from added_files import login_generator, password_generator
#
# from ..data import db_session
# from ..data.teachers import Teacher
# from ..data.exams import Exam
# from ..data.groups import Group
# from ..data.portfolio import Portfolio
# from ..data.students import Student
#
#
# UPLOAD_FOLDER = './static/files'
# DOWNLOAD_FOLDER = './static/files'
# ALLOWED_EXTENSIONS = ['pdf', 'png', 'jpg', 'jpeg']
#
# blueprint = Blueprint(
#     'site_api',
#     __name__,
#     template_folder='templates'
# )
#
#
#
#
# @blueprint.route('/api/get_student/<login>/<password>')
# def get_student_api(login, password):
#     db_sess = db_session.create_session()
#     student = db_sess.query(Student).filter(Student.login == login, Student.password == password)
#     student.avatar = url_for("student_avatar", student_id=student["student_id"])
#     return jsonify(student)
#
#
# @blueprint.route('/api/get_teacher/<login>/<password>')
# def get_teacher_api(login, password):
#     teacher = dict(db.get_teacher(login, password))
#     teacher["avatar"] = url_for("teacher_avatar", teacher_id=teacher["teacher_id"])
#     return jsonify(teacher)
#
#
# @blueprint.route('/api/classes/<teacher_id>')
# def classes_api(teacher_id):
#     teacher = dict(db.get_teacher_by_teacher_id(teacher_id))
#     teacher["avatar"] = url_for("teacher_avatar", teacher_id=teacher["teacher_id"])
#     students = list(db.get_students_by_teacher_id(teacher_id))
#     for index in range(len(students)):
#         students[index] = \
#                         {
#                         "student_id": students[index][0],
#                         "name": students[index][1],
#                         "login": students[index][2],
#                         "password": students[index][3],
#                         "avatar": url_for("student_avatar", student_id=students[index][0]),
#                         "birth_day": students[index][5],
#                         "class": students[index][7]
#                         }
#
#     dict_obj = {
#             "teacher": teacher,
#             "students": students
#     }
#     return jsonify(dict_obj)
#
#
# @blueprint.route('/api/profile/<string:student_id>')
# def profile_api(student_id):
#     student = db.get_student_by_student_id(student_id)
#     portfolio = db.get_portfolio_by_student_id(student_id)
#     port_list = [list(item) for item in portfolio]
#     port_reqs = [list(item)[5] for item in portfolio]
#
#     json_obj = {
#             "student":{
#                     "student_id": student[0],
#                     "name": student[1],
#                     "login": student[2],
#                     "password": student[3],
#                     "avatar": url_for("student_avatar", student_id=student_id),
#                     "birth_day": student[5],
#                     "class": student[6],
#                     "teacher_id": student[7]
#                      },
#             "portfolio":
#                      port_list,
#             "requests":
#                      port_reqs
#              }
#
#     return jsonify(json_obj)
#
#
# @blueprint.route('/api/add_student')
# def add_student_api():
#     if not request.json:
#         return jsonify({'error': 'Empty request'})
#     elif not all(key in request.json for key in
#                  ['student_name', 'content', 'teacher_id', 'login', 'password']):
#         return jsonify({'error': 'Bad request'})
#     else:
#         student_name = request.json["student_name"]
#         student_class = request.json["student_class"]
#         teacher_id = request.json["teacher_id"]
#         login = login_generator.generate_login(student_name)
#         password = password_generator.generate_password()
#
#         db.insert_student(student_name, login, password, teacher_id, student_class, 0)
#     return jsonify({"operation": "OK"})
#
# @blueprint.route('/api/add_portfolio')
# def add_portfolio_api():
#     if not request.json:
#         return jsonify({'error': 'Empty request'})
#     elif not all(key in request.json for key in
#                  ['name', 'level', 'student_id', 'user_id', 'result', 'result', 'random_uuid']):
#         return jsonify({'error': 'Bad request'})
#     else:
#         name = request.json["name"]
#         level = request.json["level"]
#         student_id = request.json["student_id"]
#         subject = request.json["subject"]
#         date = request.json["date"]
#         result = request.json["result"]
#         random_uuid = request.json["random_uuid"]
#         db.insert_portfolio(name, subject, student_id, level, random_uuid, result, date)
#         return jsonify({"operation": "OK"})
#
#
# @blueprint.route('/api/get_exams/<student_id>')
# def get_exams(student_id):
#     exams = [dict(x) for x in db.get_exams_by_student_id(student_id)]
#     for exam in exams:
#         exam.pop("student_id")
#         exam.pop("created_at")
#     json_obj = {
#                 "exams": exams
#                 }
#
#     return jsonify(json_obj)
#
# @blueprint.route("/api/delete_student/<student_id>")
# def delete_student_api(student_id):
#     db.delete_student_by_id(student_id)
#     return jsonify({"operation": "OK"})
#
#
# @blueprint.route('/api/download_all/<student_id>')
# def download_all(student_id):
#     portfolio = db.get_portfolio_by_student_id(student_id)
#     archive = file_zipping(portfolio)
#     zip_sender = send_from_directory(DOWNLOAD_FOLDER, archive, as_attachment=True)
#
#     h = make_response(open("./static/files/" + archive, "rb"))
#     h.headers['Content_Type'] = 'files/zip'
#     json_obj = {
#                 "request": url_for("show_api_document", h=h)
#                }
#     zip_delete(archive)
#     return jsonify(json_obj)
#
#
# @blueprint.route('/api/download_one/')
# def download_one():
#     pass
