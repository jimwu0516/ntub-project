# Generated by Django 4.2.10 on 2024-02-15 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contribute', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='item_image',
            field=models.ImageField(blank=True, null=True, upload_to='item_images/'),
        ),
    ]
