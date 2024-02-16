from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
@app.route('/index/')
def index():
    context = {'title': 'Главная'}
    return render_template('index.html', **context)


@app.route('/about/')
def about():
    context = {'title': 'О нас'}
    return render_template('about.html', **context)


@app.route('/contacts/')
def contacts():
    context = {'title': 'Контакты'}
    return render_template('contacts.html', **context)


@app.route('/delivery/')
def delivery():
    context = {'title': 'Доставка'}
    return render_template('delivery.html', **context)


@app.route('/pay/')
def pay():
    context = {'title': 'Оплата'}
    return render_template('pay.html', **context)


@app.route('/shoes/')
def shoes():
    context = {'title': 'Обувь'}
    return render_template('shoes.html', **context)


@app.route('/jeans/')
def jeans():
    context = {'title': 'Джинсы'}
    return render_template('jeans.html', **context)


@app.route('/mensport/')
def mensport():
    context = {'title': 'Мужчинам'}
    return render_template('mensport.html', **context)


@app.route('/womansport/')
def womansport():
    context = {'title': 'Женщинам'}
    return render_template('womansport.html', **context)


@app.route('/kidsport/')
def kidsport():
    context = {'title': 'Детям'}
    return render_template('kidsport.html', **context)


@app.route('/coat/')
def coat():
    context = {'title': 'Пальто'}
    return render_template('coat.html', **context)


@app.route('/shirts/')
def shirts():
    context = {'title': 'Рубашки'}
    return render_template('shirts.html', **context)

if __name__ == '__main__':
    app.run(debug=True)
