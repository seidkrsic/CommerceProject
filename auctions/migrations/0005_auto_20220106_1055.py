# Generated by Django 3.0.1 on 2022-01-06 09:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auto_20220105_2139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='bid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auctions.Bid'),
        ),
    ]
