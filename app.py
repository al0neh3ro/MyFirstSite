# библиотеки
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import request, redirect, url_for, flash
from datetime import datetime
from flask import session
import os
import psycopg2
from dotenv import load_dotenv
load_dotenv()

# создание основы для запуска 
app = Flask(__name__)

# ключ для сессии 
app.secret_key = 'secret_key_0123'

# Получаем строку подключения из переменных окружения
DATABASE_URL = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# доделать подключение к бд на alive и разобраться с render



# Настройка подключения к PostgreSQL
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:123456@localhost/user_from_my_site'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Создаём объект для работы с БД
db = SQLAlchemy(app)

#  создание юзера
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))

def currenttime():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time

# главная страница сайта
@app.route('/')
def home():
    username = session.get('username', None)
    now=currenttime()
    return render_template('index.html', username = username, current_time=now)

# еще одна страница 
@app.route('/about')
def about():
   username = session.get('username', None)
   now=currenttime()
   return render_template('about.html', username=username, current_time=now) 

# и еще страница
@app.route('/contact')
def contact():
    username = session.get('username', None)
    now=currenttime()
    return render_template('contact.html', username=username, current_time=now)

# страница регистарции
@app.route('/register', methods = ['GET', 'POST'])
def register():
    message = None
    if request.method == 'POST':  # делаем пост в бд для отправки и проверки данных
        name = request.form['username'] # тут 
        email = request.form['email'] # тут 
        password = request.form.get('password') # и тут но подругому, запрашиваем их бд данные

        # проврка корректности почты
        message1 = "Введите корректную почту!"
        if '@' not in email or '.' not in email:
            return render_template('register.html', message = message1)
        
        # поиск по бд, а конкретно поиск емейла 
        searchUser = User.query.filter_by(email=email).first()
        if searchUser:
            mess2 = "Почта уже занята!"
            return render_template('register.html', message = mess2)
        else:
            pass
        
        # добавляение в данных юзера в бд
        user = User(name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()

        session['username'] = name
        

        message = f'Пользователь {name} успешно зарегистрирован!'
        print(f"Пользователь {name} успешно добавлен!")
        return render_template('index.html' , message=message, username=name)

    username = session.get('username', None)
    now=currenttime()
    # возварт на страницу регистарации после заврешения    
    return render_template('register.html', username=username, current_time=now)


# страница логина
@app.route('/login', methods = ['GET', 'POST'])
def login():
    message = None
    if request.method == 'POST':
        # проверям в бд емаил и пароль
        email = request.form.get('email')
        password = request.form.get('password')
        
        # проврека почты
        message1 = "Введите корректную почту!"
        if '@' not in email or '.' not in email:
            return render_template('login.html', message = message1)
        
        # проверка на заполненные поля (хз работает ли, не проверял)
        if not email or not password:
            return render_template('login.html', message="Заполните все поля!")
        
        # поиск почты в бд
        user = User.query.filter_by(email=email).first()
        if user:
          print('email confirm')
        else:
            mess1 = "Данной почты не существует!"
            return render_template('login.html', message = mess1)
        
        # проверка пароля
        if user.password == password: 
            session['username'] = user.name
            print('password confirm')
            return render_template('index.html', message = 'Вход выполнен успешно!', username=user.name)
        else:
            return render_template('login.html', message = 'Пароль неверный!')

    now=currenttime()
    # возврат к логину          
    return render_template('login.html', current_time=now)

@app.route('/logout')
def logout():
    session.pop('username', None)
    # now=currenttime()
    return redirect('/login')

# 30.06.2026 - я впервые сам пофиксил баг по поведению сайта
# горжусь собой, это было круто 









# добавление пользовтаелей
# with app.app_context():
  # new_user = User(name="Anna")
  # db.session.add(new_user)
  # db.session.commit()
  # print("User added!")

# удаление пользователей
# with app.app_context():
#     db.session.query(User).delete()
#     db.session.commit()
#     print("Все пользователи удалены")


# создание таблицы
# with app.app_context():
#     db.create_all()
#     print("Table create!")

# запуск сервера
if __name__ == '__main__':
    print("1. Запуск сервера...")
    app.run(debug=True, port=5000)
    print("2. Сервер остановлен (эта строка появится только после Ctrl+C)")


