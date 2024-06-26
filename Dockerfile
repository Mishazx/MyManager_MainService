FROM python:3.11-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py create_superuser && python manage.py runserver 0.0.0.0:8000"]
