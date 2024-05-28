from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, current_user, UserMixin
import sqlite3

# Создаем экземпляр приложения Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'  # Устанавливаем секретный ключ

# Настройка Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Подключаемся к базе данных
def get_db_connection():
    conn = sqlite3.connect('kino.db')
    conn.row_factory = sqlite3.Row
    return conn

# Определяем класс пользователя
class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

# Функция загрузки пользователя из базы данных
@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    user_data = conn.execute('SELECT * FROM users WHERE UserID = ?', (user_id,)).fetchone()
    conn.close()
    if user_data:
        return User(id=user_data['UserID'], username=user_data['Username'])
    else:
        return None

# Основная страница
@app.route('/')
def index():
    conn = get_db_connection()
    films_old = conn.execute('SELECT * FROM films WHERE ReleaseYear < 2000').fetchall()
    films_new = conn.execute('SELECT * FROM films WHERE ReleaseYear >= 2000').fetchall()
    conn.close()
    return render_template('index.html', films_old=films_old, films_new=films_new, current_user=current_user.username if current_user.is_authenticated else None)

@app.route('/films')
def films():
    conn = get_db_connection()
    films = conn.execute('SELECT * FROM films').fetchall()
    conn.close()
    return render_template('films.html', films=films)

# Страница с сеансами
@app.route('/sessions')
def sessions():
    conn = get_db_connection()
    sessions = conn.execute('SELECT * FROM sessions').fetchall()
    conn.close()
    return render_template('sessions.html', sessions=sessions)

# Страница с бронированием
@app.route('/bookings')
def bookings():
    conn = get_db_connection()
    bookings = conn.execute('SELECT * FROM bookings').fetchall()
    conn.close()
    return render_template('bookings.html', bookings=bookings)

@app.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():

    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm-password']

    conn = get_db_connection()
    user_check = conn.execute('SELECT * FROM users WHERE Username = ? OR Email = ?', (username, email)).fetchone()

    if user_check:
        flash('User already exists! Please choose a different username or email.', 'error')
        return render_template('register.html', user_exists=True)

    if password != confirm_password:
        flash('Passwords do not match! Please try again.', 'error')
        return redirect(url_for('register_page'))

    conn.execute('INSERT INTO users (Username, Password, Email) VALUES (?, ?, ?)', (username, password, email))
    conn.commit()

    user_id = conn.execute('SELECT UserID FROM users WHERE Email = ?', (email,)).fetchone()['UserID']
    conn.close()

    new_user = User(id=user_id, username=username)
    login_user(new_user)

    flash('Registration successful! Welcome, {}!'.format(username), 'success')

    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE Email = ? AND Password = ?', (email, password)).fetchone()
        conn.close()

        if user:
            login_user(User(id=user['UserID'], username=user['Username']))
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password.', 'error')

    return render_template('login.html')


def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

@app.route('/film/<int:film_id>')
def film_details(film_id):
    conn = get_db_connection()
    film = conn.execute('SELECT * FROM films WHERE FilmID = ?', (film_id,)).fetchone()
    ratings = conn.execute('SELECT AVG(Rating) AS AvgRating, COUNT(Rating) AS NumRatings FROM ratings WHERE FilmID = ?', (film_id,)).fetchone()
    sessions = conn.execute('SELECT * FROM sessions WHERE FilmID = ?', (film_id,)).fetchall()

    similar_films = conn.execute('SELECT * FROM films WHERE Genre = ? AND FilmID != ?', (film['Genre'], film_id)).fetchall()

    conn.close()

    if film is None:
        return 'Film not found!', 404

    return render_template('film_details.html', film=film, ratings=ratings, sessions=sessions, similar_films=similar_films)

if __name__ == '__main__':
    app.run(debug=True)