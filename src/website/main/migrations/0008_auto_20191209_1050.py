# Generated by Django 2.2.5 on 2019-12-09 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20191118_0921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='board',
            field=models.CharField(default='', max_length=2500),
        ),
    ]