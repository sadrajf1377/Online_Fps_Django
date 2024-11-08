# Generated by Django 4.2 on 2024-07-09 01:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import messages_module.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post_module', '0006_remove_post_model_hashtags_hash_tag_posts'),
        ('messages_module', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='attached_post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='post_module.post_model', verbose_name='linked post'),
        ),
        migrations.AddField(
            model_name='message',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='group_messages', verbose_name='attached image'),
        ),
        migrations.AddField(
            model_name='message',
            name='message_type',
            field=models.CharField(choices=[('normal', 'normal'), ('post', 'post')], default='normal', max_length=10),
        ),
        migrations.CreateModel(
            name='Direct_Message_Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Direct_Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='time of creation')),
                ('text', models.TextField(max_length=2000)),
                ('message_type', models.CharField(choices=[('normal', 'normal'), ('post', 'post')], max_length=10)),
                ('image', models.ImageField(blank=True, null=True, upload_to='direct_messages', verbose_name='attached image')),
                ('attached_post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='post_module.post_model', verbose_name='linked post')),
                ('parent_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='messages_module.direct_message_group', verbose_name='parent group of this message')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='sender of this post')),
            ],
        ),
    ]
