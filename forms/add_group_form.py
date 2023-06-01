from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class AddGroup(FlaskForm):
    name = StringField(validators=[DataRequired()])
    submit = SubmitField("Войти")

