# Generated by Django 4.2 on 2024-07-01 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post_module', '0004_post_like_list'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hash_Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='hashtag title')),
            ],
        ),
        migrations.AlterModelOptions(
            name='post_like_list',
            options={'verbose_name': 'like_list', 'verbose_name_plural': 'like_lists'},
        ),
        migrations.AlterModelOptions(
            name='post_model',
            options={'verbose_name': 'post', 'verbose_name_plural': 'posts'},
        ),
        migrations.AddField(
            model_name='post_model',
            name='hashtags',
            field=models.ManyToManyField(blank=True, null=True, to='post_module.hash_tag', verbose_name='posts hashtags'),
        ),
    ]
