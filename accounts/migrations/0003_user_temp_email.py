# Generated by Django 3.0.3 on 2020-02-27 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_email_confirmed'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='temp_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
