# Используем официальный образ Python
FROM python:3.8-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем requirements.txt в контейнер
COPY requirements.txt requirements.txt

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Копируем содержимое текущей директории в контейнер в /app
COPY . .

# Определяем переменную окружения для Flask (это необязательно, но может быть полезно)
ENV FLASK_APP=app.py

# Команда для запуска приложения Flask
CMD ["flask", "run", "--host=0.0.0.0"]

# Экспонируем порт 5000, который используется Flask
EXPOSE 5000
