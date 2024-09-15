# Используем официальный образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта в контейнер
COPY . .

RUN pip install gunicorn

# Экспонируем порт, на котором будет работать FastAPI (8000)
EXPOSE 8000

# Команда для запуска приложения
CMD ["gunicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

