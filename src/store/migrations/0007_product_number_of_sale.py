# Generated by Django 4.0.4 on 2022-06-08 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_alter_product_images_alter_product_product_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='number_of_sale',
            field=models.IntegerField(default=0),
        ),
    ]
