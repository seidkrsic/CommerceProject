# Generated by Django 3.0.1 on 2022-01-05 20:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20220105_2119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='comments',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auctions.Comments'),
        ),
    ]
