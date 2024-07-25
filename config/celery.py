from celery.schedules import crontab

app.conf.beat_schedule = {
    'fetch-and-store-portfolio-value-daily': {
        'task': 'stats.tasks.fetch_and_store_portfolio_value',
        'schedule': crontab(hour=0, minute=0),  # Runs daily at midnight
    },
}
