# Generated by Django 5.0.1 on 2024-01-22 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NewReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('author', models.CharField(max_length=100)),
                ('date', models.DateTimeField()),
                ('property', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('length', models.IntegerField()),
                ('reasonableness', models.IntegerField()),
                ('comprehensiveness', models.IntegerField()),
                ('relevancy', models.IntegerField()),
                ('tonality', models.FloatField()),
            ],
        ),
    ]
