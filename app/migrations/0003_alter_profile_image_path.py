# Generated by Django 4.2.17 on 2024-12-08 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_profile_image_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image_path',
            field=models.ImageField(blank=True, null=True, upload_to='avatars/'),
        ),
    ]
