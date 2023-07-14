# Generated by Django 4.2.1 on 2023-06-01 16:43

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("djpay", "0008_alter_paypalinfo_tokens"),
    ]

    operations = [
        migrations.RenameField(
            model_name="paypalinfo",
            old_name="scopes",
            new_name="scope",
        ),
        migrations.RenameField(
            model_name="paypalinfo",
            old_name="access_token",
            new_name="token_token",
        ),
        migrations.RemoveField(
            model_name="paypalinfo",
            name="base_url",
        ),
    ]