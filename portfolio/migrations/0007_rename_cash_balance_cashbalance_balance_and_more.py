# Generated by Django 5.0.3 on 2024-05-08 09:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0006_remove_portfolio_cash_balance_cashbalance'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='cashbalance',
            old_name='cash_balance',
            new_name='balance',
        ),
        migrations.AlterField(
            model_name='cashbalance',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]