# Generated by Django 3.0.3 on 2020-02-24 12:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Governorate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('image', models.ImageField(null=True, upload_to='core/images/')),
                ('slug', models.SlugField(editable=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('slug', models.SlugField(editable=False, unique=True)),
                ('governorate', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cities', to='core.Governorate')),
            ],
        ),
    ]
