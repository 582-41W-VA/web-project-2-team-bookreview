# Generated by Django 5.0.3 on 2024-03-26 11:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookreviews', '0010_alter_customuser_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'permissions': [('can_view_users', 'Can view users'), ('can_edit_users', 'Can edit users'), ('can_edit_reviews', 'Can edit reviews'), ('can_delete_reviews', 'Can delete reviews'), ('can_view_all_reviews', 'Can view all reviews'), ('can_delete_comments', 'Can delete comments')]},
        ),
    ]
