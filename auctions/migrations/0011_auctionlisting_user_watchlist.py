# Generated by Django 3.0.1 on 2022-01-06 15:48

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_auto_20220106_1502'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='user_watchlist',
            field=models.ManyToManyField(blank=True, null=True, related_name='auctions', to=settings.AUTH_USER_MODEL),
        ),
    ]
