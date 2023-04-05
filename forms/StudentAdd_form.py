from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class AddStudents(FlaskForm):
    student = StringField(validators=[DataRequired()])
    class_number = StringField(validators=[DataRequired()])
    submit = SubmitField("Добавить ученика")