# Generated by Django 2.0.7 on 2018-07-16 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_delete_null'),
    ]

    operations = [
        migrations.CreateModel(
            name='SuggestionBox',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=64)),
                ('suggest_count', models.IntegerField()),
            ],
        ),
    ]