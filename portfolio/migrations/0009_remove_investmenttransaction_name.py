# Generated by Django 5.0.6 on 2024-07-20 12:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0008_rename_transaction_category_investmenttransaction_asset_type_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='investmenttransaction',
            name='name',
        ),
    ]
