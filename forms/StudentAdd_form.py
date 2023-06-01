from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class AddStudents(FlaskForm):
    student_name = StringField(validators=[DataRequired()])
    submit = SubmitField("Добавить ученика")