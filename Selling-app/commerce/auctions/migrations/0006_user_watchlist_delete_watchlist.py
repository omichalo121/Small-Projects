# Generated by Django 4.2.3 on 2023-07-27 10:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0005_watchlist"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="watchlist",
            field=models.ManyToManyField(
                blank=True, related_name="watchers", to="auctions.listing"
            ),
        ),
        migrations.DeleteModel(
            name="Watchlist",
        ),
    ]
