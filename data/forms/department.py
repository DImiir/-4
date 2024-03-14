from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, EmailField
from wtforms.validators import InputRequired


class DepartmentForm(FlaskForm):
    title = StringField('Название')
    chief = IntegerField('Главный')
    members = StringField('Работники')
    email = EmailField('Почта', validators=[InputRequired()])
    submit = SubmitField('submit')
