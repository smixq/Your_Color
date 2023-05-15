from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, EmailField, StringField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email('Неверно введённый email'), Length(min=6)])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
