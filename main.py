import os
import uuid

import fitz
from flask import Flask, render_template, redirect, session, request, send_from_directory, url_for
from forms.login_form import LoginForm
from database import DataBase
from forms.StudentAdd_form import AddStudents
from added_files.login_generator import generate_login
from added_files.password_generator import generate_password
from added_files.zipper import file_zipping, zip_delete


UPLOAD_FOLDER = './static/files'
DOWNLOAD_FOLDER = './static/files'
ALLOWED_EXTENSIONS = ['pdf', 'png', 'jpg', 'jpeg']

app = Flask(__name__)
app.config["SECRET_KEY"] = "q1w2e3r4t5y"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = DataBase("base.sqlite3")
db.create_tables()

def allowed_file(filename):
    return '.' in filename and \
           filename.split('.')[-1] in ALLOWED_EXTENSIONS


@app.route("/")
@app.route('/index')
def index():
    if "teacher_id" in session:
        return redirect("classes")
    if "student_id" in session:
        return redirect("profile")
    return render_template("index.html", title="Port-Keeper")

@app.route('/logout')
def logout():
    session.clear()
    return redirect("index")


@app.route("/teacher-login", methods=["GET", "POST"])
def teacher_login():
    if "teacher_id" in session:
        return redirect("classes")
    form = LoginForm()
    if form.validate_on_submit():
        name = form.login.data
        password = form.password.data
        teacher = db.get_teacher(name, password)
        if teacher:
            session["teacher_id"] = teacher[0]
            session["login"] = teacher[1]
            session["avatar"] = teacher[3]
            session["post"] = "учитель информатики"
            return redirect("classes")
    return render_template("teacher-login.html", form=form, title="Teacher Login")


@app.route("/student-login", methods=["GET", "POST"])
def student_login():
    form = LoginForm()
    if "teacher_id" in session:
        return redirect("classes")
    if "student_id" in session:
        return redirect("profile")
    if form.validate_on_submit():
        login = form.login.data
        password = form.password.data
        student = db.get_student(login, password)
        if student:
            session["student_id"] = student[0]
            session["login"] = student[1]
            session["avatar"] = student[3]
            session["class"] = student[6]
            return redirect(url_for("profile"))
    return render_template("student-login.html", form=form, title="Student Login")


@app.route("/classes")
def classes():
    if "teacher_id" not in session:
        return redirect("index")
    students = db.get_students_by_teacher_id(session["teacher_id"])
    return render_template("classes.html", students=students, title="Teacher profile")


@app.route("/profile/<student_id>", methods=["POST", "GET"])
def profile_by_id(student_id):
    exams_subjects = ["Русский язык", "Литература", "Алгебра", "Геометрия", "Информатика", "Музыка",
                      "ОБЖ", "Физическая культура", "Технология", "Английский язык", "Литература Республики Коми",
                      "История", "Родная (русская) литература", "Родной (русский) язык", "Биология",
                      "Химия", "Физика", "География", "Обществознание"]
    student = db.get_student_by_student_id(student_id)
    portfolio = db.get_portfolio_by_student_id(student_id)
    exams = db.get_exams_by_student_id(student_id)
    if request.method == "POST":
        db.update_students_novelty(student_id)
        db.delete_exams(student_id)
        for i in range(1, 5):
            subject = request.form.get("exam" + str(i))
            mark = request.form.get("mark" + str(i))
            db.insert_exams(subject, mark, student_id)
        exams = db.get_exams_by_student_id(student_id)
        student = db.get_student_by_student_id(student_id)
    return render_template("student-profile.html", title="Student profile", student=student, port=portfolio,
                                                exams=exams, subjects=exams_subjects, old = student[-1], N=None)


@app.route("/profile", methods=["POST", "GET"])
def profile():
    exams_subjects = ["Русский язык", "Литература", "Алгебра", "Геометрия", "Информатика", "Музыка",
                      "ОБЖ", "Физическая культура", "Технология", "Английский язык", "Литература Республики Коми",
                      "История", "Родная (русская) литература", "Родной (русский) язык", "Биология",
                      "Химия", "Физика", "География", "Обществознание"]
    student_id = session["student_id"]
    student = db.get_student_by_student_id(student_id)
    portfolio = db.get_portfolio_by_student_id(student_id)
    exams = db.get_exams_by_student_id(student_id)
    if request.method == "POST":
        db.update_students_novelty(student_id)
        db.delete_exams(student_id)
        for i in range(1, 5):
            subject = request.form.get("exam" + str(i))
            mark = request.form.get("mark" + str(i))
            db.insert_exams(subject, mark, student_id)
        exams = db.get_exams_by_student_id(student_id)
        student = db.get_student_by_student_id(student_id)
    return render_template("student-profile.html", title="Student profile", student=student, port=portfolio,
                                                exams=exams, subjects=exams_subjects, old=student[-1], N=None)


@app.route("/info")
def info():
    return render_template("information.html", title="Information")


@app.route("/add-portfolio", methods=["POST", "GET"])
def add_port():
    if request.method == "POST":
        name = request.form.get("name")
        level = request.form.get("level")
        subject = request.form.get("subject")
        date = request.form.get("date")
        result = request.form.get("result")
        uploaded_file = request.files["file"]
        file_expansion = "." + str(uploaded_file).split(".")[-1].split("'")[0]
        random_uuid = str(uuid.uuid4()) + file_expansion

        if uploaded_file and allowed_file(uploaded_file.filename):
            uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], random_uuid))
            if file_expansion == ".pdf":
                uploaded_file = fitz.open(f"./static/files/{random_uuid}")
                for page in uploaded_file:
                    pdf_image = page.get_pixmap(matrix=fitz.Identity, dpi=None,
                                          colorspace=fitz.csRGB, clip=None, alpha=True, annots=True)
                pdf_image.save(os.path.join(app.config['UPLOAD_FOLDER'], random_uuid.split(".")[0] + "-miniature.jpg"))


            db.insert_portfolio(name, subject, int(session["student_id"]), random_uuid, level, result, date)
            return redirect(url_for("profile"))

    return render_template("port-add-item.html", title="Add portfolio")


@app.route("/support")
def support():
    return render_template("support.html", title="support")


@app.route("/add-student", methods=["POST", "GET"])
def add_student():
    form = AddStudents()
    if "teacher_id" in session:
        if form.validate_on_submit():
            name = form.student.data
            login = generate_login(name)
            class_num = form.class_number.data
            password = generate_password()
            db.insert_student(name, login, password, session["teacher_id"], class_num, 0)
            return redirect("classes")
    else:
        return redirect("index")
    return render_template("add-students.html", title="new student", form=form)

@app.route("/download/<string:file_uuid>")
def download_file(file_uuid):
    if "teacher_id" in session or "student_id" in session:
        filename = file_uuid
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)


@app.route("/profile/download-all/<string:student_id>")
def download_zip(student_id):
    if "teacher_id" in session or "student_id" in session:
        portfolio = db.get_portfolio_by_student_id(student_id)
        archive = file_zipping(portfolio)
        zip_sender = send_from_directory(DOWNLOAD_FOLDER, archive, as_attachment=True)
        zip_delete(archive)
        return zip_sender

if __name__ == "__main__":
    app.run(debug=True)
