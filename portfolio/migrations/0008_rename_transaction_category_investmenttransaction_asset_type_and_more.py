# Generated by Django 5.0.6 on 2024-07-20 12:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0007_alter_investmenttransaction_symbol_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='investmenttransaction',
            old_name='transaction_category',
            new_name='asset_type',
        ),
        migrations.RenameField(
            model_name='portfolioentry',
            old_name='investment_name',
            new_name='asset_name',
        ),
        migrations.RenameField(
            model_name='portfolioentry',
            old_name='investment_symbol',
            new_name='asset_symbol',
        ),
        migrations.RenameField(
            model_name='portfolioentry',
            old_name='investment_type',
            new_name='asset_type',
        ),
    ]