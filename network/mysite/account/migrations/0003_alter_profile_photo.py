# Generated by Django 4.0.6 on 2022-08-06 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, default='defaultr/zero_photo.jpg', upload_to='users/%Y/%m/%d'),
        ),
    ]