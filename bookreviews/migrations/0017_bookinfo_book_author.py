# Generated by Django 5.0.3 on 2024-04-02 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookreviews', '0016_alter_commenting_comment_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookinfo',
            name='book_author',
            field=models.CharField(default='null', max_length=255),
            preserve_default=False,
        ),
    ]
