# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y netcat-openbsd gcc postgresql \
    && apt-get clean

# Install pipenv
RUN pip install --upgrade pip
RUN pip install pipenv

# Copy project files
COPY . /usr/src/app/

# Install project dependencies
RUN pipenv install --deploy --ignore-pipfile
RUN pipenv install gunicorn  # 安装 gunicorn

# Collect static files and set permissions
RUN pipenv run python manage.py collectstatic --noinput
RUN chown -R www-data:www-data /usr/src/app/staticfiles
RUN chmod -R 755 /usr/src/app/staticfiles

# Copy entrypoint.sh
COPY entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# Expose port 8000
EXPOSE 8000

# Run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
