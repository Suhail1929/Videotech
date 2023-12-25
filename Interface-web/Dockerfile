FROM python:3.8

RUN pip install flask flask_simplelogin flask.views

WORKDIR /app

COPY app_code/ /app

CMD ["python", "manage.py", "runserver"]
