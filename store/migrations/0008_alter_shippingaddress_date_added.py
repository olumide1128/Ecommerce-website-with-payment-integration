# Generated by Django 3.2.7 on 2021-09-15 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_shippingaddress_date_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingaddress',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]