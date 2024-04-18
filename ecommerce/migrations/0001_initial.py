# Generated by Django 5.0.4 on 2024-04-18 03:07

import cloudinary.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250)),
                ('description', models.TextField()),
                ('image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('price', models.FloatField()),
                ('stock', models.IntegerField()),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'products',
            },
        ),
        migrations.CreateModel(
            name='SaleModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('total', models.FloatField()),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'sales',
            },
        ),
        migrations.CreateModel(
            name='SaleDetailModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField()),
                ('price', models.FloatField()),
                ('subtotal', models.FloatField()),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.productmodel')),
                ('sale_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.salemodel')),
            ],
            options={
                'db_table': 'sale_details',
            },
        ),
    ]
