# Generated by Django 4.0.4 on 2022-05-25 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0003_sizecategory_rename_category_colorcategory_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='colorcategory',
            name='size',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='sizecategory',
            name='size',
            field=models.IntegerField(default=0),
        ),
    ]
