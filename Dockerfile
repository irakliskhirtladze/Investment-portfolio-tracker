# Use the official Python image from the Docker Hub
FROM --platform=linux/amd64 python:3.12-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip setuptools \
    && pip install --no-cache-dir -r requirements.txt

# Copy the Django project
COPY . /code/

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port for development server
EXPOSE 8000

# Run the development server
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--reload", "--workers=3"]
