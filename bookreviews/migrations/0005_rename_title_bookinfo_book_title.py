# Generated by Django 5.0.3 on 2024-03-25 01:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookreviews', '0004_commenting'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookinfo',
            old_name='title',
            new_name='book_title',
        ),
    ]
