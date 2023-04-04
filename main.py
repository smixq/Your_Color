from flask import Flask, render_template, redirect, request, make_response, session

from data import db_session
# from form.login import LoginForm
# from form.register import RegisterForm
from flask_login import LoginManager, login_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asffsdfSDFASFKJFSADHFGJSDJFG'


def main():
    db_session.global_init("db/blogs.db")
    app.run(debug=True)


@app.route("/")
def index():
    params = {'link': 'css/styles_for_generate_plattes.css'}
    return render_template("generate_plattes.html", **params)

    
if __name__ == '__main__':
    main()
