# Generated by Django 4.2.3 on 2023-11-22 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventi', '0003_evento_stripe_product_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='evento',
            name='stripe_price_id',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
