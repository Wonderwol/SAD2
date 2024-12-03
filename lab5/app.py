from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Flask-Login настройка
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Модель User
class User(UserMixin):
    def __init__(self, id, email, password, name):
        self.id = id
        self.email = email
        self.password = password
        self.name = name

# Простая база данных пользователей (для демонстрации)
users = {
    1: User(1, "test@example.com", "password123", "John Doe"),
}
next_user_id = 2  # Следующий ID для новых пользователей

# Загрузка пользователя
@login_manager.user_loader
def load_user(user_id):
    return users.get(int(user_id))

# Эндпоинт для регистрации (POST-запрос)
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    global next_user_id
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        # Проверка на заполненность полей
        if not name or not email or not password:
            flash('Все поля обязательны для заполнения', 'error')
            return redirect(url_for('signup'))

        # Проверка на уникальность email
        if any(user.email == email for user in users.values()):
            flash('Пользователь с таким email уже существует', 'error')
            return redirect(url_for('signup'))

        # Создание нового пользователя
        new_user = User(next_user_id, email, password, name)
        users[next_user_id] = new_user
        next_user_id += 1
        flash('Регистрация прошла успешно! Войдите в систему.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

# Эндпоинт для выхода (GET-запрос)
@app.route('/logout')
@login_required
def logout():
    logout_user()  # Завершаем сессию
    flash('Вы успешно вышли из системы.', 'info')
    return redirect(url_for('login'))

# Эндпоинт для входа
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('Все поля обязательны для заполнения', 'error')
            return redirect(url_for('login'))

        user = next((u for u in users.values() if u.email == email), None)
        if not user:
            flash('Пользователь с указанным email не найден', 'error')
            return redirect(url_for('login'))

        if user.password != password:
            flash('Неверный пароль', 'error')
            return redirect(url_for('login'))

        login_user(user)
        return redirect(url_for('index'))

    return render_template('login.html')

# Корневой эндпоинт
@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template(
            'index.html',
            lab_title="Лабораторная работа Flask-Login",
            lab_description="Эта лабораторная работа демонстрирует использование Flask-Login.",
            user=current_user
        )
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
