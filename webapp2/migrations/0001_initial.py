# Generated by Django 4.2.2 on 2023-07-24 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='properties',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('desc', models.CharField(max_length=1000)),
                ('image', models.ImageField(default=None, null=True, upload_to='properties/%y/%m/%d/')),
            ],
        ),
    ]