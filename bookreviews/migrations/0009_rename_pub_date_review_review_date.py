# Generated by Django 5.0.3 on 2024-03-26 08:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookreviews', '0008_review_pub_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='pub_date',
            new_name='review_date',
        ),
    ]