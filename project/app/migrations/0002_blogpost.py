# Generated by Django 3.0.8 on 2020-07-18 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('content', models.TextField()),
                ('name', models.CharField(max_length=25)),
                ('timeStamp', models.DateTimeField(blank=True)),
            ],
        ),
    ]