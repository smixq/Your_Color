import datetime
import random

from flask import Flask, render_template, redirect, request, make_response, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, \
    current_user
from sqlalchemy import func
from blueprints import random_palettes
from data import db_session
from data.liked_palettes import Liked_palettes
from data.saved_palettes import Saved_plattes
from data.user import User
from form.login import LoginForm
from form.profile import ProfileForm
from form.register import RegisterForm
from flask import make_response
from data.img import resize_img

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asffsdfSDFASFKJFSADHFGJSDJFG'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


def main():
    db_session.global_init("db/blogs.db")
    app.register_blueprint(random_palettes.blueprint)
    app.run()


@app.route("/")
def index():
    return render_template("generate_palettes.html")

@app.route("/about-us")
def about_us():
    return render_template("about_us.html")


@app.route("/delete-palettes", methods=['POST'])
@login_required
def delete_palettes():
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()

    if request.method == 'POST':
        if request.method == 'POST':
            data = request.json
            if data:

                saved_palette = db_sess.query(Saved_plattes).filter(
                    Saved_plattes.id == data['id_palettes']).first()
                liked_palette = db_sess.query(Liked_palettes).filter(
                    Liked_palettes.id_palette == data['id_palettes']).first()
                if liked_palette:
                    db_sess.delete(liked_palette)
                db_sess.delete(saved_palette)

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


@app.route("/fresh")
def fresh():
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    saved_palette = db_sess.query(Saved_plattes).filter(
        Saved_plattes.date >= datetime.datetime.now() - datetime.timedelta(days=7)).all()

    count = db_sess.query(func.count(Liked_palettes.id_palette),
                          Liked_palettes.id_palette).group_by(Liked_palettes.id_palette).all()
    count_liked_palettes = {}

    for i in count:
        count_liked_palettes[int(i[1])] = i[0]
    palettes_liked = []

    palettes_ids = {}
    repeated = []
    if len(saved_palette) >= 20:
        quantity = 20
    else:
        quantity = len(saved_palette)
    for i in range(quantity):
        random_int = random.randint(0, len(saved_palette) - 1)
        while random_int in repeated:
            random_int = random.randint(0, len(saved_palette) - 1)
        repeated.append(random_int)
        palettes_ids[saved_palette[random_int].id] = saved_palette[random_int].colors.split('#')[1:]
    if current_user.is_authenticated:
        liked_palette = db_sess.query(Liked_palettes).filter(
            Liked_palettes.id_user == current_user.id).all()
        for like_pal in liked_palette:
            palettes_liked.append(int(like_pal.id_palette))

    return render_template("fresh.html", palettes_ids=palettes_ids, liked_paletes=palettes_liked,
                           count_liked_palettes=count_liked_palettes)


@app.route("/best")
def best():
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()

    palettes = db_sess.query(func.count(Liked_palettes.id_palette),
                             Liked_palettes.id_palette).group_by(Liked_palettes.id_palette).all()
    count_liked_palettes = {}
    for i in palettes:
        count_liked_palettes[int(i[1])] = i[0]
    count_liked_palettes = dict(sorted(count_liked_palettes.items(), key=lambda item: -item[1]))
    palettes_liked = []

    palettes_ids = {}
    saved_palette = db_sess.query(Saved_plattes).filter(Saved_plattes.id.in_(count_liked_palettes.keys())).all()
    if len(count_liked_palettes.keys()) >= 20:
        quantity = 20
    else:
        quantity = len(count_liked_palettes.keys())
    for i in range(quantity):
        color_palette = ''
        for el in saved_palette:
            if el.id == list(count_liked_palettes.keys())[i]:
                color_palette = el.colors.split('#')[1:]
        palettes_ids[list(count_liked_palettes.keys())[i]] = color_palette
    if current_user.is_authenticated:
        liked_palette = db_sess.query(Liked_palettes).filter(
            Liked_palettes.id_user == current_user.id).all()
        for like_pal in liked_palette:
            palettes_liked.append(int(like_pal.id_palette))
    return render_template("best.html", palettes_ids=palettes_ids, liked_paletes=palettes_liked,
                           count_liked_palettes=count_liked_palettes)


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
            avatar = resize_img(file.read())
            user.avatar = avatar

            db_sess.commit()

    return render_template('profile.html', title='Профиль', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if not current_user.is_authenticated:
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
    else:
        return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    if not current_user.is_authenticated:
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
    else:
        return redirect('/')


if __name__ == '__main__':
    main()
