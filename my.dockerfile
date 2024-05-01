# Используем базовый образ Python
FROM python:3.12

# Установка зависимостей
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

# Копирование приложения в контейнер
COPY . /app

# Копирование файла базы данных внутрь контейнера
COPY books.db /app/books.db

# Определение переменных среды Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Открытие порта, на котором будет работать приложение Flask
EXPOSE 5000

# Запуск приложения при запуске контейнера
CMD ["flask", "run"]
 