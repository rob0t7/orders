# Generated by Django 4.0.2 on 2022-02-26 00:34

import django.core.validators
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    replaces = [('orders', '0001_initial'), ('orders', '0002_alter_product_name'), ('orders', '0003_alter_product_price')]

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(db_index=True, max_length=255, unique=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
