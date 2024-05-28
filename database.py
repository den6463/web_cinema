import sqlite3

def create_database():
    conn = sqlite3.connect('kino.db')
    cursor = conn.cursor()

    # Создание таблиц
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bookings (
        BookingID INTEGER PRIMARY KEY AUTOINCREMENT,
        UserID INTEGER,
        SessionID INTEGER,
        NumTickets INTEGER,
        TotalAmount REAL,
        BookingDate TEXT,
        FOREIGN KEY (UserID) REFERENCES users (UserID),
        FOREIGN KEY (SessionID) REFERENCES sessions (SessionID)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cinemas (
        CinemaID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT,
        Location TEXT
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS discounts (
        DiscountID INTEGER PRIMARY KEY AUTOINCREMENT,
        DiscountName TEXT,
        Percentage REAL,
        Description TEXT
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS favorites (
        FavoriteID INTEGER PRIMARY KEY AUTOINCREMENT,
        UserID INTEGER,
        FilmID INTEGER,
        FOREIGN KEY (UserID) REFERENCES users (UserID),
        FOREIGN KEY (FilmID) REFERENCES films (FilmID)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS films (
        FilmID INTEGER PRIMARY KEY AUTOINCREMENT,
        Title TEXT,
        ReleaseYear INTEGER,
        Genre TEXT,
        Director TEXT,
        Poster TEXT,
        WatchLink TEXT
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS genres (
        GenreID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ratings (
        RatingID INTEGER PRIMARY KEY AUTOINCREMENT,
        UserID INTEGER,
        FilmID INTEGER,
        Rating REAL,
        Review TEXT,
        RatingDate TEXT,
        FOREIGN KEY (UserID) REFERENCES users (UserID),
        FOREIGN KEY (FilmID) REFERENCES films (FilmID)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS seats (
        SeatID INTEGER PRIMARY KEY AUTOINCREMENT,
        SessionID INTEGER,
        SeatNumber TEXT,
        SeatType TEXT,
        FOREIGN KEY (SessionID) REFERENCES sessions (SessionID)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sessions (
        SessionID INTEGER PRIMARY KEY AUTOINCREMENT,
        FilmID INTEGER,
        StartTime TEXT,
        TicketPrice REAL,
        FOREIGN KEY (FilmID) REFERENCES films (FilmID)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tickets (
        TicketID INTEGER PRIMARY KEY AUTOINCREMENT,
        BookingID INTEGER,
        SeatNumber TEXT,
        FOREIGN KEY (BookingID) REFERENCES bookings (BookingID)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        UserID INTEGER PRIMARY KEY AUTOINCREMENT,
        Username TEXT,
        Password TEXT,
        Email TEXT,
        Phone TEXT
    );
    ''')

    cursor.executemany('''
    INSERT INTO bookings (BookingID, UserID, SessionID, NumTickets, TotalAmount, BookingDate) VALUES (?, ?, ?, ?, ?, ?)
    ''', [
        (1, 1, 1, 2, 20.00, '2024-04-04'),
        (2, 2, 3, 3, 33.00, '2024-04-05'),
        (3, 3, 5, 1, 11.50, '2024-04-06'),
        (4, 4, 7, 4, 50.00, '2024-04-07'),
        (5, 5, 9, 2, 22.00, '2024-04-08'),
        (6, 6, 2, 3, 36.00, '2024-04-09'),
        (7, 7, 4, 2, 21.00, '2024-04-10'),
        (8, 8, 6, 1, 9.00, '2024-04-11'),
        (9, 9, 8, 3, 30.00, '2024-04-12'),
        (10, 10, 10, 2, 24.00, '2024-04-13')
    ])

    cursor.executemany('''
    INSERT INTO cinemas (CinemaID, Name, Location) VALUES (?, ?, ?)
    ''', [
        (1, 'Кинотеатр Однажды в Голливуде', 'Улица Пирогова, 10, Астана'),
        (2, 'Кинотеатр Звездные войны', 'Пушкина, 5, Алматы'),
        (3, 'Кинотеатр Невероятная жизнь Уолтера Митти', 'Улица Горького, 15, Новосибирск')
    ])

    cursor.executemany('''
    INSERT INTO films (FilmID, Title, ReleaseYear, Genre, Director, Poster, WatchLink) VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', [
        (1, 'Начало', 2010, 'Научная фантастика', 'Кристофер Нолан', 'static/img/1.jpeg', 'static/video/1.mp4'),
        (2, 'Крестный отец', 1972, 'Криминал', 'Фрэнсис Форд Коппола', 'static/img/2.jpg', 'static/video/1.mp4'),
        (3, 'Побег из Шоушенка', 1994, 'Драма', 'Фрэнк Дарабонт', 'static/img/3.png', 'static/video/1.mp4'),
        (4, 'Криминальное чтиво', 1994, 'Криминал', 'Квентин Тарантино', 'static/img/4.jpg', 'static/video/1.mp4'),
        (5, 'Темный рыцарь', 2008, 'Боевик', 'Кристофер Нолан', 'static/img/5.jpg', 'static/video/1.mp4'),
        (6, 'Форрест Гамп', 1994, 'Драма', 'Роберт Земекис', 'static/img/6.jpg', 'static/video/1.mp4'),
        (7, 'Матрица', 1999, 'Боевик', 'Лана и Лилли Вачовски', 'static/img/7.jpeg', 'static/video/1.mp4'),
        (8, 'Бойцовский клуб', 1999, 'Драма', 'Дэвид Финчер', 'static/img/8.jpg', 'static/video/1.mp4'),
        (9, 'Интерстеллар', 2014, 'Научная фантастика', 'Кристофер Нолан', 'static/img/9.jpg', 'static/video/1.mp4'),
        (10, 'Властелин колец: Братство кольца', 2001, 'Фэнтези', 'Питер Джексон', 'static/img/10.jpg', 'static/video/1.mp4')
    ])

    cursor.executemany('''
    INSERT INTO genres (GenreID, Name) VALUES (?, ?)
    ''', [
        (1, 'Научная фантастика'),
        (2, 'Криминал'),
        (3, 'Драма'),
        (4, 'Боевик'),
        (5, 'Фэнтези')
    ])

    cursor.executemany('''
    INSERT INTO ratings (RatingID, UserID, FilmID, Rating, Review, RatingDate) VALUES (?, ?, ?, ?, ?, ?)
    ''', [
        (1, 1, 1, 9.5, 'Удивительный фильм, понравилась концепция!', '2024-04-02'),
        (2, 2, 2, 10.0, 'Один из лучших фильмов всех времен!', '2024-04-03'),
        (3, 3, 3, 9.0, 'Бессмертный классический фильм, обязательно к просмотру!', '2024-04-04'),
        (4, 4, 4, 8.5, 'Отличный сюжет и персонажи.', '2024-04-05'),
        (5, 5, 5, 9.5, 'Абсолютно потрясающая визуализация!', '2024-04-06'),
        (6, 6, 6, 8.0, 'Сердце согревающий и вдохновляющий.', '2024-04-07'),
        (7, 7, 7, 9.0, 'Взрывной экшен!', '2024-04-08'),
        (8, 8, 8, 8.5, 'Блестяще выполненные повороты сюжета.', '2024-04-09'),
        (9, 9, 9, 9.0, 'Эпическое путешествие по пространству и времени.', '2024-04-10'),
        (10, 10, 10, 9.5, 'Шедевр сюжета.', '2024-04-11')
    ])


    cursor.executemany('''
    INSERT INTO sessions (SessionID, FilmID, StartTime, TicketPrice) VALUES (?, ?, ?, ?)
    ''', [
        (1, 1, '2024-04-05 18:00:00', 10.00),
        (2, 2, '2024-04-06 19:00:00', 12.00),
        (3, 3, '2024-04-07 20:00:00', 11.00),
        (4, 4, '2024-04-08 21:00:00', 10.50),
        (5, 5, '2024-04-09 18:30:00', 11.50),
        (6, 6, '2024-04-10 17:00:00', 9.00),
        (7, 7, '2024-04-11 18:30:00', 12.50),
        (8, 8, '2024-04-12 20:00:00', 10.00),
        (9, 9, '2024-04-13 21:30:00', 11.00),
        (10, 10, '2024-04-14 19:00:00', 12.00)
    ])

    cursor.executemany('''
    INSERT INTO tickets (TicketID, BookingID, SeatNumber) VALUES (?, ?, ?)
    ''', [
        (1, 1, 'A1'),
        (2, 2, 'B3'),
        (3, 3, 'C5'),
        (4, 4, 'D2'),
        (5, 5, 'E4'),
        (6, 6, 'F6'),
        (7, 7, 'G8'),
        (8, 8, 'H9'),
        (9, 9, 'I7'),
        (10, 10, 'J10')
    ])

    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()