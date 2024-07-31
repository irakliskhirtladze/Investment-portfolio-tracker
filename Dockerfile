# Use the official Python image from the Docker Hub
FROM python:3.12-slim-bullseye

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Copy the Django project
COPY . /code/

# Use the environment variable to select the correct settings file
ARG ENVIRONMENT
ENV DJANGO_SETTINGS_MODULE=config.settings.${ENVIRONMENT}

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "project.wsgi:application"]
