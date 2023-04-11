from flask import Flask, render_template, redirect, request, make_response, \
    session

from data import db_session
from form.login import LoginForm
from form.register import RegisterForm
from form.profile import ProfileForm
from flask_login import LoginManager, login_user, login_required, logout_user, \
    current_user
from data.user import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asffsdfSDFASFKJFSADHFGJSDJFG'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def main():
    db_session.global_init("db/blogs.db")
    app.run(debug=True)


@app.route("/")
def index():
    params = {'link': 'css/styles_for_generate_plattes.css'}
    return render_template("generate_plattes.html", **params)


@app.route('/userava')
@login_required
def userava():
    img = current_user.avatar
    if not img:
        return ""

    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h


@app.route("/profile", methods=['GET', 'POST'])
def profile():
    form = ProfileForm()
    if form.validate_on_submit():

        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        if form.password.data:
            if form.password.data != form.password_again.data:
                return render_template('profile.html', title='Регистрация',
                                       form=form,
                                       message="Пароли не совпадают")

            user.set_password(form.password.data)
            db_sess.commit()
        file = form.avatar.data
        if file:
            user.avatar = file.read()
            db_sess.commit()



    return render_template('profile.html', title='Профиль', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(
            User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


if __name__ == '__main__':
    main()
