# Используем Python как базовый образ
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /usr/src/app/api

# Устанавливаем необходимые пакеты для локали и gettext
RUN apt-get update && apt-get install -y locales gettext && \
    echo "ru_RU.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen

# Устанавливаем переменные окружения для локали
ENV LANG=ru_RU.UTF-8
ENV LANGUAGE=ru_RU:ru
ENV LC_ALL=ru_RU.UTF-8

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем Flask-Babel и Babel CLI для работы с переводами
RUN pip install flask-babel babel

# Копируем исходники приложения, включая папку translations
COPY . .

# Компилируем переводы (выполняется в случае изменений в переводах)
RUN pybabel compile -d translations

# Команда для запуска приложения
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "infrastructure.api.app:app"]
