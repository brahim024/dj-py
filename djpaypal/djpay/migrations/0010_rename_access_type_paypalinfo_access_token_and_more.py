# Generated by Django 4.2.1 on 2023-06-01 16:44

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("djpay", "0009_rename_scopes_paypalinfo_scope_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="paypalinfo",
            old_name="access_type",
            new_name="access_token",
        ),
        migrations.RenameField(
            model_name="paypalinfo",
            old_name="token_token",
            new_name="token_type",
        ),
    ]
