# Generated by Django 4.2.3 on 2023-08-02 07:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mail", "0002_alter_email_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="email",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
