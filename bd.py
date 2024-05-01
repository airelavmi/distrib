import sqlite3

# Создание соединения с базой данных
conn = sqlite3.connect('books.db')

# Создание курсора для выполнения операций с базой данных
cur = conn.cursor()

# Создание таблицы жанров
cur.execute('''CREATE TABLE IF NOT EXISTS genres (
               genre_id INTEGER PRIMARY KEY,
               genre_name TEXT NOT NULL UNIQUE)''')

# Создание таблицы авторов
cur.execute('''CREATE TABLE IF NOT EXISTS authors (
               author_id INTEGER PRIMARY KEY,
               author_name TEXT NOT NULL UNIQUE)''')

# Создание таблицы книг
cur.execute('''CREATE TABLE IF NOT EXISTS books (
               book_id INTEGER PRIMARY KEY,
               title TEXT NOT NULL,
               rating REAL NOT NULL,
               genre_id INTEGER,
               author_id INTEGER,
               FOREIGN KEY (genre_id) REFERENCES genres (genre_id),
               FOREIGN KEY (author_id) REFERENCES authors (author_id))''')

# Данные для вставки в таблицу жанров
genres_data = [
    ("Fantastic",),
    ("Classic literature",),
    ("Detective",),
    ("Adventures",),
    ("Love story",),
    ("Psychology",),
]

# Вставка данных в таблицу жанров
cur.executemany("INSERT INTO genres (genre_name) VALUES (?)", genres_data)

# Данные для вставки в таблицу авторов
authors_data = [
    ("George Orwell",),
    ("Andy Weir",),
    ("William Gibson",),
    ("Ernst Jünger",),
    ("Arthur C. Clarke",),
    ("Fyodor Dostoevsky",),
    ("Alexander Griboyedov",),
    ("Leo Tolstoy",),
    ("Franz Kafka",),
    ("Agatha Christie",),
    ("Stephen King",),
    ("Stieg Larsson",),
    ("Arthur Conan Doyle",),
    ("Miguel de Cervantes",),
    ("Daniel Defoe",),
    ("Jules Verne",),
    ("Jane Austen",),
    ("Alexandre Dumas",),
    ("Gabriel García Márquez",),
    ("Maria Semenova",),
    ("Anton Chekhov",),
    ("Erich Maria Remarque",),
    ("Carl Rogers",),
    ("Hermann Hesse",),
    ("Philip K. Dick",),
    ("Donald A. Norman",)
]

# Вставка данных в таблицу авторов
cur.executemany("INSERT INTO authors (author_name) VALUES (?)", authors_data)

# Данные для вставки в таблицу книг
books_data = [
    ("1984", 4.5, 1, 1),
    ("The Martian", 4.4, 1, 2),
    ("Neuromancer", 4.2, 1, 3),
    ("A Time to Live and a Time to Die", 4.1, 1, 4),
    ("Childhood's End", 4.3, 1, 5),
    ("Crime and Punishment", 4.8, 2, 6),
    ("Woe from Wit", 4.6, 2, 7),
    ("The Brothers Karamazov", 4.7, 2, 6),
    ("War and Peace", 4.9, 2, 8),
    ("The Trial", 4.5, 2, 9),
    ("Murder on the Orient Express", 4.7, 3, 10),
    ("The Green Mile", 4.9, 3, 11),
    ("The Girl with the Dragon Tattoo", 4.5, 3, 12),
    ("Sherlock Holmes", 4.8, 3, 13),
    ("The Adventures of Sherlock Holmes", 4.6, 3, 13),
    ("Don Quixote", 4.6, 4, 14),
    ("Robinson Crusoe", 4.4, 4, 15),
    ("The Mysterious Island", 4.5, 4, 16),
    ("Journey to the Center of the Earth", 4.3, 4, 16),
    ("The Lost World", 4.2, 4, 13),
    ("Pride and Prejudice", 4.7, 5, 17),
    ("The Count of Monte Cristo", 4.8, 5, 18),
    ("The Ghost's Husband", 4.6, 5, 19),
    ("Love and Other Troubles", 4.4, 5, 20),
    ("The Lady with the Dog", 4.3, 5, 21),
    ("Three Comrades", 4.5, 6, 22),
    ("The Road to Self", 4.4, 6, 23),
    ("The Glass Bead Game", 4.3, 6, 24),
    ("Blade Runner", 4.2, 6, 25),
    ("Freedom from False Beliefs", 4.1, 6, 26)
]

# Вставка данных в таблицу книг
cur.executemany("INSERT INTO books (title, rating, genre_id, author_id) VALUES (?, ?, ?, ?)", books_data)

# Подтверждение выполнения операций и закрытие соединения
conn.commit()
conn.close()
