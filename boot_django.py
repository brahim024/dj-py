# boot_django.py
#
# This file sets up and configures Django. It's used by scripts that need to
# execute as if running in a Django server.
import os
import django
from django.conf import settings
from django.core.management import call_command


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "djpay"))


def boot_django():
    settings.configure(
        BASE_DIR=BASE_DIR,
        DEBUG=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
            }
        },
        INSTALLED_APPS=("djpay",),
        TIME_ZONE="UTC",
        USE_TZ=True,
    )
    django.setup()


boot_django()
call_command("makemigrations", "djpay")
