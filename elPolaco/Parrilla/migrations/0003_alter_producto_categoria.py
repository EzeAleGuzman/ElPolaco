# Generated by Django 4.2.16 on 2024-11-15 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Parrilla', '0002_remove_producto_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='categoria',
            field=models.CharField(choices=[('sandwiches', 'Sandwiches'), ('porciones', 'Porciones'), ('ensaladas', 'Ensaladas'), ('papas', 'Papas'), ('bebidas', 'Bebidas')], max_length=50),
        ),
    ]