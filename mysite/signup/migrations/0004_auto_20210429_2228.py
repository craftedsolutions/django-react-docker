# Generated by Django 3.1.8 on 2021-04-29 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0003_auto_20210429_1948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailconfirmation',
            name='confirmation_date',
            field=models.DateTimeField(null=True, verbose_name='Email Confirmation Date'),
        ),
    ]
