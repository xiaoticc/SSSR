from flask import Flask, request, json, render_template
from data import db_session
from data.db_session import User
import os
# class LoginForm(FlaskForm):
#     username = StringField('Логин', validators=[DataRequired()])
#     password = PasswordField('Пароль', validators=[DataRequired()])
#     remember_me = BooleanField('Запомнить меня')
#     submit = SubmitField('Войти')
# ура база данных подключена
db_session.global_init("db/data.db")
db_sess = db_session.create_session()
# добавление юсеров
# user = User()
# user.name = "Пользователь 1"
# user.surname = "йоаймо"
# user.email = "email@email.ru"
# db_sess = db_session.create_session()
# db_sess.add(user)
# db_sess.commit()
# user2 = User()
# user2.name = "Пользователь 2"
# user2.surname = "йоаймо"
# user2.email = "mail@email.ru"
# db_sess = db_session.create_session()
# db_sess.add(user2)
# db_sess.commit()

# сортировка юсеров
# for user in db_sess.query(User).all():
#     print(user)
# for user in db_sess.query(User).filter((User.id > 1) | (User.email.notilike("%1%"))):
#     print(user)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SuperSecretKey'


# app.debug = True


# # СОЗДАТЬ ДБ
# @app.route('/')
# def index():
#     return render_template('html/carousel.html')
#
#
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         return render_template('html/sidebar.html')
#     return render_template('html/register.html', form=form)


@app.route("/")
def home():
    # return render_template('html/carousel.html')
    return render_template('carousel.html')


@app.route("/signin", methods=['POST'])
def signin():
    global db_sess
    email = request.form['username']
    password = request.form['password']
    if email and password:
        db_sess = db_session.create_session()
        for user in db_sess.query(User).filter((User.email == email)):
            print(user.hashed_password, User.check_password(user, password))
            if User.check_password(user, password):
                validateUser(email, password)
                print(user.name)
                return render_template('secondvers.html')

        # return json.dumps({'validation' : validateUser(username, password)})
    # тут надо сделать чтобы при неправильном вводе данных или если вовсе учетной записи нет чтобы писало обэтом красным
            else:
                return json.dumps({'validation': False})  # временно


@app.route("/register", methods=['POST'])
def register():
    global db_sess
    email = request.form['username']
    password = request.form['password']
    name = request.form['name']
    surname = request.form['surname']
    if email and password and name and surname:
        user = User()
        user.name = name
        user.surname = surname
        user.email = email
        for users in db_sess.query(User).filter(User.email == email):
            if users:
                return json.dumps({'validation': False})
        user.password = User.set_password(user, password)
        # db_sess = db_session.create_session()
        db_sess.add(user)
        db_sess.commit()
        validateregisterUser(email, password, name, surname)
        return render_template('secondvers.html')
        # return json.dumps({'validation' : validateUser(username, password)})
    # тут надо сделать чтобы при неправильном вводе данных или если вовсе учетной записи нет чтобы писало обэтом красным
    else:
        return json.dumps({'validation': False})  # временно


def validateUser(username, password):
    print(username)
    print(password)
    return True


def validateregisterUser(username, password, name, surname):
    print(username)
    print(password)
    print(name)
    print(surname)
    return True


@app.route('/sign')
def sign():
    return render_template('signin.html')


@app.route('/reg')
def reg():
    return render_template('register.html')


@app.route('/search_main')
def search_main():
    return render_template('search_main.html')


@app.route('/like')
def like():
    return render_template('.html')


@app.route('/main')
def main():
    return render_template('secondvers.html')


@app.route('/log_out')
def log_out():
    return render_template('carousel.html')


@app.route('/studio')
def studio():
    return render_template('studio.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    file_audio = request.files['audio_file']
    track_name = request.form['track_name']
    artist = request.form['artist']
    file_cover = request.files['cover_file']
    print(os.path.dirname(__file__))
    print(os.path.join(os.path.dirname(__file__), '..'))
    print(os.path.dirname(os.path.realpath(__file__)))
    print(os.path.abspath(os.path.dirname(__file__)))
    if file_cover and artist and track_name and file_audio:
        # filename = file_audio.filename
        # file_audio.save(os.path.join(os.path.dirname(__file__), str(artist + "_" + track_name + ".mp3")))
        # file_cover.save(os.path.join(os.path.dirname(__file__), str(artist + "_" + track_name + ".jpeg")))
        file_audio.save(os.path.join(str(os.path.dirname(__file__) + "/static/other/Audio"), str(artist + "_" + track_name + ".mp3")))
        file_cover.save(os.path.join(str(os.path.dirname(__file__) + "/static/other/Cover"), str(artist + "_" + track_name + ".jpeg")))
        return render_template('secondvers.html')
    else:
        return render_template('carousel.html')


@app.route('/sssr')
def sssr_main():
    return render_template('carousel.html')
    # return render_template('player.html')  # пока что эта страница но потом должна быть та что выше строчкой


if __name__ == '__main__':
    app.run(port=8000)
