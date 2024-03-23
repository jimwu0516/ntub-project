# Generated by Django 4.2.10 on 2024-03-12 10:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contribute', '0006_item_item_category'),
        ('borrow', '0003_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item_orders', to='contribute.item'),
        ),
    ]
