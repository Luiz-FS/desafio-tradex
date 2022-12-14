# Generated by Django 4.1.2 on 2022-11-11 23:08

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

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
                ('name', models.CharField(max_length=200)),
                ('ean', models.PositiveIntegerField()),
                ('image', models.CharField(max_length=250)),
                ('weight', models.PositiveIntegerField()),
                ('min_cost', models.DecimalField(decimal_places=2, max_digits=8)),
                ('max_cost', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
