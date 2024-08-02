# Use the official Python image from the Docker Hub
FROM --platform=linux/amd64 python:3.12-bookworm

# Add a line to print environment variables
RUN echo "Environment Variables: $(env)"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip setuptools
RUN pip install -r requirements.txt

# Copy the Django project
COPY . /code/

# Use the environment variable to select the correct settings file
ARG ENVIRONMENT
ENV DJANGO_SETTINGS_MODULE=config.settings.${ENVIRONMENT}

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]


