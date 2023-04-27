from flask import Flask, render_template, redirect, request, abort, url_for
from data import db_session
from data.favourites import Favourites
from data.users import User
from data.products import Products
from forms.user import RegisterForm, LoginForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
itemdata = []


def main():
    global itemData
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    itemData = db_sess.query(Products).all()
    app.run()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    return render_template("product_view.html", itemData=db_sess.query(Products).all(), title="интернет-магазин")


@app.route("/<category>", methods=['GET', 'POST'])
def category(category):
    db_sess = db_session.create_session()
    itemDat = db_sess.query(Products).filter(Products.category == category).all()
    return render_template("product_view.html", itemData=itemDat, title="интернет-магазин")


@app.route("/book/<book_name>", methods=['GET', 'POST'])
def book_page(book_name):
    db_sess = db_session.create_session()
    img = db_sess.query(Products).filter(Products.name == book_name).first().image
    desc = db_sess.query(Products).filter(Products.name == book_name).first().description
    author = db_sess.query(Products).filter(Products.name == book_name).first().author
    if current_user.is_authenticated:
        if db_sess.query(Favourites).filter(Favourites.user_id == current_user.id,
                                            Favourites.book_name == book_name).first():
            return render_template('del.html', title='страница книги', book_name=book_name, book_image=img,
                                   description=desc, author=author)
        return render_template('favourite.html', title='страница книги', book_name=book_name, book_image=img,
                               description=desc, author=author)
    return render_template('book_page.html', title='страница книги', book_name=book_name, book_image=img,
                           description=desc, author=author)


@app.route("/favorite_book")
def favorite_book():
    db_sess = db_session.create_session()
    fav_books = db_sess.query(Products).filter(Products.favourites, Favourites.user_id == current_user.id)
    return render_template('favorite_book.html', title='Избранное', fav_books=fav_books)


@app.route("/book/<book_name>/fav", methods=['GET', 'POST'])
def add_fav(book_name):
    favourite = Favourites()
    favourite.user_name = current_user.name
    favourite.book_name = book_name
    favourite.user_id = current_user.id
    db_sess = db_session.create_session()
    db_sess.add(favourite)
    db_sess.commit()

    img = db_sess.query(Products).filter(Products.name == book_name).first().image
    desc = db_sess.query(Products).filter(Products.name == book_name).first().description
    author = db_sess.query(Products).filter(Products.name == book_name).first().author
    if db_sess.query(Favourites).filter(Favourites.user_id == current_user.id,
                                        Favourites.book_name == book_name).first():
        return render_template('del.html', title='страница книги', book_name=book_name, book_image=img,
                               description=desc, author=author)
    return render_template('favourite.html', title='страница книги', book_name=book_name, book_image=img,
                           description=desc, author=author)


@app.route("/book/<book_name>/del", methods=['GET', 'POST'])
def del_fav(book_name):
    print(3412)
    db_sess = db_session.create_session()
    img = db_sess.query(Products).filter(Products.name == book_name).first().image
    desc = db_sess.query(Products).filter(Products.name == book_name).first().description
    author = db_sess.query(Products).filter(Products.name == book_name).first().author
    db_sess.query(Favourites).filter(Favourites.user_id == current_user.id,
                                     Favourites.book_name == book_name).delete()
    db_sess.commit()
    return render_template('favourite.html', title='страница книги', book_name=book_name, book_image=img,
                           description=desc, author=author)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form, itemdata=itemdata)
    return render_template('login.html', title='Авторизация', form=form, itemData=itemdata)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают", itemdata=itemdata)
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть", itemdata=itemdata)
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form, itemdata=itemdata)


if __name__ == '__main__':
    main()
