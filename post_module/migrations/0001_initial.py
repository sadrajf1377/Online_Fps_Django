# Generated by Django 4.2 on 2024-06-23 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post_Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='date of creation')),
                ('comment_text', models.TextField(max_length=1000, verbose_name='main text of comment')),
            ],
        ),
        migrations.CreateModel(
            name='Post_Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(upload_to='post_images', verbose_name='picture of a post')),
            ],
        ),
        migrations.CreateModel(
            name='Post_Model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.TextField(max_length=2000, verbose_name='post caption')),
                ('title', models.CharField(max_length=30, verbose_name='post title')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='date of creation')),
            ],
        ),
    ]