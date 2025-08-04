from django.apps import AppConfig


class YourAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "userdetail"

    def ready(self):
        import userdetail.signals


# class UserdetailConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'userdetail'
