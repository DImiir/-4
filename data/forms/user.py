import datetime
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, DateTimeField, IntegerField, BooleanField
from wtforms.validators import InputRequired


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[InputRequired()])
    password = PasswordField('Пароль', validators=[InputRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    surname = StringField('Фамилия')
    name = StringField('Имя')
    age = IntegerField('Возраст')
    position = StringField('Должность')
    speciality = StringField('Профессия')
    address = StringField('Адрес')
    email = EmailField('Почта', validators=[InputRequired()])
    hashed_password = PasswordField('Пароль', validators=[InputRequired()])
    modified_date = DateTimeField('Дата изменения', default=datetime.datetime.now())
    submit = SubmitField('submit')
