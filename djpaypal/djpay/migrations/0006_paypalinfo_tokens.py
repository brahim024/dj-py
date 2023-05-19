# Generated by Django 4.2.1 on 2023-05-19 10:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("djpay", "0005_paypalinfo_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="paypalinfo",
            name="tokens",
            field=models.OneToOneField(
                default="",
                on_delete=django.db.models.deletion.CASCADE,
                to="djpay.paypaltoken",
            ),
            preserve_default=False,
        ),
    ]
