# Generated by Django 5.0.6 on 2024-07-03 13:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0004_rename_transaction_investmenttransaction'),
    ]

    operations = [
        migrations.RenameField(
            model_name='portfolioentry',
            old_name='investment_type',
            new_name='investment_category',
        ),
    ]
