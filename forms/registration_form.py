from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, NoneOf
from database import DataBase

db = DataBase("database/base.sqlite3")
db.create_tables()

login_list = [x for x in db.get_logins("students") + db.get_logins("teachers")]

class RegistrationForm(FlaskForm):
    class_code = StringField("Код вашего класса", validators=[DataRequired()])
    login = StringField("Придумайте логин", validators=[DataRequired(), NoneOf(login_list, message="логин уже занят")])
    password = PasswordField("Придумайте пароль", validators=[DataRequired(), Length(min=7, message="Пароль должен быть длиннее 7 символов")])
    password2 = PasswordField("Подтвердите пароль", validators=[DataRequired(), EqualTo('password', message="Пароли не совпадают")])
    submit = SubmitField("Зарегистрироваться")
