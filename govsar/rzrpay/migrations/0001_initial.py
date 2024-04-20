# Generated by Django 5.0 on 2024-03-23 11:49

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('website', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('razorpay_order_id', models.CharField(max_length=256)),
                ('amount', models.FloatField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('failed', 'Failed'), ('success', 'Success')], max_length=7)),
                ('tax', models.FloatField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('items', models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='website.item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]