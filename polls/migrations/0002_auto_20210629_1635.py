# Generated by Django 3.1.4 on 2021-06-29 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='myuploadfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('myfiles', models.FileField(upload_to='')),
            ],
        ),
        migrations.DeleteModel(
            name='Hotel',
        ),
    ]
