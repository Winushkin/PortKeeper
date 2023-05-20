import os
import uuid

import fitz

from flask import Flask, render_template, redirect, session, request, send_from_directory, \
    url_for, make_response, abort, flash
from forms.login_form import LoginForm
from forms.StudentAdd_form import AddStudents
from forms.registration_form import RegistrationForm

from added_files.login_generator import generate_login
from added_files.password_generator import generate_password
from added_files.zipper import file_zipping, zip_delete

from data import db_session
from database import DataBase
from data.students import Student
from data.teachers import Teacher
from data.portfolio import Portfolio
from data.exams import Exam
from blueprints import site_api

UPLOAD_FOLDER = './static/files'
DOWNLOAD_FOLDER = './static/files'
ALLOWED_EXTENSIONS = ['pdf', 'png', 'jpg', 'jpeg']


def allowed_file(filename):
    return '.' in filename and \
           filename.split('.')[-1] in ALLOWED_EXTENSIONS


app = Flask(__name__)
app.config["SECRET_KEY"] = "hello hachapuri"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = DataBase("database/base.sqlite3")
db.create_tables()



exams_subjects = ["Русский язык", "Литература", "Алгебра", "Геометрия", "Информатика", "Музыка",
                      "ОБЖ", "Физическая культура", "Технология", "Английский язык", "Литература Республики Коми",
                      "История", "Родная (русская) литература", "Родной (русский) язык", "Биология",
                      "Химия", "Физика", "География", "Обществознание"]


# ________________________________________________HEADER_________________________________________________________________


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/info")
def info():
    return render_template("information.html", title="Information")

@app.route("/")
def index():
    if "teacher_id" in session:
        return redirect("classes")
    if "student_id" in session:
        return redirect("profile")
    return render_template("index.html", title="Port-Keeper")


@app.route("/support")
def support():
    return render_template("support.html", title="support")

# ___________________________________________________CONTENT_____________________________________________________________


@app.route("/teacher-login", methods=["GET", "POST"])
def teacher_login():
    if "teacher_id" in session:
        return redirect("classes")
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        login = form.login.data
        password = form.password.data
        teacher = db_sess.query(Teacher).filter(Teacher.login == login, Teacher.password == password).first()
        if teacher:
            session["teacher_id"] = teacher.id
            session["name"] = teacher.name
            return redirect(url_for("classes"))
    return render_template("teacher-login.html", form=form, title="Teacher Login")


@app.route("/student-login", methods=["GET", "POST"])
def student_login():
    form = LoginForm()
    if "teacher_id" in session:
        return redirect("classes")
    if "student_id" in session:
        return redirect("profile")
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        login = form.login.data
        password = form.password.data
        student = db_sess.query(Student).filter(Student.login == login, Student.password == password).first()
        if student:
            session["student_id"] = student.id
            session["name"] = student.name
            session["login"] = student.login
            session["birth-date"] = student.birth_date
            session["class"] = student.group
            return redirect(url_for("profile"))
    return render_template("student-login.html", form=form, title="Student Login")


@app.route("/classes", methods=["GET", "POST"])
def classes():
    if "teacher_id" not in session or "student_id" in session:
        return redirect("index")
    if request.method == "POST":
        db_sess = db_session.create_session()
        uploaded_file = request.files['file']
        img_bytes = uploaded_file.read()
        teacher = db_sess.query(Teacher).filter(Teacher.id == session["teacher_id"]).first()
        teacher.avatar = img_bytes
        db_sess.commit()
    teacher = db_sess.query(Teacher).filter(Teacher.id == session["teacher_id"]).first()
    students = db_sess.query(Student).filter(Student.teacher_id == teacher.id).all()

    return render_template("classes.html", students=students, title="Teacher profile", teacher=teacher)


@app.route("/classes/settings")
def settings():
    db_sess = db_session.create_session()
    students = db_sess.query(Student).filter(Student.teacher_id == session["teacher_id"])
    return render_template("settings.html", students=students, title="settings", )


@app.route("/delete_student/<string:student_id>")
def delete_student(student_id):
    db_sess = db_session.create_session()
    db_sess.query(Student).filter(Student.id == student_id).delete()
    db_sess.commit()
    return redirect(url_for("settings"))


@app.route("/profile/<student_id>", methods=["POST", "GET"])
def profile_by_id(student_id):
    db_sess = db_session.create_session()
    student = db_sess.query(Student).filter(Student.id == student_id).first()
    portfolio = db_sess.query(Portfolio).filter(Portfolio.student_id == student_id).all()
    exams = db_sess.query(Exam).filter(Exam.student_id == student_id).all()
    if request.method == "POST":
        db_sess.query(Exam).filter(Exam.student_id == student_id).delete()
        db_sess.commit()
        for i in range(1, 5):
            subject = request.form.get("exam" + str(i))
            mark = request.form.get("mark" + str(i))
            exam = Exam()
            exam.subject = subject
            exam.mark = mark
            exam.student_id = student_id
            db_sess.add(exam)
        db_sess.commit()
        exams = db_sess.query(Exam).filter(Exam.student_id == student_id).all()
        student = db_sess.query(Student).filter(Student.id == student_id).first()
    return render_template("student-profile.html", title="Student profile", student=student, port=portfolio,
                                                exams=exams, subjects=exams_subjects)


@app.route("/profile", methods=["POST", "GET"])
def profile():
    db_sess = db_session.create_session()
    student_id = session["student_id"]
    student = db_sess.query(Student).filter(Student.id == student_id).first()
    portfolio = db_sess.query(Portfolio).filter(Portfolio.student_id == student_id).all()
    exams = db_sess.query(Exam).filter(Exam.student_id == student_id).all()
    if request.method == "POST":
        if "exam1" in request.form.keys():
            db_sess.query(Exam).filter(Exam.student_id == student_id).delete()
            db_sess.commit()
            for i in range(1, 5):
                subject = request.form.get("exam" + str(i))
                mark = request.form.get("mark" + str(i))
                exam = Exam()
                exam.subject = subject
                exam.mark = mark
                exam.student_id = student_id
                db_sess.add(exam)
            db_sess.commit()
        else:
            uploaded_file = request.files['file']
            img_bytes = uploaded_file.read()
            student = db_sess.query(Student).filter(Student.id == session["student_id"]).first()
            student.avatar = img_bytes
            db_sess.commit()
        student = db_sess.query(Student).filter(Student.id == session["student_id"]).first()
        exams = db_sess.query(Exam).filter(Exam.student_id == student_id).all()
    return render_template("student-profile.html", title="Student profile", student=student, port=portfolio,
                                                exams=exams, subjects=exams_subjects)

@app.route("/add-student", methods=["POST", "GET"])
def add_student():
    form = AddStudents()
    if "teacher_id" in session:
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            student = Student()
            student.name = form.student_name.data
            student.login = generate_login(student.name)
            student.password = generate_password()
            student.teacher_id = session["teacher_id"]
            student.group = form.class_number.data
            db_sess.add(student)
            db_sess.commit()
            return redirect("classes")
    else:
        return redirect("index")
    return render_template("add-students.html", title="new student", form=form)


@app.route("/student_registration", methods=["POST", "GET"])
def student_registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        class_code = form.class_code.data
        login = form.login.data
        is_uniq_login = db.check_uniq_login(login)
        if not is_uniq_login:
            flash("Логин уже существует. Придумайте другой")
        else:
            pass
    return render_template("student_registration.html", title="registration", form=form)

@app.route("/teacher_registration", methods=["POST", "GET"])
def teacher_registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        class_code = form.class_code.data
        login = form.login.data
        is_uniq_login = db.check_uniq_login(login)
        if not is_uniq_login:
            flash("Логин уже существует. Придумайте другой")

    return render_template("teacher-registration.html", title="registration", form=form)

# ___________________________________________________FILES_______________________________________________________________

@app.route("/add-portfolio", methods=["POST", "GET"])
def add_port():
    if request.method == "POST":
        db_sess = db_session.create_session()
        name = request.form.get("name")
        level = request.form.get("level")
        subject = request.form.get("subject")
        date = ".".join(request.form.get("date").split("-")[::-1])
        result = request.form.get("result")
        uploaded_file = request.files["file"]

        file_expansion = "." + str(uploaded_file).split(".")[-1].split("'")[0]
        random_uuid = str(uuid.uuid4()) + file_expansion
        if uploaded_file and allowed_file(uploaded_file.filename):
            uploaded_file.save(os.path.join(UPLOAD_FOLDER, random_uuid))
            if file_expansion == ".pdf":
                uploaded_file = fitz.open(f"./static/files/{random_uuid}")
                for page in uploaded_file:
                    pdf_image = page.get_pixmap(matrix=fitz.Identity, dpi=None,
                                                colorspace=fitz.csRGB, clip=None, alpha=False, annots=True)
                pdf_image.save(os.path.join(UPLOAD_FOLDER, random_uuid.split(".")[0] + "-miniature.jpg"))
        port = Portfolio()
        port.name = name
        port.subject = subject
        port.student_id = int(session["student_id"])
        port.level = level
        port.file_uuid = random_uuid
        port.result = result
        port.date = date
        db_sess.add(port)
        return redirect(url_for("profile"))

    return render_template("port-add-item.html", title="Add portfolio")


@app.route("/download/<string:file_uuid>")
def download_file(file_uuid):
    if "teacher_id" in session or "student_id" in session:
        filename = file_uuid
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)


@app.route("/profile/download-all/<string:student_id>")
def download_zip(student_id):
    if "teacher_id" in session or "student_id" in session:
        db_sess = db_session.create_session()
        portfolio = db_sess.query(Portfolio).filter(Portfolio.student_id == student_id).all()
        archive = file_zipping(portfolio)
        zip_sender = send_from_directory(DOWNLOAD_FOLDER, archive, as_attachment=True)
        zip_delete(archive)
        return zip_sender


@app.route("/document/<string:filename>")
def show_document(filename):
    db_sess = db_session.create_session()
    is_exist = db_sess.query(Portfolio).filter(Portfolio.file_uuid == filename)
    exp = filename.split(".")[1]
    if is_exist:
        h = make_response(open("./static/files/" + filename, "rb"))
        if exp == "pdf":
            h.headers['Content-Type'] = 'files/pdf'
        else:
            h.headers['Content-Type'] = "image/jpeg"
        return h
    abort(404)


@app.route("/show_api_document/<h>")
def show_api_document(h):
    return h

@app.route("/user_avatar")
def user_avatar():
    db_sess = db_session.create_session()
    if "teacher_id" in session:
        current_user = db_sess.query(Teacher).filter(Teacher.id == session["teacher_id"]).first()
        img = current_user.avatar
    if "student_id" in session:
        current_user = db_sess.query(Student).filter(Student.id == session["student_id"]).first()
        img = current_user.avatar
    if not img:
        return ""
    h = make_response(img)
    h.headers['Content-Type'] = 'image/jpg'
    return h


@app.route("/student_avatar/<string:student_id>")
def student_avatar(student_id):
    db_sess = db_session.create_session()
    current_user = current_user = db_sess.query(Student).filter(Student.id == student_id).first()
    img = current_user.avatar
    if not img:
        return ""
    h = make_response(img)
    h.headers['Content-Type'] = 'image/jpg'
    return h


@app.route("/teacher_avatar/<string:teacher_id>")
def teacher_avatar(teacher_id):
    db_sess = db_session.create_session()
    current_user = db_sess.query(Teacher).filter(Teacher.id == session["teacher_id"]).first()
    img = current_user.avatar
    if not img:
        return ""
    h = make_response(img)
    h.headers['Content-Type'] = 'image/jpg'
    return h


# _______________________________________________________________________________________________________________________


if __name__ == "__main__":
    app.register_blueprint(site_api.blueprint)
    db_session.global_init("db/database.db")
    app.run(debug=True)
