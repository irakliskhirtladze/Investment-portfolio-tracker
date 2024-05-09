# Generated by Django 5.0.3 on 2024-05-09 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0009_alter_portfolio_average_trade_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolio',
            name='quantity',
            field=models.DecimalField(decimal_places=5, max_digits=10, verbose_name='Investment Quantity'),
        ),
    ]