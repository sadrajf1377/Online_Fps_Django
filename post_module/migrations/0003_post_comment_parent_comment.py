# Generated by Django 4.2 on 2024-06-27 00:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post_module', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post_comment',
            name='parent_comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='post_module.post_comment', verbose_name='parent comment'),
        ),
    ]
