# Generated by Django 2.0.7 on 2018-07-17 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_feedbackbox'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedbackbox',
            name='done',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='suggestionbox',
            name='done',
            field=models.BooleanField(default=False),
        ),
    ]
