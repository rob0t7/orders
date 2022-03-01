# Generated by Django 4.0.2 on 2022-03-01 00:09

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_order_order_status_alter_order_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('quantity', models.IntegerField(default=1)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('product_name', models.CharField(max_length=255)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='line_items', to='orders.order')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]