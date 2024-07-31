#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path
from decouple import Config, Csv


def main():
    """Run administrative tasks."""
    # Determine the base directory
    BASE_DIR = Path(__file__).resolve().parent

    # Load the appropriate .env file
    env_file = BASE_DIR / ('.env.dev' if os.getenv('DJANGO_ENV') == 'development' else '.env.prod')
    config = Config(env_file)

    # Set the default settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                          'project.settings.dev' if config('DJANGO_ENV') == 'development' else 'project.settings.prod')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
