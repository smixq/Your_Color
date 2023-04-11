from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField
from wtforms.validators import DataRequired


class ProfileForm(FlaskForm):
    password = PasswordField('Пароль')
    password_again = PasswordField('Повторите пароль')
    avatar = FileField('Выберете файл для аватара')
    submit = SubmitField('Подтвердить')
