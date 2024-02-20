from flask import Flask, flash, redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import session

app = Flask(__name__)
app.secret_key = b'5f214cacbd30c2ae4784b520f17912ae0d5d8c16ae98128e3f549546221265e4'


@app.route('/')
def greetings():
    salute = 'Уважаемый пользователь!'
    if 'username' in session:
        salute = f'Привет, {session["username"]}!'
    context = {'title': 'index',
               'message': salute}
    return render_template('index.html', **context)


@app.post('/hello/')
def hello():
    user_name = f'Пользователь: {request.form.get("name")}!'
    email = f'Электронная почта: {request.form.get("email")}'
    context = {'title': 'hello',
               'username': user_name,
               'usermail': email}
    if request.method:
        session['username'] = request.form.get('name') or 'NoName'
        # Проверка данных формы
        if not request.form['name']:
            flash('Введите имя!', 'danger')
        if not request.form['email']:
            flash('Введите email!', 'danger')
            return redirect(url_for("greetings"))
        # Обработка данных формы
        # flash('Форма успешно отправлена!', 'success')
        # return redirect(url_for("greetings"))
    return render_template('hello.html', **context)


@app.route('/logout/')
def logout():
    session.pop('username', None)
    return redirect(url_for("greetings"))


if __name__ == '__main__':
    app.run(debug=True)
