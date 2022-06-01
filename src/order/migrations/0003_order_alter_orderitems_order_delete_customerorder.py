# Generated by Django 4.0.4 on 2022-05-27 09:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0002_customerorder_orderitems_delete_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('zipcode', models.CharField(max_length=6)),
                ('city', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('total', models.FloatField()),
                ('is_valided', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now=True)),
                ('state_id', models.ForeignKey(default=3, null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.state')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='orderitems',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.order'),
        ),
        migrations.DeleteModel(
            name='CustomerOrder',
        ),
    ]
