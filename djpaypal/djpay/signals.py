from django.test.signals import setting_changed
from django.dispatch import receiver



@receiver(setting_changed)
def my_callback(sender, **kwargs):
    print("Request finished!")

