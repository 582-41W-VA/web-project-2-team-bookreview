# Generated by Django 5.0.3 on 2024-03-26 07:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookreviews', '0006_rename_comment_review_review_content'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'permissions': [('can_view_users', 'Can view users'), ('can_edit_users', 'Can edit users'), ('can_edit_reviews', 'Can edit reviews'), ('can_delete_reviews', 'Can delete reviews')]},
        ),
    ]
