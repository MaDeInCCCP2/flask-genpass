from flask import Flask, render_template, request, redirect, url_for, flash, session
import random
import string
import secrets
import re

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


def generate_password(length, complexity):
    if complexity == 'easy':
        chars = string.ascii_uppercase + string.ascii_lowercase
    elif complexity == 'medium':
        chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    else:
        chars = string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation

    try:
        length = int(length)
        if not 8 <= length <= 64:
            raise ValueError
        return ''.join(random.sample(chars, length))
    except (ValueError, TypeError):
        flash('Длина пароля должна быть от 8 до 64 символов.', 'error')
        return ''


def save_password(password):
    try:
        with open("history.txt", "a", encoding='utf-8') as f:
            f.write(f"{password}\n")
    except IOError:
        flash('Ошибка сохранения истории паролей.', 'error')


def user_exists(username):
    try:
        with open("login.txt", "r", encoding='utf-8') as f:
            for line in f:
                stored_user, _ = line.strip().split(',')
                if stored_user == username:
                    return True
    except FileNotFoundError:
        pass
    return False


def is_valid_username(username):
    return bool(re.match(r'^[a-zA-Z0-9]{3,20}$', username))


@app.before_request
def make_session_transient():
    if 'username' not in session:
        session.clear()


@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    if 'username' not in session:
        return redirect(url_for('login'))

    complexity = request.form.get('complexity', 'medium')
    length = request.form.get('length', 8)
    password = generate_password(length, complexity)

    if password:
        save_password(password)
        return render_template('index.html', password=password)
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']

        if not username or not password:
            flash('Заполните все поля.', 'error')
            return render_template('login.html')

        if not is_valid_username(username):
            flash('Имя пользователя должно содержать 3-20 букв и цифр.', 'error')
            return render_template('login.html')

        try:
            with open("login.txt", "r", encoding='utf-8') as f:
                for line in f:
                    stored_user, stored_pass = line.strip().split(',')
                    if stored_user == username and stored_pass == password:
                        session['username'] = username
                        flash('Вход выполнен успешно!', 'success')
                        return redirect(url_for('index'))
        except FileNotFoundError:
            flash('Нет зарегистрированных пользователей.', 'error')
            return render_template('login.html')

        flash('Неверное имя пользователя или пароль.', 'error')
        return render_template('login.html')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']

        if not username or not password:
            flash('Заполните все поля.', 'error')
            return render_template('register.html')

        if not is_valid_username(username):
            flash('Имя пользователя должно содержать 3-20 букв и цифр.', 'error')
            return render_template('register.html')

        if user_exists(username):
            flash(f'Пользователь "{username}" уже существует!', 'error')
            return render_template('register.html')

        try:
            with open("login.txt", "a", encoding='utf-8') as f:
                f.write(f"{username},{password}\n")
            flash('Регистрация прошла успешно! Теперь вы можете войти.', 'success')
            return redirect(url_for('login'))
        except IOError:
            flash('Ошибка при регистрации. Попробуйте позже.', 'error')
            return render_template('register.html')

    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Вы вышли из аккаунта.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)