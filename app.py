from flask import Flask, request, jsonify
import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


app = Flask(__name__)

# Подключение к базе данных
conn = sqlite3.connect('books.db')
cur = conn.cursor()

# Инициализация и обучение TF-IDF векторизаторов
tfidf_vectorizer_genre = TfidfVectorizer()
tfidf_vectorizer_author = TfidfVectorizer()
tfidf_vectorizer_title = TfidfVectorizer()

tfidf_vectorizer_genre_books = TfidfVectorizer()
tfidf_vectorizer_author_books = TfidfVectorizer()

# Получение данных из базы данных
cur.execute("SELECT genre_name FROM genres")
genres = cur.fetchall()
cur.execute("SELECT author_name FROM authors")
authors = cur.fetchall()
cur.execute("SELECT title FROM books")
titles = cur.fetchall()

# Преобразование данных для TF-IDF векторизации
genres_text = [' '.join(genre) for genre in genres]
authors_text = [' '.join(author) for author in authors]
titles_text = [' '.join(title) for title in titles]


# Получение данных о книгах из базы данных
cur.execute("SELECT book_id, genre_id, author_id FROM books ORDER BY book_id")
books_data = cur.fetchall()

# Создание словаря для хранения соответствия genre_id и genre_name
genre_id_to_name = {}
author_id_to_name = {}

# Получение соответствующих имен жанров для каждого genre_id
for book in books_data:
    genre_id = book[1]
    author_id = book[2]

    cur.execute("SELECT genre_name FROM genres WHERE genre_id=?", (genre_id,))
    genre_name = cur.fetchone()[0]
    genre_id_to_name[genre_id] = genre_name

    cur.execute("SELECT author_name FROM authors WHERE author_id=?", (author_id,))
    author_name = cur.fetchone()[0]
    author_id_to_name[author_id] = author_name

# Замена genre_id на genre_name в books_data
books_genres = [genre_id_to_name[book[1]] for book in books_data]
books_authors = [author_id_to_name[book[2]] for book in books_data]

# Обучение TF-IDF векторизаторов
tfidf_matrix_genre = tfidf_vectorizer_genre.fit_transform(genres_text)
tfidf_matrix_author = tfidf_vectorizer_author.fit_transform(authors_text)
tfidf_matrix_title = tfidf_vectorizer_title.fit_transform(titles_text)

tfidf_matrix_genre_books = tfidf_vectorizer_genre_books.fit_transform(books_genres)
tfidf_matrix_author_books = tfidf_vectorizer_author_books.fit_transform(books_authors)


def recommend_books(cur, genre=None, author=None, title=None):
    # Определение индекса книги, если задано название
    if title:
        cur.execute("SELECT * FROM books WHERE Title=?", (title,))
        book_data = cur.fetchone()
        # Если книга с таким названием найдена, book_data будет содержать данные о книге
        if book_data:
            idx = book_data[0]
        else:
            print("Книга с названием '{}' не найдена.".format(title))
    else:
        idx = None
    # Вычисление косинусной схожести для каждого параметра
    cosine_similarities_genre = cosine_similarity(tfidf_matrix_genre_books, tfidf_matrix_genre_books)
    cosine_similarities_author = cosine_similarity(tfidf_matrix_author_books, tfidf_matrix_author_books)
    cosine_similarities_title = cosine_similarity(tfidf_matrix_title, tfidf_matrix_title)
    
    #idx_g = None
    if genre:
        cur.execute("SELECT * FROM genres WHERE genre_name=?", (genre,))
        gerne_data = cur.fetchone()
        print(gerne_data)
        if gerne_data:
            idx_g = gerne_data[0]
        else:
            print("Жанр '{}' не найден.".format(genre))
    #if idx_g is not None:
    cosine_similarities_genre_books = cosine_similarity(tfidf_matrix_genre, tfidf_matrix_genre_books)

    #idx_a = None
    if author:
        cur.execute("SELECT * FROM authors WHERE author_name=?", (author,))
        author_data = cur.fetchone()
        if author_data:
            idx_a = author_data[0]
        else:
            print("Автор '{}' не найден.".format(author))
    #if idx_a is not None:
    cosine_similarities_author_books = cosine_similarity(tfidf_matrix_author, tfidf_matrix_author_books)

    #if idx_a is not None or idx_a is not None or idx is not None:
        # Формирование списка рекомендаций
    recommendations = []
    for i in range(len(titles)):
        if idx is not None and i == idx:
            continue
        score = 0
        if genre:
            score += cosine_similarities_genre_books[idx_g-1][i]
        if author:
            score += cosine_similarities_author_books[idx_a-1][i]

        recommendations.append((titles[i][0], score))

        # Сортировка рекомендаций сначала по схожести
    recommendations.sort(key=lambda x: x[1], reverse=True)

        # Если задано название книги, добавляем похожие книги
    if idx is not None:
        recommendations = []
        for i in range(len(titles)):
            # Пропускаем текущую книгу
            if i == idx-1:
                continue
            score = 0
            score += cosine_similarities_genre[idx-1][i]
            score += cosine_similarities_author[idx-1][i]
            recommendations.append((titles[i][0], score))

    recommendations.sort(key=lambda x: x[1], reverse=True)
    return recommendations[:5]


# Закрытие соединения с базой данных
conn.close()

# Функция для подключения к базе данных
def get_db_connection():
    conn = sqlite3.connect('books.db')
    conn.row_factory = sqlite3.Row
    return conn

# Обработчик маршрута /recommend
@app.route('/recommend', methods=['GET'])
def get_recommendations():
    # Получение параметров запроса
    genre = request.args.get('genre')
    author = request.args.get('author')
    title = request.args.get('title')

    # Получение соединения с базой данных
    conn = get_db_connection()
    cur = conn.cursor()

    # Вызов функции для получения рекомендаций
    recommendations = recommend_books(cur, genre=genre, author=author, title=title)

    # Закрытие курсора и соединения с базой данных
    cur.close()
    conn.close()

    # Возврат рекомендаций в формате JSON
    return jsonify(recommendations)


# Запуск приложения
if __name__ == '__main__':
    app.run(debug=True)