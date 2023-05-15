from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, EmailField, StringField
from wtforms.validators import DataRequired, Length, Email


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired(), Email('Неверно введённый email'), Length(min=6)])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')
