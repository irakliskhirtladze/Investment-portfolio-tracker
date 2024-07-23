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

# Run the site domain setting command after migrations
CMD ["sh", "-c", "python manage.py migrate && python manage.py set_site_domain && python manage.py runserver 0.0.0.0:8000"]
