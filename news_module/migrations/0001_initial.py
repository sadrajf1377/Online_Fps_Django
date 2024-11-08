# Generated by Django 4.2 on 2024-06-23 20:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='comment_dislike_list',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='comment_like_list',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', error_messages={'unique': 'News instancewith such title exists'}, max_length=100, unique=True, verbose_name='news title')),
                ('news_text', models.TextField(default='', max_length=2000, verbose_name='news main text')),
                ('image', models.FileField(upload_to='news_images/')),
                ('creation_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date of Creation')),
            ],
            options={
                'verbose_name': 'News',
                'verbose_name_plural': 'News',
            },
        ),
        migrations.CreateModel(
            name='News_Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like_or_dislike', models.CharField(choices=[('like', 'like'), ('dislike', 'dislike'), ('neutral', 'neutral')], default='neutral', max_length=10, verbose_name='users opinion')),
                ('comment', models.CharField(default='', max_length=200, verbose_name='users comment')),
                ('creation_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='creation date')),
                ('parent_news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news_module.news', verbose_name='parent comment')),
            ],
            options={
                'verbose_name': 'News Comment',
                'verbose_name_plural': 'News Comments',
            },
        ),
    ]
