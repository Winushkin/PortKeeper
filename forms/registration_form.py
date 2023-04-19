from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length

class RegistrationForm(FlaskForm):
    class_code = StringField("Код вашего класса", validators=[DataRequired()])
    login = StringField("Придумайте логин", validators=[DataRequired()])
    password = PasswordField("Придумайте пароль", validators=[DataRequired(), Length(min=7, message="Пароль должен быть длиннее 7 символов")])
    password2 = PasswordField("Подтвердите пароль", validators=[DataRequired(), EqualTo('password', message="Пароли не совпадают")])
    submit = SubmitField("Зарегистрироваться")
