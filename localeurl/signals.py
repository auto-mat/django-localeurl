import django.dispatch

locale_change = django.dispatch.Signal(providing_args=["locale", "user"])
