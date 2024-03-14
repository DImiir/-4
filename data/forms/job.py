import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, IntegerField, BooleanField
from wtforms.validators import InputRequired


class JobForm(FlaskForm):
    team_leader = IntegerField('ID капитана')
    job = StringField('Название', validators=[InputRequired()])
    work_size = IntegerField('Объём работы')
    collaborators = StringField('Соучастники')
    start_date = DateTimeField('Дата начала', default=datetime.datetime.now)
    end_date = DateTimeField('Дата конца')
    is_finished = BooleanField('Завершённость', default=False)
    submit = SubmitField('submit')