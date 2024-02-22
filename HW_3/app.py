from flask import Flask, flash, redirect, render_template, request, url_for, session
from werkzeug.security import check_password_hash
from HW_3.templates.models import db, User
from flask_wtf.csrf import CSRFProtect
from HW_3.templates.forms import LoginForm
from HW_3.templates.forms import RegistrationForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///mydatabase.db"
db.init_app(app)
app.config['SECRET_KEY'] = b'34ba3b91fd4e0b45042d9a8f1fdad7510e2e86bb4ad599b58dde826c13eabe45'
csrf = CSRFProtect(app)


@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('OK')


# @app.cli.command("add-user")
def add_user(name, surname, email, password):
    user = User(user_name=name, user_surname=surname, email=email, user_password=password)
    db.session.add(user)
    db.session.commit()
    print("User added to database!")


@app.cli.command("edit-user")
def edit_user():
    user = User.query.filter_by(username='FirstUser').first()
    user.email = 'new_email@example.com'
    db.session.commit()
    print('Edit FirstUser mail in DB!')


@app.cli.command("del-user")
def del_user():
    user = User.query.filter_by(username='FirstUser').first()
    db.session.delete(user)
    db.session.commit()
    print('Delete FirstUser from DB!')


@app.route('/')
def greetings():
    return redirect('login')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data

        # Поиск пользователя в базе данных по email
        user = User.query.filter_by(email=email).first()

        if user:
            # Проверка соответствия пароля
            if check_password_hash(user.user_password, password):
                # Установка сеанса для пользователя
                session['user_id'] = user.id
                flash('Вы успешно вошли в систему!', 'success')
                return redirect(url_for('congratulations'))
            else:
                flash('Неправильный email или пароль.', 'danger')
        else:
            flash('Пользователь с таким email не найден.', 'danger')

    return render_template('login.html', form=form)


@app.route('/logout/')
def logout():
    session.pop('username', None)
    return redirect(url_for("login"))


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if request.method == 'POST' and form.validate():
        # Обработка данных из формы
        name = form.name.data
        surname = form.surname.data
        email = form.email.data
        password = form.password.data
        add_user(name, surname, email, password)
        return render_template('login.html', form=form)
    # !!! после успешной регистрации возвращаем форму для авторизации на сайте
    return render_template('register.html', form=form)


@app.route('/congratulations/')
def congratulations():
    # Получаем идентификатор пользователя из сессии
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    context = {'title': 'congratulations', 'username': user.user_name}
    return render_template('congratulations.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
