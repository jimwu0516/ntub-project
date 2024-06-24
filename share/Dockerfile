FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

RUN apt-get update \
    && apt-get install -y netcat-openbsd gcc postgresql \
    && apt-get clean

RUN pip install --upgrade pip
RUN pip install pipenv

COPY . /usr/src/app/

RUN pipenv install --deploy --ignore-pipfile
RUN pipenv install gunicorn  # 安装 gunicorn

RUN pipenv run python manage.py collectstatic --noinput
RUN chown -R www-data:www-data /usr/src/app/staticfiles
RUN chmod -R 755 /usr/src/app/staticfiles

COPY entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
