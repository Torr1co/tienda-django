# Generated by Django 3.1.4 on 2020-12-26 15:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='articulopedido',
            old_name='quantity',
            new_name='cantidad',
        ),
        migrations.RenameField(
            model_name='articulopedido',
            old_name='product',
            new_name='producto',
        ),
    ]