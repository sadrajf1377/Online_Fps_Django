# Generated by Django 4.2 on 2024-06-23 20:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('report_module', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='report_session',
            name='owner_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='whos session is this'),
        ),
        migrations.AddField(
            model_name='report',
            name='reply_to',
            field=models.ForeignKey(blank=True, help_text='parent message of this report', null=True, on_delete=django.db.models.deletion.CASCADE, to='report_module.report', verbose_name='parent_message'),
        ),
        migrations.AddField(
            model_name='report',
            name='report_session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report_module.report_session', verbose_name='parent session'),
        ),
    ]
