# Generated by Django 4.2.3 on 2023-07-27 12:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0006_user_watchlist_delete_watchlist"),
    ]

    operations = [
        migrations.AddField(
            model_name="listing",
            name="active",
            field=models.CharField(default="Y", max_length=1),
        ),
    ]
