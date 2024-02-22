from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), nullable=False)
    user_surname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    user_password = db.Column(db.String(15), nullable=False)                   # Поле пароль
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        """Функция выводит информацию о пользователе"""
        return f'User({self.username}, {self.email})'

