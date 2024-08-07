# Use the official Python slim image as a parent image
FROM python:3.12-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip setuptools \
    && pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /code/

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port for Gunicorn
EXPOSE 8000

# Set environment variable for settings module
ENV DJANGO_SETTINGS_MODULE=config.settings.prod

# Run the production server using Gunicorn
CMD ["sh", "-c", "python manage.py migrate && python manage.py set_site_domain && gunicorn config.wsgi -b 0.0.0.0:8000 --timeout=30 --threads=10"]
