import datetime
import random

from flask import Flask, render_template, redirect, request, make_response
from flask_login import LoginManager, login_user, login_required, logout_user, \
    current_user
from sqlalchemy import func

from data import db_session
from data.liked_palettes import Liked_palettes
from data.saved_palettes import Saved_plattes
from data.user import User
from form.login import LoginForm
from form.profile import ProfileForm
from form.register import RegisterForm

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
    return render_template("generate_palettes.html", **params)


@app.route("/delete-palettes", methods=['POST'])
@login_required
def delete_palettes():
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()

    if request.method == 'POST':
        if request.method == 'POST':
            data = request.json
            if data:
                palette = db_sess.query(Saved_plattes).filter(
                    Saved_plattes.id == data['id_palettes']).first()
                db_sess.delete(palette)
                db_sess.commit()

    return ''


@app.route("/save-palette", methods=['POST'])
@login_required
def add_favourite():
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    if request.method == 'POST':
        if request.method == 'POST':
            data = request.json
            if data:
                plattes = Saved_plattes()
                user_id = data['user_id']
                colors = ''.join(data['colors'])
                if data['is_del']:
                    user = db_sess.query(Saved_plattes).filter(
                        Saved_plattes.id_user == user_id).filter(
                        Saved_plattes.colors == ''.join(data['colors'])).first()
                    db_sess.delete(user)
                    db_sess.commit()
                else:
                    plattes.colors = colors
                    plattes.id_user = int(user_id)
                    db_sess.add(plattes)
                    db_sess.commit()
    return ''


@app.route("/liked_palettes", methods=['POST'])
@login_required
def liked_palettes():
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    if request.method == 'POST':
        data = request.json
        if data:
            liked_palette = Liked_palettes()
            id_palette = data['id_palette']
            user_id = data['user_id']
            if data['is_del']:
                id_entry = db_sess.query(Liked_palettes).filter(
                    Liked_palettes.id_user == current_user.id).filter(
                    Liked_palettes.id_palette == id_palette).first()
                db_sess.delete(id_entry)
                db_sess.commit()
            else:
                liked_palette.id_palette = id_palette
                liked_palette.id_user = user_id
                db_sess.add(liked_palette)
                db_sess.commit()
    return ''


@app.route("/saved")
@login_required
def saved():
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    palettes = db_sess.query(Saved_plattes).filter(Saved_plattes.id_user == user.id).all()
    colors_hash = []
    pallets_ids = []
    flag = False
    for color in palettes:
        pallets_ids.append(color.id)
        if color.colors.split('#'):
            colors_hash.append(color.colors.split('#')[1:])
            flag = True
    if flag:
        length = len(colors_hash[0])
    else:
        length = 0
    return render_template("saved.html", colors_hash=colors_hash, palettes_ids=pallets_ids,
                           len_colors=len(colors_hash), len_colors_elements=length)


@app.route("/best")
def best():
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    saved_palette = db_sess.query(Saved_plattes).filter(
        Saved_plattes.date >= datetime.datetime.now() - datetime.timedelta(days=7)).all()
    liked_palette = db_sess.query(Liked_palettes).filter(
        Liked_palettes.id_user == current_user.id).all()

    # count = db_sess.query(Liked_palettes).group_by(Liked_palettes.id_palette)
    count = db_sess.query(func.count(Liked_palettes.id_palette),
                          Liked_palettes.id_palette).group_by(Liked_palettes.id_palette).all()
    count_liked_palettes = {}

    for i in count:
        count_liked_palettes[int(i[1])] = i[0]
    palettes_liked = []
    for like_pal in liked_palette:
        palettes_liked.append(int(like_pal.id_palette))
    palettes_ids = {}
    flag = False
    for i in range(20):
        random_int = random.randint(0, len(saved_palette))
        palettes_ids[saved_palette[random_int].id] = saved_palette[i].colors.split('#')[1:]

    return render_template("best.html", palettes_ids=palettes_ids, liked_paletes=palettes_liked,
                           count_liked_palettes=count_liked_palettes)



@ app.route('/userava')
@ login_required
def userava():
    img = current_user.avatar
    if not img:
        return ""

    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h


@app.route("/profile", methods=['GET', 'POST'])
@login_required
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
